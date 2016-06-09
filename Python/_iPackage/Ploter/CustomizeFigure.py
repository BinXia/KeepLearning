import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



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
			'labelweight': 'bold',
				# bold label for axis label. Format: ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']; Type: str
			'labelsize': 12,
				# font size of xlabel and ylabel. Format: 12; Type: int
			'xtick': None,
				# the positions of xticklabel. Format: [1,3,5]; Type: int
			'xticklabel': None,
				# the label of xtick. Format: ['A','B']; Type: str
			'tickweight': 'normal',
				# bold label for axis tick. Format: ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']; Type: str
			'ticksize': 12,
				# font size of xtick and ytick. Format: 12; Type: int
			'tickvisible': {'x':False,'y':False},
				# the visibility of tick. Format: {'x':True,'y':True}; Type: dict+boolean
			'legend': None,
				# the legend of figure. Format: 
				# 'legend': {
				# 	'type':'patch',
				# 	'color':['#000000','#FFFF00'],
				# 	'linestyle':['-','-'],
				# 	'label':['A','B'],
				# }
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

		if self._parameters['xticklabel'] != None and self._parameters['xtick'] != None:
			fontdict = {
				'weight': self._parameters['tickweight'],
				'fontsize': self._parameters['ticksize']
			}
			self._figure.gca().set_xticklabels(self._parameters['xticklabel'],fontdict=fontdict)
			self._figure.gca().set_xticks(self._parameters['xtick'])

		if self._parameters['tickvisible'] != None:
			axis = None
			if not self._parameters['tickvisible']['x'] and not self._parameters['tickvisible']['y']:
				axis = 'both'
			elif self._parameters['tickvisible']['x'] and not self._parameters['tickvisible']['y']:
				axis = 'y'
			elif not self._parameters['tickvisible']['x'] and self._parameters['tickvisible']['y']:
				axis = 'x'
			else:
				axis = None

			if axis != None:
				if axis == 'x':
					self._figure.gca().set_xticks([])
					self._figure.tick_params(axis=axis,which='both',bottom=False,top=False)
				elif axis == 'y':
					self._figure.gca().set_yticks([])
					self._figure.tick_params(axis=axis,which='both',left=False,right=False)
				else:
					self._figure.gca().set_xticks([])
					self._figure.gca().set_yticks([])
					self._figure.tick_params(axis=axis,which='both',bottom=False,top=False,left=False,right=False)

		if self._parameters['legend'] != None:
			legend = {
				'edgecolor': None,
				'facecolor': None,
				'color': None,
				'linewidth': None,
				'linestyle': None,
				'label': None,
				'loc': None,
				'mode': None,
				'ncol': None,
				'borderaxespad': None,
			}
			for key,value in self._parameters['legend'].items():
				legend[key] = value
			handles = list()
			num = len(legend['label'])

			if legend['type'] == 'line':
				for index in range(num):
					handles.append(
						plt.Line2D((0,0),(0,0), 
							color=legend['color'][index],
							linestyle=legend['linestyle'][index],
							label=legend['label'][index],
						)
					)
			elif self._parameters['legend']['type'] == 'patch':
				for index in range(num):
					handles.append(
						mpatches.Patch(
							edgecolor=legend['edgecolor'],
							facecolor=legend['facecolor'][index],
							# color=legend['color'][index],
							linewidth=legend['linewidth'],
							linestyle=legend['linestyle'],
							label=legend['label'][index],
						)
					)
			self._figure.gca().legend(
				handles=handles,
				loc=legend['loc'],
				mode=legend['mode'],
				ncol=legend['ncol'],
				borderaxespad=legend['borderaxespad'],
				bbox_to_anchor=legend['bbox_to_anchor'],
			)




def test():
	parameters = {
		# 'legend': {
		# 	'type':'line',
		# 	'color':['#000000','#FFFF00'],
		# 	'linestyle':['-','-'],
		# 	'label':['A','B'],
		# },
		# 'legend': {
		# 	'type':'patch',
		# 	'color':['#000000','#FFFF00'],
		# 	'linestyle':'-',
		# 	'label':['A','B'],
		# },
	}
	
	X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
	C, S = np.cos(X), np.sin(X)

	fig = plt.figure()
	CustomizeFigure(figure=plt,parameters=parameters)
	ax = fig.add_subplot(111)

	a = ax.plot(X, C)
	b = ax.plot(X, S)

	
	

	# plt.savefig('./Test.pdf')
	plt.show()




if __name__ == '__main__':test()