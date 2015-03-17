import os, string, nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

docIndex = open('docIndex.csv', 'a')

wnl = WordNetLemmatizer()

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

counter = 0
for filename in os.listdir("clean"):
	with open("clean/" + filename) as current_file:
		counter += 1
		docIndex.write(str(counter) + ", " + filename + "\n")
		f = open("lemma/" + str(counter) + ".txt", 'a')
		for line in current_file:
			tokens = nltk.word_tokenize(line)
			tagged = nltk.pos_tag(tokens)
			for word in tagged:
				posTag = get_wordnet_pos(word[1])
				if posTag == "":
					f.write(wnl.lemmatize(word[0]) + " ")
				else:
					f.write(wnl.lemmatize(word[0], pos=posTag) + " ")

		print("counter:" + str(counter))
