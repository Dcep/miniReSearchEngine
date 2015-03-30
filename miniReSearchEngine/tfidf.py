__author__ = 'dan'
import sys, os, math, json, csv

from operator import itemgetter
from lemma import lemma


class searchAlgorithm:
	def __init__(self):
		self.invFile = {}
		self.bagOfWords = {}
		self.returnCount = 20

		""" Epsilon values
			Epsilon is used to stop division by 0, but can also be used as a smoothing value
			idfEpsilon is used as a smoothing value
		"""
		self.Epsilon = sys.float_info.epsilon
		# idf smoothing
		self.idfEpsilon = sys.float_info.epsilon
		#k usually exists in range [1.0 -2.0]
		self.k = 1.6
		#b should be between [0-1] without other information should be set to 0.75
		self.b = 0.75
		reader = open('docIndex.csv')
		self.originalDocs = {}
		for row in reader:
			self.originalDocs[row.split(',')[0]] = row.split()[1]


	def docInfo(self, document, payload, data, file, model):
		self.send[document] = json.dumps(dict(id=document, Job_Title="query: " +
		                                                             payload + ",<br> " + model + ": " + str(
			self.docList[document]) + "<br> original doc: " + self.originalDocs[document] +
		                                                             ", <br> lemma: " + " ".join(data),
		                                      Job_Requirements=file, retCount=self.returnCount))

	def tfidf(self, payload, data):
		for word in self.docDict:
			word = word.encode('ascii', 'ignore')
			for document in self.docDict[word]['docNo']:
				with open("lemma/" + str(document) + '.txt') as current_file:
					try:
						self.docList[document] = self.docList[document] + (
							(self.docDict[word]['docNo'][document]["Freq"] * self.idf) + self.Epsilon)
					except:
						self.docList[document] = ((self.docDict[word]['docNo'][document]["Freq"] * self.idf[
							word]) + self.Epsilon) * payload.split().count(word)
					self.docInfo(document, payload, data, current_file.read(), "tf-idf")


	def cosine_tfidf(self, payload, data):

		for word in self.docDict:
			for document in self.docDict[word]['docNo']:
				try:
					self.docList[document].append(
						(self.docDict[word]['docNo'][document]["Freq"] * self.idf[word]) + self.Epsilon)
				except:
					self.docList[document] = []
					self.docList[document].append(
						(self.docDict[word]['docNo'][document]["Freq"] * self.idf[word]) + self.Epsilon)

		tfidfMag = {}
		for document in self.docList:
			for tfidf in self.docList[document]:
				try:
					tfidfMag[document] += tfidf * tfidf
				except:
					tfidfMag[document] = tfidf * tfidf
		queryMag = 0
		for word in payload.split():
			queryMag += payload.split().count(word) ** 2

		for document in tfidfMag:
			tfidfMag[document] = math.sqrt(tfidfMag[document])
		queryMag = math.sqrt(queryMag)

		for document in tfidfMag:
			with open("clean/" + self.originalDocs[document]) as current_file:
				mag = (queryMag * tfidfMag[document]) + self.Epsilon
				self.docList[document] = sum(self.docList[document]) / mag
				self.docInfo(document, payload, data, current_file.read(), 'tf-idf cosine')

	def okapiBM25(self, query, data):

		print self.b
		print self.k
		# maybe convert the BM25 calc to internal function
		for word in self.docDict:
			for document in self.docDict[word]['docNo']:
				try:
					self.docList[document].append(self.idf[word] *
					                              (self.docDict[word]['docNo'][document]["Freq"] * (self.k + 1)) /
					                              (self.docDict[word]['docNo'][document]["Freq"] + self.k *
					                               (1 - self.b + self.b * (
						                               self.bagOfWords[document]["docWordCountTotal"] / self.bagOfWords[
							                               'average']))))
				except:
					self.docList[document] = []
					self.docList[document].append(self.idf[word] *
					                              (self.docDict[word]['docNo'][document]["Freq"] * (self.k + 1)) /
					                              (self.docDict[word]['docNo'][document]["Freq"] + self.k *
					                               (1 - self.b + self.b * (
						                               self.bagOfWords[document]["docWordCountTotal"] / self.bagOfWords[
							                               'average']))))
		for document in self.docList:
			with open("clean/" + self.originalDocs[document]) as current_file:
				self.docList[document] = sum(self.docList[document])
				self.docInfo(document, query, data, current_file.read(), 'Okapi-BM25')

	def calc_idf(self, data, payload):
		wcount = len(data)
		self.idf = {}
		self.docDict = {}
		self.docList = {}
		# calculate idf for all words in the query
		for i in range(wcount):
			try:
				i = int(i)
				print data[i]
				self.docDict[data[i]] = self.invFile[data[i]]
				print payload['idf']
				if payload['idf'] == 'BIM':
					self.idf[data[i]] = (math.log(
						(self.invFile['totalDocuments'] - self.docDict[data[i]]['DocCount'] + self.idfEpsilon) / (
							self.docDict[data[i]]['DocCount'] + self.idfEpsilon)))
				else:
					print "here"
					self.idf[data[i]] = (math.log((self.invFile['totalDocuments'] + self.idfEpsilon) / (
						self.docDict[data[i]]['DocCount'] + self.idfEpsilon)))
					print self.idf[data[i]]
			except:
				#del self.docDict[data[i]]
				print "word not in corpus"
		if not self.docDict:
			raise KeyError("no available queries")

	def query(self, payload):
		self.send = {}
		model = payload['model']
		query = payload['MSG']
		lem = lemma()
		data = []
		# self.returnCount = returnCount
		data.extend([i for i in lem.return_lemma(query)])
		try:
			self.calc_idf(data, payload)
			if model == 'product':
				self.tfidf(query, data)
			elif model == 'Okapi':
				self.okapiBM25(query, data)
			else:
				self.cosine_tfidf(query, data)
			count = 0

			for i in sorted(self.docList.items(), key=itemgetter(1), reverse=True):
				count += 1
				yield self.send[i[0]]
				if count == int(self.returnCount):
					print("return count: " + str(self.returnCount) + "Request count: " + str(count))
					break
		except KeyError as e:
			print e
			self.send = json.dumps(
				{'id': 'NaN', "Job_Title": query + " Not in Collection, <br> lemma: " + " ".join(data),
				 "Job_Requirements": query + " Not in Collection",
				 "Job_Description": query + " Not in Collection"})
			yield self.send