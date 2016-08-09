#coding=UTF-8
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../../_iPackage')
import _toolkits
from CustomizeFigure import CustomizeFigure


class Plot(object):
	"""
	Introduction:
		This is the default setting of plot used in my experiments.
	Graph type:
		plot
	Input:
		path: path for saving figure .pdf
			Type: str
			Format:
				'./Test.pdf'
	"""
	def __init__(self, path='./Test.pdf'):
		super(Plot, self).__init__()
		self._path = path

		self._parameters = {
			'marker':'b-',
				# A valid marker style
				# character	description
				# '-'		solid line style
				# '--'		dashed line style
				# '-.'		dash-dot line style
				# ':'		dotted line style
				# '.'		point marker
				# ','		pixel marker
				# 'o'		circle marker
				# 'v'		triangle_down marker
				# '^'		triangle_up marker
				# '<'		triangle_left marker
				# '>'		triangle_right marker
				# '1'		tri_down marker
				# '2'		tri_up marker
				# '3'		tri_left marker
				# '4'		tri_right marker
				# 's'		square marker
				# 'p'		pentagon marker
				# '*'		star marker
				# 'h'		hexagon1 marker
				# 'H'		hexagon2 marker
				# '+'		plus marker
				# 'x'		x marker
				# 'D'		diamond marker
				# 'd'		thin_diamond marker
				# '|'		vline marker
				# '_'		hline marker

				# character	color
				# 'b'		blue
				# 'g'		green
				# 'r'		red
				# 'c'		cyan
				# 'm'		magenta
				# 'y'		yellow
				# 'k'		black
				# 'w'		white
			'markersize':8,
				# The size of markers.
			'linewidth':1,
				# The width of line, can be a list object.
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
		def _PlotFigure(self,data_fig,SaveOrShow='Show',parameters={'plot':{},'common':{}}):
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
					Format: {'plot':{},'common':{}} (same as self._parameters, see function test())
	Mission:
		_PlotFigure is for common plot.
	"""
	def _PlotFigure(self,data_fig,SaveOrShow='Show',parameters={'plot':{},'common':{}}):
		# update parameters for boxplot
		for key,value in parameters['plot'].items():
			self._parameters[key] = value

		Data,Label = self.__initData(data_fig)

		fig = plt.figure()
		CustomizeFigure(figure=plt,parameters=parameters['common'])
		ax = fig.add_subplot(111)
		

		for datum,marker in zip(Data,self._parameters['marker']):
			p = ax.plot(
				datum[0],
				datum[1],
				marker,
				markersize=self._parameters['markersize'],
				linewidth=self._parameters['linewidth'],
			)
		

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
		'1': {'Data':[np.array(range(10)),np.array([0,1,2,3,4,5,6,7,8,9])],'Label':'5'},
		'2': {'Data':[np.array(range(10)),np.array([-1,5,4,5,4,5,4,5,4,10])],'Label':'4'},
		'3': {'Data':[np.array(range(10)),np.array([3,2,3,2,3,2,3,2,3,2])],'Label':'3'},
		'4': {'Data':[np.array(range(10)),np.array([7,8,7,8,7,8,7,8,7,8])],'Label':'2'},
		'5': {'Data':[np.array(range(10)),np.array([5,6,7,8,9,5,6,7,8,9])],'Label':'1'}
	}

	"""
	Test
	"""
	task = Plot()
	parameters = {
		'plot':{
			'marker':['b-','g--','r-.','c:','m.'],
		},
		'common':{
			'xlabel': 'Sparsity',
			'ylabel': 'Number of Users',
			'figwidth': 15,
			'legend': {
				'type':'line',
				'color':['#000000','#FFFF00','#000000','#FFFF00','#000000'],
				'linestyle':['-','--','-.','-','--'],
				'label':['A','B','C','D','E'],
				'ncol':5,
				'bbox_to_anchor':(.2,.99,.6,.102),
				'borderaxespad':0.,
			},
		}
	}
	task._PlotFigure(data_fig=data,SaveOrShow='Show',parameters=parameters)



if __name__ == '__main__':test()