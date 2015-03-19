import sys, os, math

from invertedFile import miniReSearchIF
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

import json

from autobahn.twisted.websocket import WebSocketServerFactory, \
	WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, \
	HTTPChannelHixie76Aware


class EchoServerProtocol(WebSocketServerProtocol,miniReSearchIF):

	def __init__(self):
		miniIst = miniReSearchIF()
		miniIst.filesDir = "lemma/"
		self.invFile, self.counts = miniIst.makeInvertedFile()
		self.totalDocs = self.invFile['totalDocuments']
		#miniReSearchIF.__init__()

	def onConnect(self, request):
		print("WebSocket connection request: {}".format(request))

	def onMessage(self, payload, isBinary):
		print "connected \n"
		print payload
		obj = json.loads(payload)
		print obj['MSG']
		if obj['TYPE'] == 'qry':
			self.search(obj["MSG"])

	def search(self, payload):
		print payload
		payload = payload.split()
		wcount = len(payload)
		#try:

		if wcount == 1:
			data = json.dumps(self.invFile[payload[0]], ensure_ascii=False)
			data = json.loads(data)
			idf = math.log(self.totalDocs/data['DocCount'])
			send = {}
			for i in data['docNo']:
				with open("lemma/" + str(i) + '.txt') as current_file:
						tf_idf = data['docNo'][i]["Freq"] * idf
						print 'tf-idf: ' + str(tf_idf)
						send[tf_idf] = json.dumps({'id': i, "Job_Title": "query: " + payload[0] + " tf-idf: " + str(tf_idf), "Job_Requirements": current_file.read(), "Job_Description": "Nan"})
			for i in sorted(send.keys()):
				self.sendMessage(send[i], isBinary=False)
		else:
			idf = {}
			docDict = {}
			tfidf = {}
			send = {}
			for i in range(wcount):
				try:
					docDict[payload[i]] = (json.loads(json.dumps(self.invFile[payload[i]], ensure_ascii=False)))
					idf[payload[i]] = (math.log(self.totalDocs/docDict[payload[i]]['DocCount']))
				except:
					#remove item that is not in corpus
					del docDict[payload[i]]
					print "word not in corpus"
			print docDict
			print idf
			for word in docDict:
				print word
				print docDict[word]['docNo']
				for document in docDict[word]['docNo']:
					with open("lemma/" + str(document) + '.txt') as current_file:
						try:
							tfidf[document] = tfidf[document] + (docDict[word]['docNo'][document]["Freq"] * idf)
						except:
							tfidf[document] = docDict[word]['docNo'][document]["Freq"] * idf[word]

						send[tfidf[document]] = json.dumps({'id': document, "Job_Title": "query: " + " ".join(payload) + " tf-idf: " + str(tfidf[document]), "Job_Requirements": current_file.read(), "Job_Description": "Nan"})
			for i in sorted(send.keys()):
				self.sendMessage(send[i], isBinary=False)
			#print tfidf


		#except:
		#	send = json.dumps({'id': 0, "Job_Title": payload + " not in databse", "Job_Requirements": payload + " not in databse", "Job_Description": payload + " not in databse"})
		#	self.sendMessage(send, isBinary=False)



if __name__ == '__main__':

	if len(sys.argv) > 1 and sys.argv[1] == 'debug':
		log.startLogging(sys.stdout)
		debug = True
	else:
		debug = False

	factory = WebSocketServerFactory("ws://localhost:8080",
									debug=debug,
									debugCodePaths=debug)

	factory.protocol = EchoServerProtocol
	factory.setProtocolOptions(allowHixie76=True)  # needed if Hixie76 is to be supported

	resource = WebSocketResource(factory)

	# # we server static files under "/" ..
	root = File(".")

	## and our WebSocket server under "/ws"
	root.putChild("ws", resource)

	## both under one Twisted Web Site
	site = Site(root)
	site.protocol = HTTPChannelHixie76Aware  # needed if Hixie76 is to be supported
	reactor.listenTCP(8080, site)

	reactor.run()
__author__ = 'dan'
