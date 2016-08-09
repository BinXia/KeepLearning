import numpy as np




class var2file(object):
	"""
	var2file:
		This is a toolkit to convert any variable into a file for other applications.

	Input:
		var: the variable saving data
			Type: np.array or list
			Format: [1,2,3,4,5,6,7]

		location: the location of saving file
			Type: str
			Format: './test'
	"""
	def __init__(self,var,location):
		super(var2file, self).__init__()

		if len(np.shape(var)) == 1:
			self.OneDimension(var,location)


	def OneDimension(self,var,location):
		FILE = open(location,'w')
		for i,e in enumerate(var):
			FILE.write('{0}\t'.format(e))
		FILE.close()














def main():
	a = [1,2,3,4,5,6,7,8,9]

	task = var2file(a,'./test')


if __name__ == '__main__':main()