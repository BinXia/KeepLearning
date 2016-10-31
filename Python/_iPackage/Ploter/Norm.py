import numpy as np
from scipy.sparse import coo_matrix



class Norm(object):
	"""
	This is a function to normalize the input data for ploter
	"""
	def __init__(self, data, ranges=[0,1], dimension='1D', dtype=np.int64):
		super(Norm, self).__init__()
		self.data = data
		self.ranges = ranges
		self.dimension = dimension
		self.dtype = dtype

		if dimension == '1D':
			pass
		elif dimension == '2D':
			if not (isinstance(data,np.matrixlib.defmatrix.matrix) or isinstance(data,np.ndarray)):
				try:
					self.data = data.toarray()
				except Exception, e:
					print 'Input data must be matrix!'
					return
		else:
			pass
		



	def normalize(self):
		MIN = np.min(self.data)
		MAX = np.max(self.data)
		output = []

		if self.dimension == '1D':
			if self.ranges[0] == 0:
				output = np.array(map(lambda x:float(x-MIN)/(MAX-MIN)*self.ranges[1],self.data))
			elif self.ranges[0] != 0:
				output = np.array(map(lambda x:(float(x-MIN)/(MAX-MIN)+1)*(self.ranges[1]-self.ranges[0]),self.data))
		elif self.dimension == '2D':
			mat = np.zeros(self.data.shape)
			if self.ranges[0] == 0:
				for index,row in enumerate(self.data):
					mat[index] = np.array(map(lambda x:float(x-MIN)/(MAX-MIN)*self.ranges[1],row))
			elif self.ranges[0] != 0:
				for index,row in enumerate(self.data):
					mat[index] = np.array(map(lambda x:(float(x-MIN)/(MAX-MIN)+1)*(self.ranges[1]-self.ranges[0]),row))
			output = mat
		else:
			print 'ha~~~?!'

		return output.astype(self.dtype)


def main():
	"""
	Data:
		User-item matrix which is conducted by interacting data

		   Item	a 	b 	c 	d 	e
		User
			A 	10 	300	0 	20 	0
			B 	150	0 	254	0 	0
			C 	0 	200	0 	0 	10	
			D 	0 	0 	100	300	100
	"""
	User = np.array([0,0,0,1,1,2,2,3,3,3])
	Item = np.array([0,1,3,0,2,1,4,2,3,4])
	Interacting = np.array([10,300,20,150,254,200,10,100,300,100])
	mat = coo_matrix((Interacting,(User,Item)),shape=(4,5))
	# mat = np.vstack((User,Item))
	# mat = User

	"""
	Test
	"""
	task = Norm(data=mat,dimension='2D').normalize()
	print task


if __name__ == '__main__':main()