#coding=utf-8
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix,lil_matrix
# from multiprocessing import Process, Queue, freeze_support
from sklearn import svm
import time


class ESSVM(object):
	"""
	ESSVM:
		Embedded Space ranking SVM

	Input:
		mat: user-item matrix
			Type: coo_matrix or csr_matrix
			Format: row for users, col for items

		previous: True if previous items will be recommended
			Type: Boolean
			Format: True, False
	"""
	def __init__(self,mat,LocList,LocInfo,previous=True):
		super(ESSVM, self).__init__()

		self._mat = mat.tolil()
		self._LocList = LocList
		self._LocInfo = LocInfo



		self._UserList = list()
		self._UserInfo = dict()
		

		




	"""
	Function:
		def _ESSVM(self):
		def _parallelProcessing(self,u_i,features_roc,length):
		def __normalization(self,array,data,upper=0,lower=0):
		def __oputFeatures(self):
		def __embeddedSpace(self,features,labels):
		def __RankRec(self,user,RecMat):
		def Recommend(self,user=-1,N=1):
	Mission:
		Recommend items to the user based on contexts using Embedded Space ranking SVM
	Input:
		user: id of user we will recommend items
			Type: int
			Format: <= all users
		RecMat: the completed matrix for recommendation
			Type: numpy.matrixlib.defmatrix.matrix
			Format RecMat.shape == (users,items)
	Output:
		recommendation: the recommendation of each user
			Type: dict
			Format: key==user, value==[(item,score)...]
	"""
	def _ESSVM(self):
		self._features_roc,self._length = self.__oputFeatures()
		RecMat = np.zeros(np.shape(self._mat))

		for u_i in xrange(self._mat.get_shape()[0]):
			features_train = list()
			labels_train = list()
			features_upper = list()
			features_lower = list()
			recommendations = np.zeros(len(self._features_roc))

			for l_i in self._mat.getrow(u_i).nonzero()[1]:
				features_train.append(self._features_roc[l_i])
				labels_train.append(self._mat[u_i,l_i])
			features_train = np.array(features_train)
			if len(labels_train) <= 2:
				RecMat[u_i] = recommendations
				continue

			features_normal = np.zeros(np.shape(features_train.T))
			for row_i,row in enumerate(features_train.T):
				row,upper,lower = self.__normalization(row,'training')
				features_normal[row_i] = row
				features_upper.append(upper)
				features_lower.append(lower)
			features_train = np.array(features_normal).T
			labels_train = self.__labelData(labels_train)
			features_train,labels_train = self.__embeddedSpace(features_train,labels_train)

			clf = svm.LinearSVC()
			clf.fit(features_train,labels_train)
			coef = clf.coef_[0][:self._length]
			for index,sample in enumerate(self._features_roc):
				score = np.sum(sample*coef)
				recommendations[index] = score
			RecMat[u_i] = recommendations


			# freeze_support()
			# done_queue = Queue()
			# for u_i in xrange(self._mat.get_shape()[0]):
			# 	Process(target=self._parallelProcessing, args=(u_i,done_queue)).start()
			# for u_i in xrange(self._mat.get_shape()[0]):
			# 	Rec = done_queue.get()
			# 	print u_i
			# 	user = Rec.keys()[0]
			# 	RecMat[user] = Rec[user]


		return RecMat


	def _parallelProcessing(self,u_i,done_queue):
		features_train = list()
		labels_train = list()
		features_upper = list()
		features_lower = list()
		recommendations = np.zeros(len(self._features_roc))

		for l_i in self._mat.getrow(u_i).nonzero()[1]:
			features_train.append(self._features_roc[l_i])
			labels_train.append(self._mat[u_i,l_i])
		features_train = np.array(features_train)
		if len(labels_train) <= 2:
			done_queue.put({u_i:recommendations})
			return -1

		features_normal = np.zeros(np.shape(features_train.T))
		for row_i,row in enumerate(features_train.T):
			row,upper,lower = self.__normalization(row,'training')
			features_normal[row_i] = row
			features_upper.append(upper)
			features_lower.append(lower)
		features_train = np.array(features_normal).T
		labels_train = self.__labelData(labels_train)
		features_train,labels_train = self.__embeddedSpace(features_train,labels_train)

		clf = svm.LinearSVC()
		clf.fit(features_train,labels_train)
		coef = clf.coef_[0][:self._length]
		for index,sample in enumerate(self._features_roc):
			score = np.sum(sample*coef)
			recommendations[index] = score

		done_queue.put({u_i:recommendations})


	def __RankRec(self,user,RecMat):
		if self._previous:
			candidate = range(self._mat.get_shape()[1])
		else:
			user_item = list(self._mat.getrow(user).toarray()[0,:])
			candidate = [index for index,i in enumerate(user_item) if i == 0]

		recommendation = [[item, RecMat[user,item]] for item in candidate]
		recommendation.sort(key=lambda x:x[1], reverse=True)

		return recommendation

	def __oputFeatures(self):
		self._featuresUsed = [0,1,2,3,6,7,8,9,10,11]
		# self._featuresUsed = [0,11]
		# self._featuresUsed = [1,11]
		# self._featuresUsed = [2,11]
		# self._featuresUsed = [3,11]
		# self._featuresUsed = [6,11]
		# self._featuresUsed = [7,11]
		# self._featuresUsed = [8,11]
		# self._featuresUsed = [9,11]
		# self._featuresUsed = [10,11]
		userFeature = list()

		for l_i,loc in enumerate(self._LocList):
			features = list()

			if 0 in self._featuresUsed:
				# 0-total checkins ever here 						
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['stats']['checkinsCount']))
				except:
					features.append(0)

			if 1 in self._featuresUsed:
				# 1-tatal users who have ever checked in here 	
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['stats']['usersCount']))
				except:
					features.append(0)

			if 2 in self._featuresUsed:
				# 2-number of tips here 							
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['stats']['tipCount']))
				except:
					features.append(0)

			if 3 in self._featuresUsed:
				# 3-count of users who have liked this venue 		
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['likes']['count']))
				except:
					features.append(0)

				# 45-lat and lng 									
				# features.extend(sample._location);

			if 6 in self._featuresUsed:
				# 6-numerical rating of the venue (0 through 10)
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['rating']))
				except:
					features.append(0)

			if 7 in self._featuresUsed:
				# 7-count of photos for this venue 				
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['photos']['count']))
				except:
					features.append(0)

			if 8 in self._featuresUsed:
				# 8-the price tier from 1 (least pricey) - 4 (most pricey) 
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['price']['tier']))
				except:
					features.append(0)

			if 9 in self._featuresUsed:
				# 9-Boolean indicating whether the owner of this business has claimed it and verified the information.
				try:
					if bool(self._LocInfo[loc]['response']['venue']['verified']):
						features.append(0)
					else:
						features.append(1)
				except:
					features.append(0)

			if 10 in self._featuresUsed:
				# 10-Seconds since epoch when the venue was created. 
				try:
					features.append(int(self._LocInfo[loc]['response']['venue']['createdAt']))
				except:
					features.append(0)

			# 11-Contains count of the number of times the acting user has been here.
			if 11 in self._featuresUsed:
				features.append(np.sum(self._mat.getcol(l_i).toarray()))

			userFeature.append(features)

		return np.array(userFeature),len(self._featuresUsed)

	def __normalization(self,array,data,upper=0,lower=0):
		array = np.array(array,dtype=np.float64)
		if data == 'training':
			upper = np.max(array);
			lower = np.min(array);
			# print self._lower,self._upper;
			if upper == lower:
				return np.zeros((np.shape(array))),upper,lower;
			return (array - lower)/(upper - lower),upper,lower;
		else:
			if upper == lower:
				return np.zeros((np.shape(array)));
			return (array - lower)/(upper - lower);

	def __embeddedSpace(self,features,labels):
		features_new = list()
		labels_new = list()
		label_type = sorted(list(set(list(labels))))
		n_class = len(label_type)

		for index in xrange(np.shape(features)[0]):
			if labels[index] == label_type[0]:
				a_neg = np.ones(n_class-2);
				a_neg[:label_type.index(labels[index])] = 0;
				features_new.append(np.append(features[index],a_neg));
				labels_new.append(0);
			elif labels[index] == label_type[-1]:
				a_pos = np.ones(n_class-2);
				a_pos[:label_type.index(labels[index])-1] = 0;
				features_new.append(np.append(features[index],a_pos));
				labels_new.append(1);
			else:
				a_pos = np.ones(n_class-2);
				a_neg = np.ones(n_class-2);
				a_pos[:label_type.index(labels[index])-1] = 0;
				a_neg[:label_type.index(labels[index])] = 0;
				features_new.append(np.append(features[index],a_pos));
				labels_new.append(1);
				features_new.append(np.append(features[index],a_neg));
				labels_new.append(0);

		return np.array(features_new),np.array(labels_new)

	def __labelData(self,labels):
		records_list = [(i,label) for i,label in enumerate(labels)]
		records_list.sort(key=lambda x:x[1],reverse=True)
		records_sum = np.sum(labels)
		labels_new = np.zeros(len(labels))

		sum_machine = 0
		ratio = [0.5,0.8]

		for (l_i,record) in records_list:
			sum_machine += record
			if sum_machine <= records_sum * ratio[0]:
				labels_new[l_i] = 2
			elif sum_machine <= records_sum * ratio[1]:
				labels_new[l_i] = 1
			else:
				pass
		return labels_new



	def Recommend(self,RecMac=0,user=-1,N=1):
		if RecMac==0:
			RecMat = self._ESSVM()
		else:
			pass

		if user == -1:
			recommendation = dict()
			for user in xrange(self._mat.get_shape()[0]):
				recommendation[user] = self.__RankRec(user,RecMat)
			return recommendation
		else:
			return {user:self.__RankRec(user,RecMat)}






