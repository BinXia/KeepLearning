#coding=UTF-8
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix
import itertools
import math


class ItemCF(object):
	"""
	ItemCF:
		Item-item collaborative filtering was first described in the literature by Sarwar et al. and Karypis, although a version of it seems to have been used by Amazon.com at this time. Rather than using similarities between users' rating behavior to predict preferences, item-item CF uses similarities between the rating patterns of items. If two items tend to have the same users like and dislike them, then they are similar and users are expected to have similar preferences for similar items. In its overall structure, therefore, this method is similar to earlier content-based approaches to recommendation and personalization, but item similarity is deduced from user preference patterns rather than extracted from item data.
	Input:

	"""
	def __init__(self,mat,previous=True):
		super(ItemCF, self).__init__()
		self._mat = mat.tocsr()
		self._previous = previous
		
		self._ItemSimilarity()




	"""
	Function:
		def _ItemSimilarity(self,s_method='Cosine'):
	Mission:
		1. Build the inverse table for user-item (decrease time complexity);
			*** If user u likes both item A and B, then I_AB = 1, otherwise, I_AB = 0.
				In process of calculating item similarity, we just calculate ones I_XY = 1.
		2. Calculate item similarity based on the inverse table.
			***	'Jaccard' for Jaccard equation
				'Cosine' for Cosine similarity
	Input:
		s_method: strategy of calculating user similarity
			Type: str
			Format: 'Jaccard' for Jaccard equation
					'Cosine' for Cosine similarity
	Output:
		self._sim_mat: item-item similarity matrix
	"""
	def _ItemSimilarity(self,s_method='Cosine'):
		"""
		1. Build the inverse table for user-item (decrease time complexity);
		"""
		inverseTabel = dict()
		item_user = np.array(self._mat.sum(axis=0))[0,:]

		for user in xrange(self._mat.get_shape()[0]):
			comb = itertools.combinations(self._mat.getrow(user).indices,2)
			for n,(i,j) in enumerate(comb):
				inverseTabel.setdefault((i,j),0)
				inverseTabel[(i,j)] += 1
				inverseTabel.setdefault((j,i),0)
				inverseTabel[(j,i)] += 1
			

		"""
		2. Calculate item similarity based on the inverse table.
		"""
		X = list()
		Y = list()
		similarity = list()

		for item_pair,value in inverseTabel.items():
			X.append(item_pair[0])
			Y.append(item_pair[1])
			similarity.append(1.0 * value / math.sqrt(item_user[X[-1]]*item_user[Y[-1]]))

		self._sim_mat = csr_matrix((similarity,(X,Y)),shape=(self._mat.get_shape()[1],self._mat.get_shape()[1]))



	"""
	Function:
		def __CalAndRankRec(self,K,user,N):
		def Recommend(self,K=3,user=-1,N=1):
	Mission:
		Recommend items to the user based on K similar items
	Input:
		K: the number of selected similar items
			Type: int
			Format: <= all items - 1
		user: id of user we will recommend items
			Type: int
			Format: <= all users
	Output:
		recommendation: the recommendation of each user
			Type: dict
			Format: key==user, value==[(item,score)...]
	"""
	def __CalAndRankRec(self,K,user):
		# order similar items
		sim_item = dict()
		for item in self._mat.getrow(user).indices:
			another_items = self._sim_mat.getrow(item).indices
			another_items_score = self._sim_mat.getrow(item).data
			comb = [[another_items[index],another_items_score[index]] for index in xrange(len(another_items))]
			comb.sort(key=lambda x:x[1],reverse=True)
			try:
				sim_item[item] = comb[:K]
			except:
				raise 'Similar items are less than selected K(%d) for item(%d)!'%(K,item)

		# calculate and order recommender score
		if self._previous:
			candidate = set(range(self._mat.get_shape()[1]))
		else:
			user_item = list(self._mat.getrow(user).toarray()[0,:])
			candidate = set([index for index,i in enumerate(user_item) if i == 0])
		recommendation = dict()
		for item,another_items in sim_item.items():
			interesting = self._mat[user,item]
			for another_item,score in another_items:
				if candidate.intersection(set([another_item])):
					recommendation.setdefault(another_item,0)
					recommendation[another_item] += score * interesting
			
		recommendation = [[key,value] for key,value in recommendation.items()]
		recommendation.sort(key=lambda x:x[1], reverse=True)
		
		return recommendation


	def Recommend(self,K=2,user=-1):
		if user == -1:
			recommendation = dict()
			for user in xrange(self._mat.get_shape()[0]):
				recommendation[user] = self.__CalAndRankRec(K,user)
			return recommendation
		else:
			return {user:self.__CalAndRankRec(K,user)}





def test():
	"""
	Data:
		User-item matrix which is conducted by interacting data

		   Item	a 	b 	c 	d 	e
		User
			A 	1 	1 	0 	1 	0
			B 	0 	1 	1 	0 	1
			C 	0 	0 	1 	1 	0	
			D 	0 	1 	1 	1 	0
			E 	1 	0 	0 	1 	0
	"""
	User = np.array([0,0,0,1,1,1,2,2,3,3,3,4,4])
	Item = np.array([0,1,3,1,2,4,2,3,1,2,3,0,3])
	Interacting = np.array([1]*13)
	mat = coo_matrix((Interacting,(User,Item)),shape=(5,5))


	"""
	Test
	"""
	task = ItemCF(mat)
	print task.Recommend()


if __name__ == '__main__':test()