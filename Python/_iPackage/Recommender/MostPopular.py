#coding=UTF-8
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix


class MostPopular(object):
	"""
	MostPopular:
		The strategy which recommends the most popular location based on the check-in data collected from each user.
	Input:
		mat: user-item matrix
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items
	"""
	def __init__(self,mat,previous=True):
		super(MostPopular, self).__init__()
		self._mat = mat
		self._previous = previous




	"""
	Function:
		def __CalAndRankPopular(self,N):
		def Recommend(self,user=-1,N=1):
	Mission:
		Recommend items to the user based on matrix factorization
	Input:
		user: id of user we will recommend items
			Type: int
			Format: <= all users
	Output:
		recommendation: the recommendation of each user
			Type: dict
			Format: key==user, value==[(item,score)...]
	"""
	def __CalAndRankPopular(self):
		recommendation = [[index,score] for index,score in enumerate(np.array(self._mat.sum(axis=0))[0,:])]
		recommendation.sort(key=lambda x:x[1], reverse=True)

		return recommendation


	def Recommend(self,user=-1):
		PopList = self.__CalAndRankPopular()

		if user == -1:
			recommendation = dict()
			for user in xrange(self._mat.get_shape()[0]):
				recommendation[user] = PopList
			return recommendation
		else:
			return {user:PopList}







def test():
	"""
	Data:
		User-item matrix which is conducted by interacting data

		   Item	a 	b 	c 	d 	e
		User
			A 	1 	1 	0 	1 	0
			B 	1 	0 	1 	0 	0
			C 	0 	1 	0 	0 	1	
			D 	0 	0 	1 	1 	1
	"""
	User = np.array([0,0,0,1,1,2,2,3,3,3])
	Item = np.array([0,1,3,0,2,1,4,2,3,4])
	Interacting = np.array([1]*10)
	mat = coo_matrix((Interacting,(User,Item)),shape=(4,5))

	"""
	Test
	"""
	task = MostPopular(mat)
	print task.Recommend()






if __name__ == '__main__':test()