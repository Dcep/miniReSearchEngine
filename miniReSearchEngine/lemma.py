"""
miniResearchEngine

A bare bones search engine for research

lemmatize words in text documents and search strings so that similar words can be more easily found when searching.

"""


import os, string, nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

class lemma:
	"""lemmatize a document, sentence or word"""

	def __init__(self):
		self.wnl = WordNetLemmatizer()

	#Method taken from stackoverflow
	@staticmethod
	def get_wordnet_pos(treebank_tag):
		if treebank_tag.startswith('J'):
			return wordnet.ADJ
		elif treebank_tag.startswith('V'):
			return wordnet.VERB
		elif treebank_tag.startswith('N'):
			return wordnet.NOUN
		elif treebank_tag.startswith('R'):
			return wordnet.ADV
		elif treebank_tag.startswith('S'):
			return wordnet.ADJ_SAT
		else:
			return ''

	def return_lemma(self, line):
		tokens = nltk.word_tokenize(line)
		tagged = nltk.pos_tag(tokens)
		for word in tagged:
			posTag = self.get_wordnet_pos(word[1])
			if posTag == "":
				yield self.wnl.lemmatize(word[0])
			else:
				yield self.wnl.lemmatize(word[0], pos=posTag)


if __name__ == '__main__':
	lem = lemma()
	docIndex = open('docIndex.csv', 'a')
	counter = 0
	for filename in os.listdir("clean"):
		with open("clean/" + filename) as current_file:
			counter += 1
			docIndex.write(str(counter) + ", " + filename + "\n")
			f = open("lemma/" + str(counter) + ".txt", 'a')
			for line in current_file:
				for word in lem.return_lemma(line):
					print word
					f.write(word + " ")

			print("counter:" + str(counter))
