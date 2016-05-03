import sys
sys.path.append('../_iPackage')
import _toolkits
from BoxPlot import BoxPlot

import MySQLdb
import numpy as np
from datetime import datetime


periods = [
	datetime(2012,10,1,0,0,0),
	datetime(2012,11,1,0,0,0),
	datetime(2012,12,1,0,0,0),
	datetime(2013,1,1,0,0,0),
	datetime(2013,2,1,0,0,0),
	datetime(2013,3,1,0,0,0),
	datetime(2013,4,1,0,0,0),
	datetime(2013,5,1,0,0,0),
	datetime(2013,6,1,0,0,0),
	datetime(2013,8,1,0,0,0)
]


def plotUserBoxPlot():
	sparsityRange = [
		1,
		2,
		3,
		4,
		5,
		6,
		7,
		8,
		9,
		10,
		20,
		50,
		5000
	]
	sparsityLevels = [
		'1',
		'2',
		'3',
		'4',
		'5',
		'6',
		'7',
		'8',
		'9',
		'10-12',
		'12-15',
		'15-20'
	]
	sparsityLevel = dict()
	for sparsity in xrange(0,len(sparsityRange)-1):
		sparsityLevel.setdefault(str(sparsity),{'Range':[sparsityRange[sparsity],sparsityRange[sparsity+1]],'Data':[0]*10,'Label':sparsityLevels[sparsity]})



	database = MySQLdb.connect('localhost','root','roro5460','LBSMining')
	cursor = database.cursor();
	for index,period in enumerate(periods):
		cursor.execute('SELECT user_id,count(*) FROM LBSMining.CheckInNyc WHERE time < \'{0}\' GROUP BY user_id'.format(period))
		data = cursor.fetchall()
		for user,records in data:
			for key,value in sparsityLevel.items():
				if records >= sparsityLevel[key]['Range'][0] and records < sparsityLevel[key]['Range'][1]:
					sparsityLevel[key]['Data'][index] += 1
					break

	sparsity = dict()
	for index,(key,value) in enumerate(sparsityLevel.items()):
		try:
			sparsity[key]
		except:
			sparsity.setdefault(key,{})

		sparsity[key]['Data'] = np.array(sparsityLevel[key]['Data'])
		sparsity[key]['Label'] = sparsityLevel[key]['Label']
		

	print sparsity

	task = BoxPlot(path='./SparsityOfUser.pdf')
	task._PlotFigure(sparsity,'Save')



def plotVenueBoxPlot():
	sparsityRange = [
		1,
		2,
		3,
		4,
		5,
		6,
		7,
		8,
		9,
		10,
		20,
		50,
		5000
	]
	sparsityLevels = [
		'1',
		'2',
		'3',
		'4',
		'5',
		'6',
		'7',
		'8',
		'9',
		'10-12',
		'12-15',
		'15-20'
	]
	sparsityLevel = dict()
	for sparsity in xrange(0,len(sparsityRange)-1):
		sparsityLevel.setdefault(str(sparsity),{'Range':[sparsityRange[sparsity],sparsityRange[sparsity+1]],'Data':[0]*10,'Label':sparsityLevels[sparsity]})

	database = MySQLdb.connect('localhost','root','roro5460','LBSMining')
	cursor = database.cursor();
	for index,period in enumerate(periods):
		cursor.execute('SELECT v_id,count(*) FROM LBSMining.CheckInNyc WHERE time < \'{0}\' GROUP BY v_id'.format(period))
		data = cursor.fetchall()
		for user,records in data:
			for key,value in sparsityLevel.items():
				if records >= sparsityLevel[key]['Range'][0] and records < sparsityLevel[key]['Range'][1]:
					sparsityLevel[key]['Data'][index] += 1
					break

	sparsity = dict()
	for index,(key,value) in enumerate(sparsityLevel.items()):
		try:
			sparsity[key]
		except:
			sparsity.setdefault(key,{})

		sparsity[key]['Data'] = np.array(sparsityLevel[key]['Data'])
		sparsity[key]['Label'] = sparsityLevel[key]['Label']
		

	print sparsity

	task = BoxPlot(path='./SparsityOfVenue.pdf')
	task._PlotFigure(sparsity,'Save')





def test():
	# plotUserBoxPlot()
	plotVenueBoxPlot()



if __name__ == '__main__':test()