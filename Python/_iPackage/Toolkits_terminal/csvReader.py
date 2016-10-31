import csv
import re
import sys, getopt

class CSVReader(object):
	"""docstring for CSVReader"""
	def __init__(self,inputFile,outputFile):
		super(CSVReader, self).__init__()
		self.read(inputFile,outputFile)
			

	def read(self,inputFile,outputFile):
		# initialization
		dateDict = dict()
		maxTrans = list()
		field = list()

		# check inputFile and outputFile
		if inputFile.split('.')[-1] != 'csv':
			inputFile = inputFile + '.csv'
		if outputFile.split('.')[-1] != 'csv':
			outputFile = outputFile + '.csv'

		# load data
		with open(inputFile, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			# spamreader = csv.DictReader(csvfile)
			for index,row in enumerate(spamreader):
				if index == 0:
					field = re.split(r',',row[3])
					# print field
					continue
				datum = re.split(r',',row[0])
				dateDict.setdefault(datum[2],[])
				dateDict[datum[2]].append(datum[1:])
		
		# filter data
		for key,items in dateDict.items():
			maximum = {'criterion':0,'data':[]}
			for item in items:
				# update rule
				value = float(item[-2]) 	# amount of transaction


				if value == maximum['criterion']:
					maximum['data'].append(item)

				elif value > maximum['criterion']:
					maximum['criterion'] = value
					maximum['data'] = [item]

			maxTrans.append([int(key),maximum['data']])
		maxTrans.sort(key=lambda x:x[0])

		
		# output to csv
		with open(outputFile, 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
			# print ['Date'+','.join(field)]
			spamwriter.writerow(['Date'+','.join(field)])
			for datum in maxTrans:
				for item in datum[1]:
					# print str(datum[0])+','+','.join(item)
					spamwriter.writerow([str(datum[0])+','+','.join(item)])


def main():
	'''
	Debug Version
	'''
	# CSVReader('Douyi_2010-2015.csv','Douyi.csv')
	# return

	'''
	Terminal Version
	'''
	try:
		opts, args = getopt.getopt(sys.argv[1:], 't:i:o:h', ['template','input', 'output', 'help'])
	except getopt.GetoptError as err:
		# print help information and exit:
		helpInfo()
		sys.exit(1)

	inputFile = ''
	outputFile = ''
	template = 'format'

	for o, a in opts:
		if o in ('-i', '--input'):
			inputFile = a
		elif o in ('-o', '--output'):
			outputFile = a
		elif o in ('-h', '--help'):
			helpInfo()
			sys.exit(0)
		else:
			helpInfo()
			sys.exit(1)

	if inputFile == '':
		helpInfo()
		sys.exit(1)
	if outputFile == '':
		outputFile = inputFile+'.txt'

	CSVReader(inputFile,outputFile)


def helpInfo():
	print 'Introduction:'
	print '  Oh, no!'
	print 'Usage:'
	print '  python csvReader.py [options]'
	print 'General Options:'
	print '  -h, --help\t\tShow help.'
	print '  -i, --input\t\tInput file.'
	print '  -o, --output\t\tOutput file.'
	print 'Example:'
	print '  python CSVReader.py -i inputFile -o outputFile'




if __name__ == '__main__':main()