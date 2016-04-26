#coding=UTF-8
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix
import itertools
import math

class UserCF(object):
	"""
	UserCF:
		User–user CF is a straightforward algorithmic interpretation of the core premise of collaborative filtering: find other users whose past rating behavior is similar to that of the current user and use their ratings on other items to predict what the current user will like. To predict Mary’s preference for an item she has not rated, user–user CF looks for other users who have high agreement with Mary on the items they have both rated. These users’ ratings for the item in question are then weighted by their level of agreement with Mary’s ratings to predict Mary’s preference.
	Input:
		mat: user-item matrix
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items
	"""
	def __init__(self,mat,previous=True):
		super(UserCF, self).__init__()
		self._mat = mat.tocsr()
		self._previous = previous

		self._UserSimilarity()




	"""
	Function:
		def _UserSimilarity(self,s_method='Cosine'):
	Mission:
		1. Build the inverse table for user-item (decrease time complexity);
			*** If user A and B has co-rating-behavior item, then I_AB = 1, otherwise, I_AB = 0.
				In process of calculating user similarity, we just calculate ones I_XY = 1.
		2. Calculate user similarity based on co-rating-behavior items.
			***	'Jaccard' for Jaccard equation
				'Cosine' for Cosine similarity
	Input:
		s_method: strategy of calculating user similarity
			Type: str
			Format: 'Jaccard' for Jaccard equation
					'Cosine' for Cosine similarity
	Output:
		self._sim_mat: user-user similarity matrix
	"""
	def _UserSimilarity(self,s_method='Cosine'):
		"""
		1. Build the inverse table for user-item (decrease time complexity);
		"""
		X = list()
		Y = list()
		intersection = dict()

		comb = itertools.combinations(xrange(self._mat.get_shape()[0]),2)
		for n,(i,j) in enumerate(comb):
			set_i = set(self._mat.getrow(i).indices)
			set_j = set(self._mat.getrow(j).indices)
			if set_i.intersection(set_j):
				intersection[(i,j)] = set_i.intersection(set_j)
				X.append(i)
				Y.append(j)

		"""
		2. Calculate user similarity based on co-rating-behavior items.
		"""
		similarity = list()
		for index in xrange(len(X)):
			if s_method == 'Cosine':
				u_i = X[index]
				u_j = Y[index]
				N_ui = len(self._mat.getrow(X[index]).indices)
				N_uj = len(self._mat.getrow(Y[index]).indices)
				similarity.append(1.0 * len(intersection[(u_i,u_j)]) / math.sqrt(N_ui*N_uj))
		
		self._sim_mat = csr_matrix((similarity,(X,Y)),shape=(self._mat.get_shape()[0],self._mat.get_shape()[0]))
		self._sim_mat = self._sim_mat + self._sim_mat.transpose()

	"""
	Function:
		def __CalAndRankRec(self,K,user,N):
		def Recommend(self,K=3,user=-1,N=1):
	Mission:
		Recommend items to the user based on K similar users
	Input:
		K: the number of selected similar users
			Type: int
			Format: <= all users - 1
		user: id of user we will recommend items
			Type: int
			Format: <= all users
	Output:
		recommendation: the recommendation of each user
			Type: dict
			Format: key==user, value==[(item,score)...]
	"""
	def __CalAndRankRec(self,K,user):
		# order similar users
		sim_user = list()
		for another_user in self._sim_mat.getrow(user).indices:
			sim_user.append((another_user,self._sim_mat[user,another_user]))
		sim_user.sort(key=lambda x:x[1],reverse=True)

		# calculate and order recommender score
		if self._previous:
			candidate = range(self._mat.get_shape()[1])
		else:
			user_item = list(self._mat.getrow(user).toarray()[0,:])
			candidate = [index for index,i in enumerate(user_item) if i == 0]

		try:
			sim_user = sim_user[:K]
		except:
			raise 'Similar users are less than selected K(%d)!'%K
		recommendation = list()
		for item in candidate:
			score = 0
			for another_user,sim_score in sim_user:
				try:
					# score(user,item) = \sum_{v\in sim_user(user,K)\cap N(item)}w_{uv}*r_{vi}
					score += self._mat[another_user,item]*sim_score
				except:
					pass
			recommendation.append((item,score))
		recommendation.sort(key=lambda x:x[1], reverse=True)
		
		return recommendation


	def Recommend(self,K=3,user=-1):
		if user == -1:
			recommendation = dict()
			for user in xrange(self._sim_mat.get_shape()[0]):
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
	task = UserCF(mat)

	print task.Recommend()



if __name__ == '__main__':test()