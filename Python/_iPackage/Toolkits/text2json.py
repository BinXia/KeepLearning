import re
import json
import sys, getopt
import codecs


class text2json(object):
	"""docstring for text2json"""
	def __init__(self,inputFile,outputFile):
		super(text2json, self).__init__()

		self.text2json(inputFile,outputFile)


	def text2json(self,inputFile,outputFile):
		previousDepth = 0
		father = []
		p = re.compile('\t')

		
		for datum in open(inputFile).readlines():
			currentDepth = len(p.findall(datum))
			datum = datum.strip()


			previousDepth = self.InformationSecurityWeb(father,datum,previousDepth,currentDepth)

		FormatRef = open(outputFile,'w')
		# FormatRef = codecs.open(outputFile, "w", "utf-8")
		FormatRef.write(json.dumps(father[0]))
		FormatRef.close()


	def InformationSecurityWeb(self,father,datum,previousDepth,currentDepth):
		# append node
		node = 	{"name":datum,"children":[]}
		if currentDepth == previousDepth and currentDepth != 0:
			father[previousDepth-1]["children"].append(node)
		elif currentDepth > previousDepth:
			father[previousDepth]["children"].append(node)
		elif currentDepth < previousDepth:
			father[currentDepth-1]["children"].append(node)

		# update stack
		if len(father) == currentDepth:
			father.append(node)
		else:
			father[currentDepth] = node

		return currentDepth




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
		outputFile = inputFile+'.txt'

	text2json(inputFile,outputFile)


def helpInfo():
	print 'Introduction:'
	print '  This is a toolkit for transforming indent file to json format.'
	print 'Usage:'
	print '  python text2json.py [options]'
	print 'General Options:'
	print '  -h, --help\t\tShow help.'
	print '  -i, --input\t\tInput file.'
	print '  -o, --output\t\tName of output file.'
	print 'Example:'
	print '  python text2json.py -i inputFile -o outputFile'






if __name__ == "__main__":main()