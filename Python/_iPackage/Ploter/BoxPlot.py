#coding=UTF-8
import numpy as np
import matplotlib.pyplot as plt



class BoxPlot(object):
	"""
	Introduction:
		This is the default setting of boxplot used in my experiments.
	Graph type:
		boxplot
	Input:
		data: the data of point
			Type: dict()
			Format:
				data = {
					'A': np.array([0,1,2,3,4,5,6,7,8,9]),
					'B': np.array([4,5,4,5,4,5,4,5,4,5]),
					'C': np.array([3,2,3,2,3,2,3,2,3,2]),
					'D': np.array([7,8,7,8,7,8,7,8,7,8]),
					'E': np.array([5,6,7,8,9,5,6,7,8,9])
				}
		parameters: the parameters to setup boxplot
			Type: dict()
			Format:

	"""
	def __init__(self, parameters={}, path='./Test.pdf'):
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
			'patch_artist':False,
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
			'manage_xticks':True
				# If the function should adjust the xlim and xtick locations.
		}
		for key,value in parameters.items():
			self._parameters[key] = value




	"""
	Function:
		def __initData(self,data):
		def _PlotFigure(self):
		def _PlotFigures(self):
	Mission:
		Plot and save figure.
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


	def _PlotFigure(self,data_fig,SaveOrShow):
		Data,Label = self.__initData(data_fig)

		plt.boxplot(
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
			manage_xticks=self._parameters['manage_xticks']
		)

		if SaveOrShow == 'Save':
			plt.savefig(self._path)
		else:
			plt.show()

		plt.close('all')


	def _PlotFigures(self,data_figs):
		for data_fig in data_figs:
			# fig, axes = plt.subplots(nrows=2, ncols=3)
			# axes[0, 0].boxplot(Data, labels=Label)
			# axes[0, 0].set_title('Default', fontsize=10)
			pass



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


	
	"""
	Test
	"""
	task = BoxPlot()
	task._PlotFigure(data,'Show')





if __name__ == '__main__':test()