#coding=utf-8
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix
import MySQLdb
from datetime import datetime
import time
import random


import sys
sys.path.append('../_iPackage')
import _toolkits
from UserCF import *
from ItemCF import *
from MatrixFactorization import *
from MostPopular import *
from LBIMC import *
from Evaluation_Rec import *
from CriteriaWriter import *


class MatrixCompletion(object):
	"""docstring for MatrixCompletion"""
	def __init__(self,UserN,VenueN):
		super(MatrixCompletion, self).__init__()
		self._mat_train = coo_matrix(0)
		self._mat_behavior = coo_matrix(0)
		self._recommendation = dict()

		self._UserN = UserN
		self._VenueN = VenueN



	def oputUserVenue(self):
		# init
		users = list()
		users_records = list()
		venues = list()
		venues_checkins = list()

		# generate user list
		database = MySQLdb.connect('localhost','root','roro5460','LBSMining')
		with database:
			cursor = database.cursor();
			cursor.execute('SELECT DISTINCT user_id FROM LBSMining.CheckInNyc')
			data = cursor.fetchall()
			field = cursor.description
			for datum in data:
				users.append(datum[0])
			cursor.close()

		with database:
			cursor = database.cursor();
			for user in users:
				cursor.execute("SELECT count(user_id) FROM LBSMining.CheckInNyc WHERE user_id = \'{0}\'".format(user))
				data = cursor.fetchall()
				users_records.append([user,int(data[0][0])])
				print users_records[-1]
			cursor.close()
		database.close()

		users_records.sort(key=lambda x:x[1],reverse=True)

		userFile = open('./users_records','w')
		for user in users_records:
			userFile.write('{0}\t{1}\n'.format(user[0],user[1]))
		userFile.close()

		# generate venue list
		database = MySQLdb.connect('localhost','root','roro5460','LBSMining')
		with database:
			cursor = database.cursor();
			cursor.execute('SELECT DISTINCT v_id FROM LBSMining.CheckInNyc')
			data = cursor.fetchall()
			field = cursor.description
			for datum in data:
				venues.append(datum[0])
			cursor.close()


		with database:
			cursor = database.cursor();
			for venue in venues:
				cursor.execute("SELECT count(v_id) FROM LBSMining.CheckInNyc WHERE v_id = \'{0}\'".format(venue))
				data = cursor.fetchall()
				venues_checkins.append([venue,int(data[0][0])])
				print venues_checkins[-1]
			cursor.close()
		database.close()

		venues_checkins.sort(key=lambda x:x[1],reverse=True)

		venueFile = open('./venues_checkins','w')
		for venue in venues_checkins:
			venueFile.write('{0}\t{1}\n'.format(venue[0],venue[1]))
		venueFile.close()


	def getUserVenueInfo(self,period):
		# init
		UserDict = dict()
		Venue2Index = dict()
		Index2Venue = dict()

		
		UserArray = list()
		VenueArray = list()
		Check_insArray = list()

		# get info of users and venues
		with open('./users_records') as datum:
			data = datum.readlines()
		for index,datum in enumerate(data):
			UserDict[index] = datum.strip().split('\t')[0]
			if index >= self._UserN:
				break

		with open('./venues_checkins') as datum:
			data = datum.readlines()
		for index,datum in enumerate(data):
			Index2Venue[index] = datum.strip().split('\t')[0]
			Venue2Index[datum.strip().split('\t')[0]] = index
			if index >= self._VenueN:
				break

		database = MySQLdb.connect('localhost','root','roro5460','LBSMining')
		with database:
			cursor = database.cursor();

			for user in xrange(self._UserN):
				cursor.execute('SELECT v_id FROM LBSMining.CheckInNyc WHERE time < \'{0}\' AND user_id = \'{1}\''.format(period,UserDict[user]))
				data = cursor.fetchall()
				
				VenueList = list()
				for datum in data:
					VenueList.append(datum[0])

				for venue in Venue2Index:
					if VenueList.count(venue) != 0:
						UserArray.append(user)
						VenueArray.append(Venue2Index[venue])
						Check_insArray.append(VenueList.count(venue))


			cursor.close()
		database.close()

		matFile = open('./PeriodMat/{0}'.format(str(period.month)+'_mat'),'w')
		matFile.write('User:\n')
		for user in UserArray:
			matFile.write('{0}\t'.format(user))
		matFile.write('\n')
		matFile.write('Venue:\n')
		for venue in VenueArray:
			matFile.write('{0}\t'.format(venue))
		matFile.write('\n')
		matFile.write('Check-in:\n')
		for checkin in Check_insArray:
			matFile.write('{0}\t'.format(checkin))
		matFile.close()


	def genUserVenueMat(self,UVCFile):
		# init
		mode = 'Ready'
		UserArray = list()
		VenueArray = list()
		Check_insArray = list()

		# open restored mat info
		with open('./PeriodMat/{0}'.format(UVCFile)) as datum:
			data = datum.readlines()

		for index,datum in enumerate(data):
			datum = datum.strip().split('\t')

			if mode == 'Ready':
				if datum[0] == 'User:':
					mode = 'User'
					continue
				elif datum[0] == 'Venue:':
					mode = 'Venue'
					continue
				elif datum[0] == 'Check-in:':
					mode = 'Check-in'
					continue
			else:
				if mode == 'User':
					UserArray = np.array(map(int,datum))
					mode = 'Ready'
					continue
				elif mode == 'Venue':
					VenueArray = np.array(map(int,datum))
					mode = 'Ready'
					continue
				elif mode == 'Check-in':
					Check_insArray = np.array(map(int,datum))
					mode = 'Ready'
					continue


		return coo_matrix((Check_insArray,(UserArray,VenueArray)),shape=(self._UserN,self._VenueN))






def main():
	UserN = 1271
	VenueN = 2583

	mission = MatrixCompletion(UserN,VenueN)
	# mission.oputUserVenue()

	# period = [
	# 	datetime(2012,10,1,0,0,0),
	# 	datetime(2012,11,1,0,0,0),
	# 	datetime(2012,12,1,0,0,0),
	# 	datetime(2013,1,1,0,0,0),
	# 	datetime(2013,2,1,0,0,0),
	# 	datetime(2013,3,1,0,0,0),
	# 	datetime(2013,4,1,0,0,0),
	# 	datetime(2013,5,1,0,0,0),
	# 	datetime(2013,6,1,0,0,0),
	# 	datetime(2013,8,1,0,0,0)
	# 		]
	# for x in xrange(len(period)):
	# 	mission.getUserVenueInfo(period[x])

	UVCFile = ['10_mat','11_mat','12_mat','1_mat','2_mat','3_mat','4_mat','5_mat','6_mat','8_mat']
	# UVCFile = ['11_mat','12_mat','1_mat','2_mat','3_mat','4_mat','5_mat','6_mat','8_mat']

	for x in xrange(len(UVCFile)-1):
		mission._mat_train = mission.genUserVenueMat(UVCFile[x])
		mission._mat_behavior = mission.genUserVenueMat(UVCFile[x+1]) - mission.genUserVenueMat(UVCFile[x])

		mission._mat_train = mission._mat_train.tolil()
		for row in random.sample(range(mission._mat_train.get_shape()[0]),10):
			mission._mat_train[row,random.randint(0,mission._mat_train.get_shape()[1]-1)] = random.randint(100,200)
			
		for col in random.sample(range(mission._mat_train.get_shape()[1]),10):
			mission._mat_train[:,col] = np.mat([random.randint(100,200) for x in xrange(mission._mat_train.get_shape()[0])]).T
		
		
		# for nearPerson in xrange(10,11,1):
		# 	parameters = {'Data': UVCFile[x], 'K': nearPerson}
		# 	recommender = UserCF(mission._mat_train)
		# 	mission._recommendation = recommender.Recommend(K=parameters['K'])

		# for similarItem in xrange(40,41,1):
		# 	parameters = {'Data': UVCFile[x], 'K': similarItem}
		# 	recommender = ItemCF(mission._mat_train,previous=True)
		# 	mission._recommendation = recommender.Recommend(K=parameters['K'])

		# for mp in xrange(1):
		# 	parameters = {'Data': UVCFile[x]}
		# 	recommender = MostPopular(mission._mat_train)
		# 	mission._recommendation = recommender.Recommend()

		# for n_component in xrange(200,210,10):
		# 	parameters = {'Data': UVCFile[x], 'n_component': n_component}
		# 	recommender = MatrixFactorization(mission._mat_train)
		# 	mission._recommendation = recommender.Recommend(K=parameters['n_component'])

		for iteration in xrange(50,600,50):
		# for Lambda in xrange(0,10):
		# 	Lambda = 1.0*Lambda/10
		# for Mu in xrange(500,2000,100):
		# for Delta in xrange(0,20):
		# 	Delta = 1.0*Delta/10
			parameters = {'Data': UVCFile[x], 'Lambda':0.1, 'Mu':500, 'Delta':0.2, 'iteration':iteration}
			recommender = LBIMC(
							mat=mission._mat_train,
							iteration=parameters['iteration'],
							previous=False,
							Lambda=parameters['Lambda'],
							Mu=parameters['Mu'],
							Delta=parameters['Delta']
							)
			mission._recommendation = recommender.Recommend()


			criteria = set(['Recall','Precision','Coverage','Coverage_Gini'])
			for N in xrange(1,101):
				parameters['N'] = N
				result = Evaluation_Rec(mission._mat_train,mission._mat_behavior,mission._recommendation,N,criteria)._result
				CriteriaWriter(type(recommender).__name__,parameters,result)

				print '%s\t%s\t%s'%(type(recommender).__name__,','.join(map(str,parameters.items())),','.join(map(str,result.items())))




if __name__ == '__main__':	main()















