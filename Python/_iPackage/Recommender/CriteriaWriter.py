#coding=UTF-8
import os
import numpy as np


class CriteriaWriter(object):
	"""
	CriteriaWriter:
		This is a toolkit for recording the result of experiments.
	"""
	def __init__(self, recommender, parameters, result):
		super(CriteriaWriter, self).__init__()
		self._recommender = recommender
		self._parameters = parameters
		self._result = result

		self._writer()
		

	def _writer(self):
		PATH = os.getcwd()

		if not os.path.isfile(PATH+'/'+self._recommender+'.cri'):
			File = open(PATH+'/'+self._recommender+'.cri','w')
			File.write('%s\t%s\n'%(','.join(map(str,self._parameters)),','.join(map(str,self._result))))
			File.close()

		File = open(PATH+'/'+self._recommender+'.cri','a')
		File.write('%s\t%s\n'%(','.join(map(str,self._parameters.values())),','.join(map(str,self._result.values()))))
		File.close()
		


def test():
	"""
	Data
	"""
	recommender = 'UserCF'
	parameters = {'K': 3, 'N': 10}
	result = {'Recall': 0.8, 'Precision': 0.5, 'Coverage': 1.0}

	"""
	Test
	"""
	task = CriteriaWriter(recommender,parameters,result)


if __name__ == '__main__':test()