'''
miniResearchEngine

A bare bones search engine for research

'''

from collections import defaultdict
import os, nltk, json



class miniReSearchIF():
	'''create inverted file from a list of text documents in a folder.
		Notes:  This would be better setup as a shelve object,
				look at persistent dicts http://code.activestate.com/recipes/576642/
				or just cpickle the dict

	'''
	def __init__(self):
		self.filesDir = "lemma/"
		#self.invertedFile = self.makeInvertedFile()


	def l(self):
		return defaultdict(self.l)

	def makeInvertedFile(self):
		#A counter Object may be better in place of the dict here
		invertedFile = self.l()
		docWordCounts = self.l()
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
						docWordCounts[filename.split('.')[0]][word] += 1
					except:
						docWordCounts[filename.split('.')[0]][word] = 1
					try:
						docWordCounts[filename.split('.')[0]]["docWordCountTotal"] += 1
					except:
						docWordCounts[filename.split('.')[0]]["docWordCountTotal"] = 1
		invertedFile['totalDocuments'] = DocumentsCount
		return invertedFile#, docWordCounts
		#return invertedFile




if __name__ == '__main__':

	mIF =  miniReSearchIF()
	mIF.filesDir = "lemma/"
	#data = mIF.makeInvertedFile()

	print mIF.invertedFile
	for i in words:
		print words[i]['docWwordCountTotal']
	print(json.dumps(data['document']))
	print json.dumps(data['document']['FreqCount'])
	print json.dumps(data['document']['DocCount'])
	for i in data['document']['docNo']:
		print json.dumps(data['document']['docNo'][i])

