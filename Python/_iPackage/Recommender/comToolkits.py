#coding=utf-8
from scipy.sparse import coo_matrix
import numpy as np



"""
insGenerator:
	This is a generator to yield each instance from long long files.

Input:
	insFILE: the location of file
		Type: str
		Format: './test'

	num: the number of instances for reading
		Type: int
		Format: 10
"""
def insGenerator(insFILE,num):
	iteration = 0
	FILE = open(insFILE)
	while iteration < num:
		iteration += 1
		line = FILE.readline()
		if line == '':
			break
		else:
			yield line.strip().split('\t')


"""
writeUserItemMat:
	This is a toolkit to save user-item matrix in coo_matrix format.

Input:
	FILE: the name of saving file
		Type: str
		Format: 'UserCF'

	UserArray: the coordinates of users (commonly ROW)
		Type: np.array
		Format: np.array([0,0,0,1,1,1,2,2,3,3,3,4,4])

	ItemArray: the coordinates of items (commonly COL)
		Type: np.array
		Format: np.array([0,1,3,1,2,4,2,3,1,2,3,0,3])

	RecordArray: the value of specific coordinate (commonly VALUE)
		Type: np.array
		Format: np.array([1]*13)
"""
def writeUserItemMat(FILE,UserArray,ItemArray,RecordArray):
	matFile = open(FILE,'w')
	matFile.write('User:\n')
	for user in UserArray:
		matFile.write('{0}\t'.format(user))
	matFile.write('\n')
	matFile.write('Item:\n')
	for item in ItemArray:
		matFile.write('{0}\t'.format(item))
	matFile.write('\n')
	matFile.write('Record:\n')
	for record in RecordArray:
		matFile.write('{0}\t'.format(record))
	matFile.close()


"""
readUserItemMat:
	This is a toolkit to read user-item matrix in coo_matrix format created by Function writeUserItemMat().

Input:
	FILE: the name of saving file
		Type: str
		Format: 'UserCF'

	matShape: the shape of generating matrix
		Type: tuple
		Format: (5,5)
"""
def readUserItemMat(FILE,matShape):
	# init
	mode = 'Ready'
	UserArray = list()
	ItemArray = list()
	RecordArray = list()

	# open restored mat info
	with open(FILE) as datum:
		data = datum.readlines()

	for index,datum in enumerate(data):
		datum = datum.strip().split('\t')

		if mode == 'Ready':
			if datum[0] == 'User:':
				mode = 'User'
				continue
			elif datum[0] == 'Item:':
				mode = 'Item'
				continue
			elif datum[0] == 'Record:':
				mode = 'Record'
				continue
		else:
			if mode == 'User':
				UserArray = np.array(map(int,datum))
				mode = 'Ready'
				continue
			elif mode == 'Item':
				ItemArray = np.array(map(int,datum))
				mode = 'Ready'
				continue
			elif mode == 'Record':
				RecordArray = np.array(map(int,datum))
				mode = 'Ready'
				continue

	return coo_matrix((RecordArray,(UserArray,ItemArray)),shape=matShape)