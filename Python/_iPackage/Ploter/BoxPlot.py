import numpy as np
from matplotlib.pyplot import plt
from matplotlib.backends.backend_pdf import PdfPages





class BoxPlot(object):
	"""
	Introduction:
		This is the default setting of boxplot used in my experiments.
	Graph type:
		boxplot
	Parameters:

	"""
	def __init__(self, data):
		super(BoxPlot, self).__init__()
		self._data = data
		
		
		self._PlotAndSave()


	"""
	Function:
		def __initData(self):
		def _PlotAndSave(self):
	"""
	def __initData(self):
		for x_axis in self._data:
			



	def _PlotAndSave(self):
		self.__initData()


		fig, axes = plt.subplots(nrows=1, ncols=1)
		axes[0, 0].boxplot(data, labels=labels)
		axes[0, 0].set_title('Default', fontsize=fs)



		pp = PdfPages('test.pdf')






		pp.savefig()
		PP.close()





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
		'A': np.array([0,1,2,3,4,5,6,7,8,9]),
		'B': np.array([4,5,4,5,4,5,4,5,4,5]),
		'C': np.array([3,2,3,2,3,2,3,2,3,2]),
		'D': np.array([7,8,7,8,7,8,7,8,7,8]),
		'E': np.array([5,6,7,8,9,5,6,7,8,9])
	}



	"""
	Test
	"""
	task = BoxPlot(data)







if __name__ == '__main__':test()