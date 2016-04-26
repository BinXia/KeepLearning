import numpy as np
from scipy.sparse import coo_matrix,csr_matrix
import itertools
from sklearn.decomposition import NMF


class MatrixFactorization(object):
	"""
	MatrixFactorization:
		In the mathematical discipline of linear algebra, a matrix decomposition or matrix factorization is a factorization of a matrix into a product of matrices. There are many different matrix decompositions; each finds use among a particular class of problems.
		Non-Negative Matrix Factorization: http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html
	Input:
		mat: user-item matrix
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items
		iteration: the time of iteration
			Type: int
			Format: alpha > 0 (default: 200)
		previous: True if previous items will be recommended
			Type: Boolean
			Format: True, False
	"""
	def __init__(self,mat,iteration=100,previous=True):
		super(MatrixFactorization, self).__init__()
		self._mat = mat.tocsr()
		self._iteration = iteration
		self._previous = previous


	"""
	Function:
		def __Factorize_Self(self,K):
		def __Factorize_NMF(self,K):
		def __RankRec(self,N,user_fmat,item_fmat):
		def Recommend(self,K=2,user=-1,N=1):
	Mission:
		Recommend items to the user based on matrix factorization
	Input:
		K: the number of factors describing each user and item
			Type: int
			Format: <= max(all items, all users)
		user: id of user we will recommend items
			Type: int
			Format: <= all users
		user_fmat: feature (factor) matrix of users
			Type: np.array
			Format: np.shape(user_fmat) = (users, features)
		item_fmat: features (factor) matrix of items
			Type: np.array
			Format: np.shape(item_fmat) = (items, features)
	Output:
		recommendation: the recommendation of each user
			Type: dict
			Format: key==user, value==[(item,score)...]
	"""
	def __Factorize_Self(self,K):
		num_users = self._mat.get_shape()[0]
		num_items = self._mat.get_shape()[1]
		P = np.random.rand(num_users,K)
		Q = np.random.rand(num_items,K)
		Q_T = Q.T

		while self._iteration:
			comb = itertools.product(range(num_users),range(num_items))
			# (stochastic) gradient descent
			for it,(u,i) in enumerate(comb):
				if self._mat[u,i] > 0:
					e_ui = self._mat[u,i] - np.dot(P[u,:],Q_T[:,i])
					for k in xrange(K):
						P[u,k] += self._alpha*(2*e_ui*Q_T[k,i]-self._beta*P[u,k])
						Q_T[k,i] += self._alpha*(2*e_ui*P[u,k]-self._beta*Q_T[k,i])

			# regularization
			
			for it,(u,i) in enumerate(comb):
				if self._mat[u,i] > 0:
					pass

			self._iteration -= 1



	def __Factorize_NMF(self,K):
		model = NMF(n_components=K,max_iter=self._iteration)
		model.fit(self._mat)
		user_fmat = model.fit_transform(self._mat)
		item_fmat = model.components_.T

		return user_fmat,item_fmat

		

	def __RankRec(self,user,user_fmat,item_fmat):
		if self._previous:
			candidate = range(self._mat.get_shape()[1])
		else:
			user_item = list(self._mat.getrow(user).toarray()[0,:])
			candidate = [index for index,i in enumerate(user_item) if i == 0]

		recommendation = [[item,np.dot(user_fmat[user],item_fmat[item].T)] for item in candidate]
		recommendation.sort(key=lambda x:x[1], reverse=True)

		return recommendation


	def Recommend(self,K=2,user=-1):
		user_fmat,item_fmat = self.__Factorize_NMF(K)

		if user == -1:
			recommendation = dict()
			for user in xrange(self._mat.get_shape()[0]):
				recommendation[user] = self.__RankRec(user,user_fmat,item_fmat)
			return recommendation
		else:
			return {user:self.__RankRec(user,user_fmat,item_fmat)}




def test():
	"""
	Data:
		User-item matrix which is conducted by interacting data

		   Item	a 	b 	c 	d
		User
			A 	5 	3 	0 	1
			B 	4 	0 	0 	1
			C 	1 	1 	0 	5
			D 	1 	0 	0 	4
			E 	0 	1 	5 	4
	"""
	User = np.array([0,0,0,1,1,2,2,2,3,3,4,4,4])
	Item = np.array([0,1,3,0,3,0,1,3,0,3,1,2,3])
	Interacting = np.array([5,3,1,4,1,1,1,5,1,4,1,5,4])
	mat = coo_matrix((Interacting,(User,Item)),shape=(5,4))

	"""
	Test
	"""
	task = MatrixFactorization(mat)
	print task.Recommend()



if __name__ == '__main__':test()