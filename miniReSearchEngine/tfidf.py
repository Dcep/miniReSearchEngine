__author__ = 'dan'
import sys, os, math, json

from operator import itemgetter
from lemma import lemma


class searchAlgorithm:

    def __init__(self):
        self.docDict = {}
        self.docList = {}
        self.returnCount = 20
        self.send = {}

    def tfidf(self, payload, data):
        for word in self.docDict:
            word = word.encode('ascii', 'ignore')
            for document in self.docDict[word]['docNo']:
                with open("lemma/" + str(document) + '.txt') as current_file:
                    try:
                        self.docList[document] = self.docList[document] + (self.docDict[word]['docNo'][document]["Freq"] * self.idf)
                    except:
                        self.docList[document] = (self.docDict[word]['docNo'][document]["Freq"] * self.idf[word]) * payload.split().count(word)

                    self.send[document] = json.dumps({'id': document, "Job_Title": "query: " +
                                                                              payload + ", tf-idf dot product: " + str(
                        self.docList[document]) + ", lemma: " + " ".join(data), "Job_Requirements": current_file.read(),
                                                 "retCount": self.returnCount})

    def cosine_tfidf(self, payload, data):
        for word in self.docDict:
            for document in self.docDict[word]['docNo']:
                try:
                    self.docList[document].append(self.docDict[word]['docNo'][document]["Freq"] * self.idf[word])
                except:
                    self.docList[document] = []
                    self.docList[document].append(self.docDict[word]['docNo'][document]["Freq"] * self.idf[word])
                #print sum(self.tfidfList[document])

        tfidfMag = {}
        for document in self.docList:
            for tfidf in self.docList[document]:
                try:
                    tfidfMag[document] += tfidf * tfidf
                except:
                    tfidfMag[document] = tfidf * tfidf
        queryMag = 0
        for word in payload.split():
            queryMag += payload.split().count(word)**2

        for document in tfidfMag:
            tfidfMag[document] = math.sqrt(tfidfMag[document])
        queryMag = math.sqrt(queryMag)

        for document in tfidfMag:
            with open("lemma/" + str(document) + '.txt') as current_file:
                mag = queryMag * tfidfMag[document]
                if mag == 0:
                    mag = 0.0000000001
                self.docList[document] = sum(self.docList[document]) / mag
                self.send[document] = json.dumps({'id': document, "Job_Title": "query: " +
                                                                                  payload + ", tf-idf dot product: " + str(
                            self.docList[document]) + ", lemma: " + " ".join(data), "Job_Requirements": current_file.read(),
                                                     "retCount": self.returnCount})





                    #self.tfidfList[document].append(self.docDict[word]['docNo'][document]["Freq"] * self.idf[word])
        print self.docList

    #@staticmethod
    def query(self, payload, invFile, returnCount):
        lem = lemma()
        data = []
        self.returnCount = returnCount
        data.extend([i for i in lem.return_lemma(payload)])  # payload.split()
        wcount = len(data)
        #try:
        print payload
        print data
        self.idf = {}
        #docDict = {}
        #tfidf = {}

        for i in range(wcount):
            try:
                self.docDict[data[i]] = (json.loads(json.dumps(invFile[data[i]], ensure_ascii=False)))
                self.idf[data[i]] = (math.log(invFile['totalDocuments'] / self.docDict[data[i]]['DocCount']))
            except:
                del self.docDict[data[i]]
                print "word not in corpus"
        if not self.docDict:
            raise KeyError("no available queries")
        #self.tfidf(payload, data)
        self.cosine_tfidf(payload, data)
        count = 0

        #print tfidf.items().sort(key=itemgetter(1), reverse=True)
        for i in sorted(self.docList.items(), key=itemgetter(1), reverse=True):
            print i
            count += 1
            print "retcoutn:" + str(self.returnCount)

            yield self.send[i[0]]
            if count == int(self.returnCount):
                print "Got to break"
                break
            print "retcount: " + str(self.returnCount) + " count: " + str(count)


        #except:
        #    self.send = json.dumps({'id': 0, "Job_Title": payload + " Not in database, lemma: " + " ".join(data),
        #                   "Job_Requirements": payload + " Not in database",
        #                  "Job_Description": payload + " Not in database"})
        #    yield self.send