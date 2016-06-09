import re
import sys, getopt



class RefToolkits(object):
	"""docstring for RefToolkits"""
	def __init__(self,inputFile,outputFile):
		super(RefToolkits, self).__init__()

		self._reference = list()

		self._patt = re.compile(r"\{(.*)\}")

		self.LoadRef(inputFile)
		self.OutputRef(outputFile)



	def LoadRef(self,inputFile):
		sample = dict()

		with open(inputFile) as datum:
			data = datum.readlines()

		for index,datum in enumerate(data):
			datum = datum.strip()
			if datum == '':
				continue
			
			if datum[0] == '@':
				sample = dict()
			elif datum == '}':
				self._reference.append(sample)
			else:
				datum = re.split('=',datum)
				sample.setdefault(datum[0],self._patt.findall(datum[1])[0])

	def OutputRef(self,outputFile):
		FormatRef = open(outputFile,'w')

		for ref in self._reference:
			# Author
			try:
				FormatRef.write('{0}\t'.format(ref['author']))
			except:
				FormatRef.write(' \t')
			# Title
			try:
				FormatRef.write('{0}\t'.format(ref['title']))
			except:
				FormatRef.write(' \t')
			# Journal or Conference
			if ref.has_key('journal'):
				FormatRef.write('{0}\t'.format(ref['journal']))
			elif ref.has_key('booktitle'):
				FormatRef.write('{0}\t'.format(ref['booktitle']))
			else:
				FormatRef.write(' \t')
				print ref['title']
			# Number & Volume
			if ref.has_key('number') and ref.has_key('volume'):
				FormatRef.write('{0}({1})\t'.format(ref['number'],ref['volume']))
			elif ref.has_key('number'):
				FormatRef.write('{0}\t'.format(ref['number']))
			elif ref.has_key('volume'):
				FormatRef.write('({0})\t'.format(ref['volume']))
			else:
				FormatRef.write(' \t')
			# Year
			try:
				FormatRef.write('{0}\t'.format(ref['year']))
			except:
				FormatRef.write(' \t')
			#Pages
			try:
				FormatRef.write('{0}\t'.format(ref['pages']))
			except:
				FormatRef.write(' \t')

			FormatRef.write('\n')

		FormatRef.close()


def main():
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
		outputFile = inputFile+'.out'

	task = RefToolkits(inputFile,outputFile)


def helpInfo():
	print 'Introduction:'
	print '  This is a toolkit for transforming references to specific format.'
	print 'Usage:'
	print '  python ReferenceAssistant.py [options]'
	print 'General Options:'
	print '  -h, --help\t\tShow help.'
	print '  -i, --input\t\tInput file.'
	print '  -o, --output\t\tName of output file.'
	print 'Example:'
	print '  python ReferenceAssistant.py -i inputFile -o outputFile'
	 

if __name__ == '__main__':	main()














