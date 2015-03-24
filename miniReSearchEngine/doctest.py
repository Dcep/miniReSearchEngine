

reader = open('docIndex.csv')
originalDocs = {}
for row in reader:
	print row
	with open("ElectricityDocs/" + row.split()[1]) as current_file:
		print current_file.read()
