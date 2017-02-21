import numpy as np
import theano.tensor as T
from theano import function
from theano import In



class Basics(object):
	"""docstring for Basics"""
	def __init__(self):
		super(Basics, self).__init__()
		

	def Algebra(self):
		'''
		byte: bscalar, bvector, bmatrix, brow, bcol, btensor3, btensor4
		16-bit integers: wscalar, wvector, wmatrix, wrow, wcol, wtensor3, wtensor4
		32-bit integers: iscalar, ivector, imatrix, irow, icol, itensor3, itensor4
		64-bit integers: lscalar, lvector, lmatrix, lrow, lcol, ltensor3, ltensor4
		float: fscalar, fvector, fmatrix, frow, fcol, ftensor3, ftensor4
		double: dscalar, dvector, dmatrix, drow, dcol, dtensor3, dtensor4
		complex: cscalar, cvector, cmatrix, crow, ccol, ctensor3, ctensor4
		'''
		x = T.dscalar('x')
		y = T.dscalar('y')
		z = x + y
		f = function([x,y],z)

		print f(2,3)
		print np.allclose(f(16.3, 12.1), 28.4)


	def Logistic(self):

		x = T.dmatrix('x')
		s = 1 / (1 + T.exp(-x))
		logistic = function([x], s)
		print logistic([[0, 1], [-1, -2]])


	def Elementwise(self):
		a, b = T.dmatrices('a', 'b')
		diff = a - b
		abs_diff = abs(diff)
		diff_squared = diff**2
		f = function([a, b], [diff, abs_diff, diff_squared])
		print f([[1, 1], [1, 1]], [[0, 1], [2, 3]])


	def DefaultValue(self):
		x, y = T.dscalars('x', 'y')
		z = x + y
		f = function([x, In(y, value=1)], z)
		print f(33)


	


def main():
	task = Basics()

	'''
	Basics
	'''
	# task.Algebra()
	# task.Logistic()
	# task.Elementwise()
	task.DefaultValue()



if __name__ == '__main__':main()