__author__ = 'dan'
import sys, os, math, json

from operator import itemgetter
from lemma import lemma

class searchAlgorithm:

	@staticmethod
	def tfidf(payload,invFile, returnCount):
		lem = lemma()
		data = []
		data.extend([i for i in lem.return_lemma(payload)])# payload.split()
		wcount = len(data)
		try:
			print payload
			print data
			idf = {}
			docDict = {}
			tfidf = {}
			send = {}
			for i in range(wcount):
				try:
					docDict[data[i]] = (json.loads(json.dumps(invFile[data[i]], ensure_ascii=False)))
					idf[data[i]] = (math.log(invFile['totalDocuments'] / docDict[data[i]]['DocCount']))
				except:
					del docDict[data[i]]
					print "word not in corpus"
			if not docDict:
				raise KeyError("no available queries")

			retDocCounts = len([i for i in docDict for x in docDict[i]['docNo']])
			if retDocCounts < returnCount:
				returnCount = retDocCounts
			for word in docDict:
				for document in docDict[word]['docNo']:
					with open("lemma/" + str(document) + '.txt') as current_file:
						try:
							tfidf[document] = tfidf[document] + (docDict[word]['docNo'][document]["Freq"] * idf)
						except:
							tfidf[document] = docDict[word]['docNo'][document]["Freq"] * idf[word]

						send[document] = json.dumps({'id': document, "Job_Title": "query: " +
							payload + ", tf-idf: " + str(tfidf[document]) + ", lemma: " + " ".join(data), "Job_Requirements": current_file.read(),
															"retCount": returnCount})

			count = 0

			print tfidf.items().sort(key=itemgetter(1),reverse=True)
			for i in sorted(tfidf.items(), key=itemgetter(1),reverse=True):
				print i
				count += 1
				if count > int(returnCount):
					print "Got to break"
					break
				yield send[i[0]]
				print "retcount: " + str(returnCount) + " count: " + str(count)


		except:
			send = json.dumps({'id': 0, "Job_Title": payload + " Not in database, lemma: " + " ".join(data),
							   "Job_Requirements": payload + " Not in database",
							   "Job_Description": payload + " Not in database"})
			yield send