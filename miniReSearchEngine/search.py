'''
miniResearchEngine

A bare bones search engine for research

'''

import sys, os, math, json, cPickle, string

from tfidf import searchAlgorithm
#from operator import itemgetter
from invertedFile import miniReSearchIF
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from lemma import lemma

from autobahn.twisted.websocket import WebSocketServerFactory, \
	WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, \
	HTTPChannelHixie76Aware


class EchoServerProtocol(WebSocketServerProtocol, miniReSearchIF):
	""" Main socket interface for search engine
		Notes:  tf-idf calculation should be removed from this file and moved
				to a new object so new search measures can also be implemented.
	"""

	def __init__(self):
		self.algo

	#def setinvFile(self):
	#	self.invFile = self.makeInvertedFile()

	def onConnect(self, request):
		print("WebSocket connection request: {}".format(request))

	def onMessage(self, payload, isBinary):
		print "connected \n"
		print payload
		obj = json.loads(payload)
		if obj['TYPE'] == 'qry':
			self.search(obj)
		elif obj['TYPE'] == 'bad':
			print obj
		#f = open("badDocs.txt", 'a')
		#f.write(payload + "\n")

	def search(self, payload):
		exclude = set(string.punctuation)
		payload['MSG'] = ''.join(ch for ch in payload['MSG'] if ch not in exclude)
		self.algo.returnCount = payload["count"]
		if payload['Epsilon'] != '0':
			self.algo.Epsilon = float(payload['Epsilon'])
		else:
			self.algo.Epsilon = sys.float_info.epsilon
		if payload['idfEpsilon'] != '0':
			self.algo.idfEpsilon = float(payload['idfEpsilon'])
		else:
			self.algo.idfEpsilon = sys.float_info.epsilon
		if "kappa" in payload:
			self.algo.k = float(payload['kappa'])
		if "beta" in payload:
			self.algo.b = float(payload['beta'])
		for data in self.algo.query(payload):
			self.sendMessage(data)


if __name__ == '__main__':

	if len(sys.argv) > 1 and sys.argv[1] == 'debug':
		log.startLogging(sys.stdout)
		debug = True
	else:
		debug = False

	factory = WebSocketServerFactory("ws://localhost:8085",
									 debug=debug,
									 debugCodePaths=debug)
	#miniIst = miniReSearchIF()
	#miniIst.filesDir = "lemma/"

	pkl_file = open('Database/invertedFile.pkl', 'rb')
	data = cPickle.load(pkl_file)
	pkl_file.close()
	pkl_file = open('Database/docWordCounts.pkl', 'rb')
	docData = cPickle.load(pkl_file)
	pkl_file.close()

	factory.protocol = EchoServerProtocol


	print "Loading Inverted File"
	factory.protocol.algo = searchAlgorithm()
	factory.protocol.algo.invFile = json.loads(data)
	factory.protocol.algo.bagOfWords = json.loads(docData)
	#factory.protocol.invFile = miniIst.makeInvertedFile()

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
