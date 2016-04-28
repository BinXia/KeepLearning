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
	def __init__(self, data, parameters=0):
		super(BoxPlot, self).__init__()
		self._data = data
		self._parameters = parameters

		self._PlotAndSave()



	"""
	Function:
		def __initData(self):
		def _PlotAndSave(self):
	Mission:
		Plot and save figure.
	"""
	def __initData(self):
		Data = list()
		Label = list()
		for x_axis,y_axis in self._data.items():
			Label.append(x_axis)
			Data.append(y_axis)
		return Data,Label


	def _PlotAndSave(self):
		Data,Label = self.__initData()


		fig, axes = plt.subplots(nrows=2, ncols=3)
		axes[0, 0].boxplot(Data, labels=Label)
		axes[0, 0].set_title('Default', fontsize=10)






def test():
	"""
	Data:
		A: np.array([0,1,2,3,4,5,6,7,8,9])
		B: np.array([4,5,4,5,4,5,4,5,4,5])
		C: np.array([3,2,3,2,3,2,3,2,3,2])
		D: np.array([7,8,7,8,7,8,7,8,7,8])
		E: np.array([5,6,7,8,9,5,6,7,8,9])
	"""
	data = 



	"""
	Test
	"""
	task = BoxPlot(data)







if __name__ == '__main__':test()