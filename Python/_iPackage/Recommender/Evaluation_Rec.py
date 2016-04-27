#coding=UTF-8
import numpy as np
from scipy.sparse import coo_matrix




class Evaluation_Rec(object):
	"""
	Evaluation_Rec:
		This is the function used to evaluate the strategies of recommender
	Input:
		mat_train: user-item matrix of users' behaviors in the past
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items
		mat_behavior: user-item matrix of users' behaviors
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items
		recommendation: recommendations
			Type: dict
			Format: key==user, value==[(item,score)...]
		N: the number of recommendations
			Type: int
			Format: < all items
		criteria: set of criteria
			Type: set
			Format: ('Recall','Precision','Coverage','Popularity')
	"""
	def __init__(self,mat_train,mat_behavior,recommendation,N,criteria):
		super(Evaluation_Rec, self).__init__()
		self._mat_train = mat_train.tocsr()
		self._mat_behavior = mat_behavior.tocsr()
		self._recommendation = recommendation
		self._N = N
		self._criteria = criteria

		self._result = self._Evaluation()


	"""
	Function:
		def _Evaluation(self):
	Mission:
		Integrated function for all the criteria
	Input:
		None
	Output:
		criteria: the dict of criteria for evaluation
			Type: dict
			Format: 
	"""	
	def _Evaluation(self):
		"""
		1. Initialize and prepare important parameters
		"""
		# RecSet: R(u) Recommendation set of users
		RecSet = dict()
		demand_cri = set(['Recall','Precision','Coverage','Popularity'])
		if demand_cri.intersection(self._criteria):
			for user in self._recommendation.keys():
				RecSet[user] = set(map(lambda x:x[0],self._recommendation[user][:self._N]))
		# print RecSet

		# BehSet: B(u) Behavior set of users
		BehSet = dict()
		demand_cri = set(['Recall','Precision'])
		if demand_cri.intersection(self._criteria):
			for user in xrange(self._mat_behavior.get_shape()[0]):
				BehSet[user] = set(self._mat_behavior.getrow(user).indices)
		# print BehSet

		# AllItem: |I| number of all items
		AllItem = 0
		demand_cri = set(['Coverage','Coverage_Gini'])
		if demand_cri.intersection(self._criteria):
			AllItem = self._mat_behavior.get_shape()[1]
		# print AllItem

		# item_count: C(l) the number of purchase records of items
		item_count = dict()
		demand_cri = set(['Popularity'])
		if demand_cri.intersection(self._criteria):
			for user in xrange(self._mat_train.get_shape()[0]):
				item_count[user] = {item:self._mat_train.getrow(user).data[index] for index,item in enumerate(self._mat_train.getrow(user).indices)}
		# print item_count

		"""
		2. Calculate selected criteria
		"""
		criteria = dict()

		if 'Recall' in self._criteria:
			criteria['Recall'] = self.__Recall(RecSet,BehSet)
		
		if 'Precision' in self._criteria:
			criteria['Precision'] = self.__Precision(RecSet,BehSet)

		if 'Coverage' in self._criteria:
			criteria['Coverage'] = self.__Coverage(RecSet,AllItem)

		if 'Coverage_Gini' in self._criteria:
			criteria['Coverage_Gini'] = self.__Coverage_Gini(RecSet,AllItem)

		if 'Popularity' in self._criteria:
			criteria['Popularity'] = self.__Popularity(RecSet,item_count)


		return criteria

	"""
	Recall = \frac{\sum_{u\in U}|RecSet[u]\cap BehSet[u]|}{\sum_{u\in U}|BehSet[u]|}
	"""
	def __Recall(self,RecSet,BehSet):
		Sum_intersection = 0
		Sum_behavior = 0
		for user in RecSet.keys():
			Sum_intersection += len(RecSet[user].intersection(BehSet[user]))
			Sum_behavior += len(BehSet[user])
		return '%5.3f'%(1.0*Sum_intersection/Sum_behavior)

	"""
	Precision = \frac{\sum_{u\in U}|RecSet[u]\cap BehSet[u]|}{\sum_{u\in U}|RecSet[u]|}
	"""
	def __Precision(self,RecSet,BehSet):
		Sum_intersection = 0
		Sum_recommendation = 0
		for user in RecSet.keys():
			Sum_intersection += len(RecSet[user].intersection(BehSet[user]))
			Sum_recommendation += len(RecSet[user])
		return '%5.3f'%(1.0*Sum_intersection/Sum_recommendation)

	"""
	Coverage = \frac{|\bigcup_{u\in U}RecSet[u]|}{|I|}
	"""
	def __Coverage(self,RecSet,AllItem):
		Sum_set = set()
		for user in RecSet.keys():
			Sum_set = Sum_set.union(RecSet[user])
		return '%5.3f'%(1.0*len(Sum_set)/AllItem)

	"""
	Coverage_Gini = \frac{1}{n-1}\sum^{n}_{i=1}(2j-n-1)p(l_i)
	"""
	def __Coverage_Gini(self,RecSet,AllItem):
		G = 0.0
		ItemList = np.zeros(AllItem)
		for user in RecSet.keys():
			for location in RecSet[user]:
				ItemList[location] += 1
		ItemListOrder = sorted([[index,score] for index,score in enumerate(ItemList)], key=lambda x:x[1])
		for i,[item,score] in enumerate(ItemListOrder):
			G += (2*(i+1)-AllItem-1)*(1.0*score/len(RecSet))
		return 1.0*G/(AllItem-1)
	"""
	Popularity = 
	"""
	def __Popularity(self,RecSet,item_count):
		pass


def test():
	"""
	Data:
		User-item matrix which is conducted by interacting data
		mat_train:
			   Item	a 	b 	c 	d 	e
			User
				A 	1 	1 	0 	1 	0
				B 	1 	0 	1 	0 	0
				C 	0 	1 	0 	0 	1
				D 	0 	0 	1 	1 	1
		mat_behavior:
			   Item	a 	b 	c 	d 	e
			User
				A 	0 	0 	1 	0 	1
				B 	0 	0 	0 	1 	0
				C 	0 	0 	1 	0 	0
				D 	0 	1 	0 	0 	0

	Recommendation:
		Format: key==user, value==[(item,score)...]
		{
			0: [(2, 0.74158162379719639), (4, 0.74158162379719639)], 
			1: [(3, 0.81649658092772615), (1, 0.40824829046386307)], 
			2: [(3, 0.81649658092772615), (0, 0.40824829046386307)], 
			3: [(0, 0.74158162379719639), (1, 0.74158162379719639)]
		}

	"""
	User = np.array([0,0,0,1,1,2,2,3,3,3])
	Item = np.array([0,1,3,0,2,1,4,2,3,4])
	Interacting = np.array([1]*10)
	mat_train = coo_matrix((Interacting,(User,Item)),shape=(4,5))

	User = np.array([0,0,1,2,3])
	Item = np.array([2,4,3,2,1])
	Interacting = np.array([1]*5)
	mat_behavior = coo_matrix((Interacting,(User,Item)),shape=(4,5))

	N = 1

	recommendation = {
		0: [(2, 0.74158162379719639), (4, 0.74158162379719639)], 
		1: [(3, 0.81649658092772615), (1, 0.40824829046386307)], 
		2: [(3, 0.81649658092772615), (0, 0.40824829046386307)], 
		3: [(0, 0.74158162379719639), (1, 0.74158162379719639)]
	}
	criteria = set(['Recall','Precision','Coverage','Coverage_Gini'])

	"""
	Test
	"""
	task = Evaluation_Rec(mat_train,mat_behavior,recommendation,N,criteria)
	print task._result


if __name__ == '__main__':test()