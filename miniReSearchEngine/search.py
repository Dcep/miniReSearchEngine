import sys, os

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
		self.invFile = miniIst.makeInvertedFile()
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
		#for i in self.invFile[payload]:
		data = json.dumps(self.invFile[payload], ensure_ascii=False)
		data = json.loads(data)
		print data
		for i in data['docNo']:
			with open("lemma/" + i + '.txt') as current_file:
				payload = json.dumps({'id': i, "Job_Title": i, "Job_Requirements": current_file.read(), "Job_Description": "Nan"})
				print payload
				self.sendMessage(payload, isBinary=False)



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
