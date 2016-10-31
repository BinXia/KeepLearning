#coding=UTF-8
import os
import numpy as np



class CrossValidation(object):
	"""
	CrossValidation:
		This is a toolkit to prepare the cross dataset for validating the algorithms.

	Input:
		data: the sequence of data
			Type: list
			Format: [
						[1,9,0],
						[2,9,1],
						[3,9,1],
						[4,9,0],
						[5,9,1],
						[6,9,0],
						[7,9,1],
						[8,9,0],
						[9,9,0],
						[10,9,1],
					]

		fold: the fold of dataset
			Type: int
			Format: 5

		dataset: the crossed dataset of original dataset
			Type: list + dict
			Format: [
						{'test': [[1, 9, 0], [2, 9, 1], [3, 9, 1]], 'train': [[4, 9, 0], [5, 9, 1], [6, 9, 0], [7, 9, 1], [8, 9, 0], [9, 9, 0], [10, 9, 1]]}, 
						{'test': [[4, 9, 0], [5, 9, 1], [6, 9, 0]], 'train': [[1, 9, 0], [2, 9, 1], [3, 9, 1], [7, 9, 1], [8, 9, 0], [9, 9, 0], [10, 9, 1]]}, 
						{'test': [[7, 9, 1], [8, 9, 0], [9, 9, 0], [10, 9, 1]], 'train': [[1, 9, 0], [2, 9, 1], [3, 9, 1], [4, 9, 0], [5, 9, 1], [6, 9, 0]]}
					]

	"""
	def __init__(self, data, fold):
		super(CrossValidation, self).__init__()

		self.dataset = self.CrossData(data,fold)

	def CrossData(self,data,fold):
		dataset = list()

		if fold == 0:
			data_cross = {'train':data,'test':[]}
			dataset.append(data_cross)
			return dataset

		per = len(data)/fold
		for index in xrange(fold):
			data_cross = {'train':[],'test':[]}
			index = index * per
			
			if index == 0:
				data_cross['test'] = data[index:index+per]
				data_cross['train'].extend(data[index+per:])
			elif index == (fold-1)*per:
				data_cross['test'] = data[index:]
				data_cross['train'].extend(data[:index])
			else:
				data_cross['test'] = data[index:index+per]
				data_cross['train'].extend(data[:index])
				data_cross['train'].extend(data[index+per:])

			dataset.append(data_cross)

		return dataset


class Normalization(object):
	"""
	CrossValidation:
		This is a toolkit to prepare the cross dataset for validating the algorithms.

	Input:
		data: the sequence of data
			Type: np.array
			Format: [
						[1,9,0],
						[2,9,1],
						[3,9,1],
						[4,9,0],
						[5,9,1],
						[6,9,0],
						[7,9,1],
						[8,9,0],
						[9,9,0],
						[10,9,1],
					]

		dimension: the dimension of the data
			Type: int
			Format: 2

		axis: the selection of normalized row or col
			Type: 0(row) or 1(col)
			Format: 1

		RANGE: the range of normalization
			Type: list
			Format: [0,1]

	"""
	def __init__(self, data, dimension, axis, RANGE=[0,1]):
		super(Normalization, self).__init__()
		
		self.normData = self.norm(data,dimension,axis,RANGE)

	def norm(self,data,dimension,axis,RANGE):
		if len(np.shape(data)) != dimension:
			raise IOError('The dimension of data is not equal to the input dimension!')

		if axis == 0:
			pass
		elif axis == 1:
			data = data.T
		else:
			raise IOError('Error input of axis!')

		mat = list()
		if dimension == 1:
			MAX = np.max(data)
			MIN = np.min(data)
			if MAX == MIN:
				mat.append(np.array([(RANGE[0]+RANGE[1])/2.0]*len(data)))
			else:
				temp = np.zeros(len(data))
				for i,e in enumerate(data):
					temp[i] = 1.0*(e-MIN)/(MAX-MIN)
				mat.append(temp)
		else:
			for row in data:
				MAX = np.max(row)
				MIN = np.min(row)
				if MAX == MIN:
					mat.append(np.array([(RANGE[0]+RANGE[1])/2.0]*len(row)))
					continue
				else:
					temp = np.zeros(len(row))
					for i,e in enumerate(row):
						temp[i] = 1.0*(e-MIN)/(MAX-MIN)
					mat.append(temp)

		if axis == 0:
			return np.array(mat)
		elif axis == 1:
			return np.array(mat).T		



def main():
	data = [
		[1,9,0],
		[2,9,1],
		[3,9,1],
		[4,9,0],
		[5,9,1],
		[6,9,0],
		[7,9,1],
		[8,9,0],
		[9,9,0],
		[10,9,1],
	]
	fold = 0

	# task = CrossValidation(data=data,fold=fold)
	# print task.dataset

	task = Normalization(data=np.array(data[0]),dimension=1,axis=0)
	print task.normData

if __name__ == '__main__':main()