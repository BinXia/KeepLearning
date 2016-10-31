#coding=UTF-8
import os
import numpy as np
from sklearn.metrics import accuracy_score,recall_score,average_precision_score,precision_score,roc_auc_score,f1_score


class CriteriaWriter(object):
	"""
	CriteriaWriter:
		This is a toolkit for recording the result of experiments.

	Input:
		method: the name of method
			Type: str
			Format: 'UserCF'

		parameters: the dictionary of input parameters
			Type: dict
			Format: {'K': 3, 'N': 10}

		result: the dictionary of output criteria
			Type: dict
			Format: {'Recall': 0.8, 'Precision': 0.5, 'Coverage': 1.0}
	"""
	def __init__(self, method, parameters, result):
		super(CriteriaWriter, self).__init__()
		self._method = method
		self._parameters = parameters
		self._result = result

		self._writer()
		
	def round(self,ins,ndigits=3):
		try:
			return '%s'%('%.*f'%(ndigits,ins))
		except:
			return '[%s]'%(','.join(map(lambda x:'%.*f'%(ndigits,x),ins)))

	def _writer(self):
		PATH = os.getcwd()

		if not os.path.isfile(PATH+'/'+'Results'+'/'+self._method+'.cri'):
			File = open(PATH+'/'+'Results'+'/'+self._method+'.cri','w')
			File.write('%s\t%s\n'%(','.join(map(str,self._parameters)),','.join(map(str,self._result))))
			File.close()

		File = open(PATH+'/'+'Results'+'/'+self._method+'.cri','a')
		File.write('%s\t%s\n'%(','.join(map(str,self._parameters.values())),','.join(map(lambda x:self.round(x),self._result.values()))))
		File.close()




class Pred2Criteria(object):
	"""
	Pred2Criteria:
		This is a function to convert a confusion matrix or predict sequence into specific criteria.

	Input:
		problem: the type of problem
			Type: str
			Format: 'Classification', 'Clustering', and 'Regression'

		cMat: the confusion matrix
			Type: np.array or np.mat
			Format: np.array([[1,1,1],[2,2,2],[3,3,3]])

		tpDict: the dictionary of ground truth and predict result
			Type: dict
			Format: {'GroundTruth':[1,2,1,2,0,0,0],'Predict':[2,1,1,2,2,1,0]}

		average: This parameter is required for multiclass/multilabel targets.
			Type: str
			Format: None, 'binary', 'micro', 'macro', 'samples', and 'weighted'
	"""
	def __init__(self,problem='Classification',cMat=[],tpDict=[],average=None):
		super(Pred2Criteria, self).__init__()
		self.criteria = dict()

		if tpDict == []:
			if cMat != []:
				tpDict = self.cMat2tpDict(cMat)


		self.criteriaCalculation(problem,tpDict,average)


	def cMat2tpDict(self,cMat):
		tpDict = {
			'GroundTruth':[],
			'Predict':[]
		}

		for label,class_array in enumerate(cMat):
			tpDict['GroundTruth'].extend([label+1]*int(np.sum(class_array)))
			for index,count in enumerate(class_array):
				if count == 0:
					continue
				tpDict['Predict'].extend([index+1]*int(count))
		
		return tpDict

	def criteriaCalculation(self,problem,tpDict,average):
		y_true = tpDict['GroundTruth']
		y_pred = tpDict['Predict']


		if problem == 'Classification':
			'''
			accuracy_score:
				sklearn method
			url:
				http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score
			'''
			self.criteria['Accuracy'] = accuracy_score(y_true=y_true,y_pred=y_pred)
			'''
			recall_score:
				sklearn method
			url:
				http://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score
			'''
			self.criteria['Recall'] = recall_score(y_true=y_true,y_pred=y_pred,average=average)
			'''
			average_precision_score:
				sklearn method
			url:
				http://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score
			'''
			# self.criteria['Precision_Avg'] = average_precision_score(y_true=y_true,y_score=y_pred)
			'''
			precision_score:
				sklearn method
			url:
				http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics.precision_score
			'''
			self.criteria['Precision'] = precision_score(y_true=y_true,y_pred=y_pred,average=average)
			'''
			roc_auc_score:
				sklearn method
			url:
				http://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score
			'''
			# self.criteria['AUC'] = roc_auc_score(y_true=y_true,y_score=y_pred)
			'''
			f1_score:
				sklearn method
			url:
				http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score
			'''
			self.criteria['F1'] = f1_score(y_true=y_true,y_pred=y_pred,average=average)

		elif problem == 'Clustering':
			pass
		elif problem == 'Regression':
			pass

def main():
	# '''
	# Data
	# '''
	# cMat = np.array([[3,1,1],[2,1,2],[0,1,4]])
	# tpDict = {
	# 	'GroundTruth':[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3],
	# 	'Predict':[1,1,1,2,3,1,1,2,3,3,2,3,3,3,3]
	# }

	# task = Pred2Criteria(cMat=cMat)
	# print task.criteria

	"""
	Data
	"""
	method = 'UserCF'
	parameters = {'K': 3, 'N': 10}
	result = {'Recall': np.array([ 0.6,  0.2,  0.8]), 'F1': np.array([ 0.6       ,  0.25      ,  0.66666667]), 'Precision': np.array([ 0.6       ,  0.33333333,  0.57142857]), 'Accuracy': 0.53333333333333333}

	"""
	Test
	"""
	task = CriteriaWriter(method,parameters,result)


if __name__ == '__main__':main()