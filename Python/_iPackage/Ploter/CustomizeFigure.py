import numpy as np
import matplotlib.pyplot as plt




class CustomizeFigure(object):
	"""
	This is a function to customize the personalized figure.
	"""
	def __init__(self, figure, parameters):
		super(CustomizeFigure, self).__init__()
		self._figure = figure
		self._parameters = parameters
		
		figure.show()





def test():
	X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
	C, S = np.cos(X), np.sin(X)

	plt.plot(X, C)
	plt.plot(X, S)
	


	task = CustomizeFigure(plt,parameters=0)

if __name__ == '__main__':test()