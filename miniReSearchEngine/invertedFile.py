from collections import defaultdict
import os, nltk, json



class miniReSearchIF():

	def __init__(self):
		filesDir = "lemma/"
		#invertedFile = self.makeInvertedFile()


	def l(self):
		return defaultdict(self.l)

	def makeInvertedFile(self):

		invertedFile = self.l()
		docWordCoutns = self.l()
		DocumentsCount = 0
		for filename in os.listdir(self.filesDir):
			with open(self.filesDir + filename) as current_file:
				DocumentsCount += 1
				tokens = nltk.word_tokenize(current_file.read())
				counter = 0
				for word in set(tokens):
					try:
						invertedFile[word]['DocCount'] += 1
					except:
						invertedFile[word]['DocCount'] = 1
				for word in tokens:
					counter += 1
					try:
						invertedFile[word]['FreqCount'] += 1
					except:
						invertedFile[word]['FreqCount'] = 1
					try:
						invertedFile[word]['docNo'][filename.split('.')[0]]['Freq'] += 1
					except:
						invertedFile[word]['docNo'][filename.split('.')[0]]['Freq'] = 1
					try:
						invertedFile[word]['docNo'][filename.split('.')[0]]['WordPosition'].append(str(counter))
					except:
						invertedFile[word]['docNo'][filename.split('.')[0]]['WordPosition'] = []
						invertedFile[word]['docNo'][filename.split('.')[0]]['WordPosition'].append(str(counter))
					try:
						docWordCoutns[filename.split('.')[0]][word] += 1
					except:
						docWordCoutns[filename.split('.')[0]][word] = 1
					try:
						docWordCoutns[filename.split('.')[0]]["docWordCountTotal"] += 1
					except:
						docWordCoutns[filename.split('.')[0]]["docWordCountTotal"] = 1
		invertedFile['totalDocuments'] = DocumentsCount
		return invertedFile, docWordCoutns




if __name__ == '__main__':

	mIF =  miniReSearchIF()
	mIF.filesDir = "lemma/"
	data, words = mIF.makeInvertedFile()
	for i in words:
		print words[i]['docWwordCountTotal']
	print(json.dumps(data['cleavage']))
	print json.dumps(data['cleavage']['FreqCount'])
	print json.dumps(data['cleavage']['DocCount'])
	for i in data['cleavage']['docNo']:
		print json.dumps(data['cleavage']['docNo'][i])

