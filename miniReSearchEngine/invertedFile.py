from collections import defaultdict
import os, nltk

l = lambda: defaultdict(l)

invertedFile = l()

for filename in os.listdir("lemma"):
	with open("lemma/" + filename) as current_file:
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



for word in invertedFile:
	print word
	print 'DocCount:' + str(invertedFile[word]['DocCount'])
	print 'FreqCount' + str(invertedFile[word]['FreqCount'])
	for doc in invertedFile[word]['docNo']:
		print 'docNo:' + str(doc) + ' Freq' +  str(invertedFile[word]['docNo'][doc]['Freq'])
		print 'docNo:' + str(doc) + ' WordPosition' + str(invertedFile[word]['docNo'][doc]['WordPosition'])