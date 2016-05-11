#coding=UTF-8
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../../_iPackage')
import _toolkits
from CustomizeFigure import CustomizeFigure


class BoxPlot(object):
	"""
	Introduction:
		This is the default setting of boxplot used in my experiments.
	Graph type:
		boxplot
	Input:
		path: path for saving figure .pdf
			Type: str
			Format:
				'./Test.pdf'
	"""
	def __init__(self, path='./Test.pdf'):
		super(BoxPlot, self).__init__()
		self._path = path

		self._parameters = {
			'notch':False,
				# If False, produces a rectangular box plot. If True, will produce a notched box plot
			'sym':'b+',
				# The default symbol for flier points. Enter an empty string (‘’) if you don’t want to show fliers. If None, then the fliers default to ‘b+’ If you want more control use the flierprops kwarg.
			'vert':True,
				# If True (default), makes the boxes vertical. If False, makes horizontal boxes.
			'whis':1.5,
				# As a float, determines the reach of the whiskers past the first and third quartiles (e.g., Q3 + whis*IQR, IQR = interquartile range, Q3-Q1). Beyond the whiskers, data are considered outliers and are plotted as individual points. Set this to an unreasonably high value to force the whiskers to show the min and max values. Alternatively, set this to an ascending sequence of percentile (e.g., [5, 95]) to set the whiskers at specific percentiles of the data. Finally, whis can be the string ‘range’ to force the whiskers to the min and max of the data. In the edge case that the 25th and 75th percentiles are equivalent, whis will be automatically set to ‘range’.
			'bootstrap':None,
				# Specifies whether to bootstrap the confidence intervals around the median for notched boxplots. If bootstrap==None, no bootstrapping is performed, and notches are calculated using a Gaussian-based asymptotic approximation (see McGill, R., Tukey, J.W., and Larsen, W.A., 1978, and Kendall and Stuart, 1967). Otherwise, bootstrap specifies the number of times to bootstrap the median to determine it’s 95% confidence intervals. Values between 1000 and 10000 are recommended.
			'usermedians':None,
				# An array or sequence whose first dimension (or length) is compatible with x. This overrides the medians computed by matplotlib for each element of usermedians that is not None. When an element of usermedians == None, the median will be computed by matplotlib as normal.
			'conf_intervals':None,
				# Array or sequence whose first dimension (or length) is compatible with x and whose second dimension is 2. When the current element of conf_intervals is not None, the notch locations computed by matplotlib are overridden (assuming notch is True). When an element of conf_intervals is None, boxplot compute notches the method specified by the other kwargs (e.g., bootstrap).
			'patch_artist':True,
				# If False produces boxes with the Line2D artist If True produces boxes with the Patch artist
			'showmeans':True,
				# If True, will toggle one the rendering of the means
			'showcaps':True,
				# If True, will toggle one the rendering of the caps
			'showbox':True,
				# If True, will toggle one the rendering of boxes
			'showfliers':True,
				# If True, will toggle one the rendering of the fliers
			'boxprops':None,
				# If provided, will set the plotting style of the boxes
			'whiskerprops':None,
				# If provided, will set the plotting style of the whiskers
			'capprops':None,
				# If provided, will set the plotting style of the caps
			'flierprops':None,
				# If provided, will set the plotting style of the fliers
			'medianprops':None,
				# If provided, will set the plotting style of the medians
			'meanprops':None,
				# If provided, will set the plotting style of the means
			'meanline':False,
				# If True (and showmeans is True), will try to render the mean as a line spanning the full width of the box according to meanprops. Not recommended if shownotches is also True. Otherwise, means will be shown as points.
			'manage_xticks':False,
				# If the function should adjust the xlim and xtick locations.
			'widths': 0.5,
				# the width of box, if width is equal to 1, then no distance between two boxes.
			'facecolor':['#00BFFF']
				# the filled color of box. Format: ['#00BFFF','#00BFFF','#00BFFF','#00BFFF']; Type: list and color.
		}



	"""
	Function:
		def __initData(self,data):
			Input:
				data: the data of point
					Type: dict()
					Format:
						See fucntion test()
			Output:
				Data: formatted data
					Type: list()
				Label: label for each array
					Type: list()
	Mission:
		Load and format input data.
	"""
	def __initData(self,data):
		Data = list()
		Label = list()

		dataset = list()
		try:
			dataset = sorted(data.items(),key=lambda x:int(x[0]))
		except:
			dataset = sorted(data.items(),key=lambda x:str(x[0]))

		for index,value in dataset:
			Label.append(value['Label'])
			Data.append(value['Data'])
		return Data,Label

	"""
	Function:
		def __decoration(self,bp):
			Input:
				bp: instance of boxplot
					Type: matplotlib.pyplot.boxplot
	Mission:
		Customize components of boxplot, such as box, whisker, cap, median, and flier.
	"""
	def __decoration(self,bp):
		# change outline color, fill color and linewidth of the boxes
		for box,facecolor in zip(bp['boxes'],self._parameters['facecolor']*len(bp['boxes'])):
			# change outline color
			box.set(color=('#000000'), linewidth=1)
			# change fill color
			box.set(facecolor=facecolor)

		# change color and linewidth of the whiskers
		for whisker in bp['whiskers']:
			whisker.set(color='#000000', linewidth=2)

		# change color and linewidth of the caps
		for cap in bp['caps']:
			cap.set(color='#000000', linewidth=2)

		# change color and linewidth of the medians
		for median in bp['medians']:
			median.set(color='#000000', linewidth=2)

		# change the style of fliers and their fill
		for flier in bp['fliers']:
			flier.set(marker='o', color='#e7298a', alpha=0.5)

	"""
	Function:
		def __SaveOrShow(self,SaveOrShow):
			Input:
				SaveOrShow: option for save or show fig
					Type: str
					Format: 'Save' or 'Show'
	Mission:
		Clear plt after save or show figure
	"""
	def __SaveOrShow(self,SaveOrShow):
		if SaveOrShow == 'Save':
			plt.savefig(self._path)
		else:
			plt.show()
		plt.close('all')



	"""
	Function:
		def _PlotFigure(self,data_fig,SaveOrShow='Show',parameters={'boxplot':{},'common':{}}):
		def _PlotGroupFigure(self,data_fig,SaveOrShow='Show',parameters={'boxplot':{},'common':{}}):
			Input:
				data_fig: the data of point (same as 'data' in '__initData')
					Type: dict()
					Format:
						See fucntion test()
				SaveOrShow: option for save or show fig (same as 'SaveOrShow' in '__SaveOrShow')
					Type: str
					Format: 'Save' or 'Show'
				parameters: parameters for option in boxplot and common
					Type: dict()
					Format: {'boxplot':{},'common':{}} (same as self._parameters, see function test())
	Mission:
		_PlotFigure is for common boxplot.
		_PlotGroupFigure is for group boxplot (need to set xlabel in parameters['common']).
	"""
	def _PlotFigure(self,data_fig,SaveOrShow='Show',parameters={'boxplot':{},'common':{}}):
		# update parameters for boxplot
		for key,value in parameters['boxplot'].items():
			self._parameters[key] = value

		Data,Label = self.__initData(data_fig)

		fig = plt.figure()
		CustomizeFigure(figure=plt,parameters=parameters['common'])
		ax = fig.add_subplot(111)
		# Remove top axes and right axes ticks
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()

		bp = ax.boxplot(
			x=Data,
			notch=self._parameters['notch'],
			sym=self._parameters['sym'],
			vert=self._parameters['vert'],
			whis=self._parameters['whis'],
			bootstrap=self._parameters['bootstrap'],
			usermedians=self._parameters['usermedians'],
			conf_intervals=self._parameters['conf_intervals'],
			patch_artist=self._parameters['patch_artist'],
			labels=Label,
			showmeans=self._parameters['showmeans'],
			showcaps=self._parameters['showcaps'],
			showbox=self._parameters['showbox'],
			showfliers=self._parameters['showfliers'],
			boxprops=self._parameters['boxprops'],
			whiskerprops=self._parameters['whiskerprops'],
			capprops=self._parameters['capprops'],
			flierprops=self._parameters['flierprops'],
			medianprops=self._parameters['medianprops'],
			meanprops=self._parameters['meanprops'],
			meanline=self._parameters['meanline'],
			manage_xticks=self._parameters['manage_xticks'],
			widths=self._parameters['widths']
		)

		self.__decoration(bp)
		self.__SaveOrShow(SaveOrShow)

		

	def _PlotGroupFigure(self,data_fig,SaveOrShow='Show',parameters={'boxplot':{},'common':{}}):
		# update parameters for boxplot
		for key,value in parameters['boxplot'].items():
			self._parameters[key] = value

		Data,Label = self.__initData(data_fig)

		fig = plt.figure()
		CustomizeFigure(figure=plt,parameters=parameters['common'])
		ax = fig.add_subplot(111)
		# Remove top axes and right axes ticks
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()


		for datum,position in zip(Data,self._parameters['positions']):

			bp = ax.boxplot(
				x=list(datum),
				notch=self._parameters['notch'],
				sym=self._parameters['sym'],
				vert=self._parameters['vert'],
				whis=self._parameters['whis'],
				bootstrap=self._parameters['bootstrap'],
				usermedians=self._parameters['usermedians'],
				conf_intervals=self._parameters['conf_intervals'],
				patch_artist=self._parameters['patch_artist'],
				positions=position,
				showmeans=self._parameters['showmeans'],
				showcaps=self._parameters['showcaps'],
				showbox=self._parameters['showbox'],
				showfliers=self._parameters['showfliers'],
				boxprops=self._parameters['boxprops'],
				whiskerprops=self._parameters['whiskerprops'],
				capprops=self._parameters['capprops'],
				flierprops=self._parameters['flierprops'],
				medianprops=self._parameters['medianprops'],
				meanprops=self._parameters['meanprops'],
				meanline=self._parameters['meanline'],
				manage_xticks=self._parameters['manage_xticks'],
				widths=self._parameters['widths']
			)

			self.__decoration(bp)
		self.__SaveOrShow(SaveOrShow)



def test():
	"""
	Data:
		A: np.array([0,1,2,3,4,5,6,7,8,9])
		B: np.array([4,5,4,5,4,5,4,5,4,5])
		C: np.array([3,2,3,2,3,2,3,2,3,2])
		D: np.array([7,8,7,8,7,8,7,8,7,8])
		E: np.array([5,6,7,8,9,5,6,7,8,9])
	"""
	data = {
		'1': {'Data':np.array([0,1,2,3,4,5,6,7,8,9]),'Label':'5'},
		'2': {'Data':np.array([-1,5,4,5,4,5,4,5,4,10]),'Label':'4'},
		'3': {'Data':np.array([3,2,3,2,3,2,3,2,3,2]),'Label':'3'},
		'4': {'Data':np.array([7,8,7,8,7,8,7,8,7,8]),'Label':'2'},
		'5': {'Data':np.array([5,6,7,8,9,5,6,7,8,9]),'Label':'1'}
	}

	data_group = {
		'1': {'Data':np.array([[0,1,2,3,4,5,6,7,8,9],[-1,5,4,5,4,5,4,5,4,10],[3,2,3,2,3,2,3,2,3,2],[7,8,7,8,7,8,7,8,7,8],[5,6,7,8,9,5,6,7,8,9]]),'Label':'5'},
		'2': {'Data':np.array([[0,1,2,3,4,5,6,7,8,9],[-1,5,4,5,4,5,4,5,4,10],[3,2,3,2,3,2,3,2,3,2],[7,8,7,8,7,8,7,8,7,8],[5,6,7,8,9,5,6,7,8,9]]),'Label':'4'},
		'3': {'Data':np.array([[0,1,2,3,4,5,6,7,8,9],[-1,5,4,5,4,5,4,5,4,10],[3,2,3,2,3,2,3,2,3,2],[7,8,7,8,7,8,7,8,7,8],[5,6,7,8,9,5,6,7,8,9]]),'Label':'3'},
		'4': {'Data':np.array([[0,1,2,3,4,5,6,7,8,9],[-1,5,4,5,4,5,4,5,4,10],[3,2,3,2,3,2,3,2,3,2],[7,8,7,8,7,8,7,8,7,8],[5,6,7,8,9,5,6,7,8,9]]),'Label':'2'},
		'5': {'Data':np.array([[0,1,2,3,4,5,6,7,8,9],[-1,5,4,5,4,5,4,5,4,10],[3,2,3,2,3,2,3,2,3,2],[7,8,7,8,7,8,7,8,7,8],[5,6,7,8,9,5,6,7,8,9]]),'Label':'1'}
	}

	
	"""
	Test
	"""
	task = BoxPlot()
	parameters = {
		'boxplot':{
			'positions': [range(1,6),range(7,12),range(13,18),range(19,24),range(25,30)],
			'widths': 0.99
		},
		'common':{
			'xlabel': 'Sparsity',
			'ylabel': 'Number of Users',
			# 'figwidth': 12
		}
	}
	# task._PlotFigure(data_fig=data,SaveOrShow='Show',parameters=parameters)
	task._PlotGroupFigure(data_fig=data_group,SaveOrShow='Show',parameters=parameters)




if __name__ == '__main__':test()