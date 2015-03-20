'''
miniResearchEngine

A bare bones search engine for research purposes

'''

import os		#for file reading
import nltk		#for tokenizer
import math		#for sqrt

#returns all the word distributions for all the documents in a dictionary
#Already have vectors

class similarity():

	#vector dot product
	def dotProduct(vector1, vector2):

		dotProduct = 0

		for key1 in vector1:
			try:
				dotProduct += (vector2[key1] * vector1[key1])

		return dotProduct


	#vector magnitude
	def magnitude(vector):

		sumOfSquares = 0

		for key in vector:
			sumOfSquares += vector[key]**2

		return math.sqrt(sumOfSquares)


	#cosine similarity measure between 2 word distribution vectors
	def cosineSimilarity(self, vector1, vector2):

		return self.dotProduct(vector1, vector2) / (self.magnitude(vector1) * self.magnitude(vector2))


	#dot similarity measure between 2 word distribution vectors
	def dotSimilarity(self, vector1, vector2):

		return self.dotProduct(vector1, vector2)

	"""
def test():

	#testing getDocumentWordVector:
	documentWordVector = getAllDocumentWordVectors()
	
	for keys,values in documentWordVector.items():
		print(keys)
		print(values)
	
#	for currentWordVector in documentWordVector:
#		for word in currentWordVector:
#			print(word + " : " + currentWordVector[word] "\n")

	#testing dotProduct:
	vector1 = {"cat":2 , "ate":1 , "the":1 , "dog":3}
	vector2 = {"dog":3 , "killed":2 , "cat's":1 , "father":4}
	
	print("expected: 9 , calculated: " + dotProduct(vector1, vector2))
	
	#testing magnitude:
	print("expected: 3.8729 , calculated: " + magnitude(vector1))
	print("expected: 5.4772 , calculated: " + magnitude(vector2))
	
	print("expected: 0.4242 , calculated: " + cosineSimilarity(vector1, vector2))

def getAllDocumentWordVectors():

	#documentWordVector : holds the word vector for each document
	#currentWordVector : holds the word frequency for each word in the document

	documentNumber = 1
	for filename in os.listdir("lemma"):
		with open("lemma/" + filename) as current_file:

			tokens = nltk.word_tokenize(current_file.read())

			for word in set(tokens):
				try:
					currentWordVector[word] += 1
				except:
					currentWordVector[word] = 1


			documentWordVector[documentNumber] = currentWordVector

	return documentWordVector


#returns the word distribution for the input document
def getWordVector(inputDocument):

	tokens = nltk.word_tokenize(inputDocument)

	for word in set(tokens):
		try:
			wordVector[word] += 1
		except:
			wordVector[word] = 1

	return wordVector

"""