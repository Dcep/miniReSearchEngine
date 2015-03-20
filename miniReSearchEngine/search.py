'''
miniResearchEngine

A bare bones search engine for research

'''

import sys, os, math, json

from operator import itemgetter
from invertedFile import miniReSearchIF
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File


from autobahn.twisted.websocket import WebSocketServerFactory, \
	WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, \
	HTTPChannelHixie76Aware


class EchoServerProtocol(WebSocketServerProtocol,miniReSearchIF):
	""" Main socket interface for search engine
		Notes:  tf-idf calculation should be removed from this file and moved
				to a new object so new search measures can also be implemented.
	"""

	def __init__(self):
		self.invFile
		#self.totalDocs = 180# self.invFile['totalDocuments']
		#return 20 documents by default
		self.count = 20


	def setinvFile(self):
		self.invFile = self.makeInvertedFile()

	def onConnect(self, request):
		print("WebSocket connection request: {}".format(request))

	def onMessage(self, payload, isBinary):
		print "connected \n"
		print payload
		obj = json.loads(payload)
		if obj['TYPE'] == 'qry':
			self.RetCount = obj["count"]
			self.search(obj["MSG"])
		elif obj['TYPE'] == 'bad':
			f = open("badDocs.txt", 'a')
			f.write(payload + "\n")

	def search(self, payload):

		payload = payload.split()
		wcount = len(payload)
		try:
			idf = {}
			docDict = {}
			tfidf = {}
			send = {}
			print payload
			#print self.invFile['Radiofrequency']
			for i in range(wcount):
				try:
					docDict[payload[i]] = (json.loads(json.dumps(self.invFile[payload[i]], ensure_ascii=False)))
					idf[payload[i]] = (math.log(self.invFile['totalDocuments'] / docDict[payload[i]]['DocCount']))
				except:
					del docDict[payload[i]]
					print "word not in corpus"
			if not docDict:
				raise KeyError("no available queries")

			retDocCounts = len([i for i in docDict for x in docDict[i]['docNo']])
			if retDocCounts < self.count:
				self.count = retDocCounts
			for word in docDict:
				for document in docDict[word]['docNo']:
					with open("lemma/" + str(document) + '.txt') as current_file:
						try:
							tfidf[document] = tfidf[document] + (docDict[word]['docNo'][document]["Freq"] * idf)
						except:
							tfidf[document] = docDict[word]['docNo'][document]["Freq"] * idf[word]

						send[document] = json.dumps({'id': document, "Job_Title": "query: " + " ".join(
							payload) + ", tf-idf: " + str(tfidf[document]), "Job_Requirements": current_file.read(),
															"retCount": self.count})

			count = 0

			print tfidf.items().sort(key=itemgetter(1),reverse=True)
			for i in sorted(tfidf.items(), key=itemgetter(1),reverse=True):
				print i
				count += 1
				if count > int(self.RetCount):
					print "Got to break"
					break
				self.sendMessage(send[i[0]], isBinary=False)
				print "retcount: " + str(self.RetCount) + " count: " + str(count)


		except:
			send = json.dumps({'id': 0, "Job_Title": " ".join(payload) + " Not in database",
							   "Job_Requirements": " ".join(payload) + " Not in database",
							   "Job_Description": " ".join(payload) + " Not in database"})
			self.sendMessage(send, isBinary=False)


if __name__ == '__main__':

	if len(sys.argv) > 1 and sys.argv[1] == 'debug':
		log.startLogging(sys.stdout)
		debug = True
	else:
		debug = False

	factory = WebSocketServerFactory("ws://localhost:8085",
									 debug=debug,
									 debugCodePaths=debug)
	miniIst = miniReSearchIF()
	miniIst.filesDir = "lemma/"

	factory.protocol = EchoServerProtocol

	print "Loading Inverted File"

	factory.protocol.invFile = miniIst.makeInvertedFile()

	print "Loaded Inverted File"

	factory.setProtocolOptions(allowHixie76=True)  # needed if Hixie76 is to be supported

	resource = WebSocketResource(factory)
	# # we server static files under "/" ..
	root = File(".")

	## and our WebSocket server under "/ws"
	root.putChild("ws", resource)

	## both under one Twisted Web Site
	site = Site(root)
	site.protocol = HTTPChannelHixie76Aware  # needed if Hixie76 is to be supported
	reactor.listenTCP(8085, site)

	reactor.run()
__author__ = 'dan'
