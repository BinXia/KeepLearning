import numpy as np
import matplotlib.pyplot as plt




class CustomizeFigure(object):
	"""
	This is a function to customize the personalized figure.
	"""
	def __init__(self, figure, parameters={}):
		super(CustomizeFigure, self).__init__()
		self._figure = figure
		self._parameters = {
			'xlim': None,
				# the limit of axis x. Format: (-5,5); Type: float
			'ylim': None,
				# the limit of axis y. Format: (-5,5); Type: float
			'figheight': 6,
				# the height of figure. Format: 6; Type: float
			'figwidth': 8,
				# the width of figure. Format: 8; Type: float
			'title': None,
				# the title of figure. Format: 'Title'; Type: str
			'xlabel': None,
				# the label of axis x. Format: 'xlabel'; Type: str
			'ylabel': None,
				# the label of axis y. Format: 'ylabel'; Type: str
			'legend': None,
				# the legend of figure. Format: 
			'labelweight': 'bold',
				# bold label for axis label and tick. Format: ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']; Type: str
			'labelsize': 12,
				# font size of xlabel and ylabel. Format: 12; Type: int
			'ticksize': 12,
				# font size of xtick and ytick. Format: 12; Type: int
		}

		# load input parameters
		for key,value in parameters.items():
			self._parameters[key] = value

		self.__decorateFigure()

		
	def __decorateFigure(self):
		if self._parameters['title'] != None:
			self._figure.title(self._parameters['title'])

		if self._parameters['figheight'] != None:
			self._figure.gcf().set_figheight(self._parameters['figheight'])

		if self._parameters['figwidth'] != None:
			self._figure.gcf().set_figwidth(self._parameters['figwidth'])

		if self._parameters['xlabel'] != None:
			fontdict = {
				'weight': self._parameters['labelweight'],
				'fontsize': self._parameters['labelsize']
			}
			self._figure.xlabel(self._parameters['xlabel'], fontdict=fontdict)

		if self._parameters['ylabel'] != None:
			fontdict = {
				'weight': self._parameters['labelweight'],
				'fontsize': self._parameters['labelsize']
			}
			self._figure.ylabel(self._parameters['ylabel'], fontdict=fontdict)

		if self._parameters['xlim'] != None:
			self._figure.xlim(self._parameters['xlim'])

		if self._parameters['ylim'] != None:
			self._figure.ylim(self._parameters['ylim'])

		if self._parameters['ticksize'] != None:
			self._figure.tick_params(axis='both',labelsize=self._parameters['ticksize'])






def test():
	CustomizeFigure(plt)

	X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
	C, S = np.cos(X), np.sin(X)

	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.plot(X, C)
	ax.plot(X, S)

	# plt.savefig('./Test.pdf')
	plt.show()




if __name__ == '__main__':test()