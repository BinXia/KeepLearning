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
			
		}


	