__author__ = 'dan'
import sys, os, math, json, csv

from operator import itemgetter
from lemma import lemma


class searchAlgorithm:

	def __init__(self):
		self.docDict = {}
		self.docList = {}
		self.returnCount = 20
		self.send = {}
		self.Epsilon = 0.5#sys.float_info.epsilon
		reader = open('docIndex.csv')
		self.originalDocs = {}
		for row in reader:
			self.originalDocs[row.split(',')[0]] = row.split()[1]


	def docInfo(self,document, payload, data, file):
		self.send[document] = json.dumps(dict(id=document, Job_Title="query: " +
			payload + ",<br> tf-idf cosine: " + str(
			self.docList[document]) + "<br> original doc: " + self.originalDocs[document] +
			", <br> lemma: " + " ".join(data), Job_Requirements=file, retCount=self.returnCount))

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
					self.docInfo(document, payload, data, current_file.read())


	def cosine_tfidf(self, payload, data):

		for word in self.docDict:
			for document in self.docDict[word]['docNo']:
				try:
					self.docList[document].append((self.docDict[word]['docNo'][document]["Freq"] * self.idf[word]) + self.Epsilon)
				except:
					self.docList[document] = []
					self.docList[document].append((self.docDict[word]['docNo'][document]["Freq"] * self.idf[word]) + self.Epsilon)


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
				self.docInfo(document, payload, data, current_file.read())

	def query(self, payload, invFile, model):
		lem = lemma()
		data = []
		#self.returnCount = returnCount
		data.extend([i for i in lem.return_lemma(payload)])
		wcount = len(data)
		try:
			self.idf = {}

			for i in range(wcount):
				try:
					self.docDict[data[i]] = (json.loads(json.dumps(invFile[data[i]], ensure_ascii=False)))
					self.idf[data[i]] = (math.log(invFile['totalDocuments'] / self.docDict[data[i]]['DocCount']))
				except:
					del self.docDict[data[i]]
					print "word not in corpus"
			if not self.docDict:
				raise KeyError("no available queries")

			if model == 'product':
				self.tfidf(payload, data)
			else:
				self.cosine_tfidf(payload, data)
			count = 0


			for i in sorted(self.docList.items(), key=itemgetter(1), reverse=True):
					count += 1
					yield self.send[i[0]]
					if count == int(self.returnCount):
						print("return count: " + str(self.returnCount) + "Request count: " + str(count))
						break
		except:
			self.send = json.dumps({'id': 'NaN', "Job_Title": payload + " Not in Collection, <br> lemma: " + " ".join(data),
		                   "Job_Requirements": payload + " Not in Collection",
		                  "Job_Description": payload + " Not in Collection"})
			yield self.send