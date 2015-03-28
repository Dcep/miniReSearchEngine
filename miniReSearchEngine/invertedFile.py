'''
miniResearchEngine

A bare bones search engine for research

'''

from collections import defaultdict
import os, nltk, json, cPickle


class miniReSearchIF():
    '''create inverted file from a list of text documents in a folder.
		Notes:  This would be better setup as a shelve object,
				look at persistent dicts http://code.activestate.com/recipes/576642/
				or just cpickle the dict

	'''

    def __init__(self):
        self.filesDir = "lemma/"

    def l(self):
        return defaultdict(self.l)

    def makeInvertedFile(self):
        #A counter Object may be better in place of the dict here
        invertedFile = self.l()
        docWordCounts = self.l()
        f = open('STOP.txt', 'r')
        stopwords = set([i.strip() for i in f])
        DocumentsCount = 0
        for filename in os.listdir(self.filesDir):
            with open(self.filesDir + filename) as current_file:
                DocumentsCount += 1
                tokens = nltk.word_tokenize(current_file.read())
                counter = 0
                for word in set(tokens):
                    #word = word.lower()
                    if word.lower() not in stopwords:
                        try:
                            invertedFile[word]['DocCount'] += 1
                        except:
                            invertedFile[word]['DocCount'] = 1
                for word in tokens:
                    #word = word.lower()
                    if word.lower() not in stopwords:
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

        docCounts = []
        for i in docWordCounts:
            docCounts.append(docWordCounts[i]["docWordCountTotal"])
        average = sum(docCounts) / len(docCounts)
        docWordCounts['average'] = average
        invertedFile['totalDocuments'] = DocumentsCount
        invertedFile =  json.dumps(invertedFile)

        output = open('Database/invertedFile.pkl', 'wb')
        data = cPickle.dumps(invertedFile,1)
        output.write(data)
        output.close()

        outputDoc = open('Database/docWordCounts.pkl', 'w')
        docWordCounts = json.dumps(docWordCounts)
        dataDoc = cPickle.dumps(docWordCounts, 1)
        outputDoc.write(dataDoc)
        outputDoc.close()

        return invertedFile  #, docWordCounts

    #return invertedFile


if __name__ == '__main__':

    mIF = miniReSearchIF()
    mIF.filesDir = "lemma/"
    mIF.makeInvertedFile()

    pkl_file = open('Database/invertedFile.pkl', 'rb')
    data = cPickle.load(pkl_file)
    pkl_file.close()

    #data = json.loads(data)
    #for i in data:
    #    print data[i]

    pkl_file = open('Database/docWordCounts.pkl', 'rb')
    data = cPickle.load(pkl_file)
    pkl_file.close()

    data = json.loads(data)

    docCounts = []
    for i in data:
        docCounts.append(data[i]["docWordCountTotal"])

    average = sum(docCounts) / len(docCounts)
    print average