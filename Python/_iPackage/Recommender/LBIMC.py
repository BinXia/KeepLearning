import numpy as np
from scipy.sparse import coo_matrix,csr_matrix


class LBIMC(object):
	"""
	LBIMC:
		\underline{L}inearized \underline{B}regman \underline{I}teration for \underline{M}atrix \underline{C}ompletion(LBIMC)
		Inspired by compressed sensing~\cite{donoho2006compressed}, based on the incomplete signal with noise information (i.e., sparse check-in data with fake records), we tend to recovery the original signal (i.e., complete the matrix for recommendation) using Bregman iteration algorithm.
	Input:
		mat: user-item matrix
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items
		iteration: the time of iteration
			Type: int
			Format: alpha > 0 (default: -1)
		previous: True if previous items will be recommended
			Type: Boolean
			Format: True, False
		Lambda: Balance the structural noise and the rank of matrix
			Type: float
			Format: 0 < Lambda < 1 (default: 0.5)
		Mu: Balance \mu (\left \| X\right \|_*+\lambda \left \| Z \right \|_{2,1}) and \frac{1}{2}\left \| P_\Omega(R-X-Z)\right \|_F^2.
			Type: float
			Format: 500 < Mu < 2000 (default: 1000)
		Delta: Control the coverage of LBIMC
			Type: float
			Format: 0 < Delta < 2 (default: 1)
	"""
	def __init__(self,mat,iteration=-1,previous=True,Lambda=0.5,Mu=1000,Delta=1):
		super(LBIMC, self).__init__()
		self._mat = mat.tocsr()
		self._iteration = iteration
		self._previous = previous
		
		self._Lambda = Lambda
		self._Mu = Mu
		self._Delta = Delta


	"""
	Function:
		def _LBIMC(self):
		def __RankRec(self,N):
		def Recommend(self,user=-1,N=1):
	Mission:
		Recommend items to the user based on matrix factorization
	Input:
		user: id of user we will recommend items
			Type: int
			Format: <= all users
		RecMat: the completed matrix for recommendation
			Type: numpy.matrixlib.defmatrix.matrix
			Format RecMat.shape == (users,items)
	Output:
		recommendation: the recommendation of each user
			Type: dict
			Format: key==user, value==[(item,score)...]
	"""
	def __RankRec(self,user,RecMat):
		if self._previous:
			candidate = range(self._mat.get_shape()[1])
		else:
			user_item = list(self._mat.getrow(user).toarray()[0,:])
			candidate = [index for index,i in enumerate(user_item) if i == 0]

		recommendation = [[item, RecMat[user,item]]  for item in candidate]
		recommendation.sort(key=lambda x:x[1], reverse=True)

		return recommendation



	def _LBIMC(self,P_omega,Lambda,Mu,Delta):
		# initialization
		users = P_omega.get_shape()[0]
		items = P_omega.get_shape()[1]
		X = csr_matrix((users,items))
		Z = csr_matrix((users,items)).todense()
		V = csr_matrix((users,items))
		U = csr_matrix((users,items))

		for iteration in xrange(self._iteration):
			V = V + Delta*(P_omega-X-Z)
			(U1,s,V1) = np.linalg.svd(V)
			s = map(lambda x:max(x-Mu*Delta,0),s)
			if V1.shape[0]>U1.shape[0]:
				X = U1*np.hstack((np.diag(s),np.zeros((U1.shape[0],V1.shape[0]-U1.shape[0]))))*V1
			elif U1.shape[0]>V1.shape[0]:
				X = U1*np.vstack((np.diag(s),np.zeros((U1.shape[0]-V1.shape[0],V1.shape[0]))))*V1
			else:
				X = U1*np.diag(s)*V1
			U = U + Delta*(P_omega-X-Z)
			for row in xrange(users):
				if ~U[row].any():	# 0-matrix
					Z[row] = max(np.linalg.norm(U[row],ord=2)-Mu*Lambda*Delta,0)*U[row]
				else:
					Z[row] = max(np.linalg.norm(U[row],ord=2)-Mu*Lambda*Delta,0)*(U[row]/np.linalg.norm(U[row],ord=2))
			# print 'Iteration {0} is completed.'.format(iteration+1)

		return X+Z



	def Recommend(self,user=-1):
		RecMat = self._LBIMC(self._mat,self._Lambda,self._Mu,self._Delta)

		if user == -1:
			recommendation = dict()
			for user in xrange(self._mat.get_shape()[0]):
				recommendation[user] = self.__RankRec(user,RecMat)
			return recommendation
		else:
			return {user:self.__RankRec(user,RecMat)}





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
	task = LBIMC(mat=mat,iteration=100,Lambda=0.5,Mu=1000,Delta=1)
	print task.Recommend()



if __name__ == '__main__':test()