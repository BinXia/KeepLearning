import numpy as np
import time


def normalization(seq):
	seq = np.array(seq,dtype=np.float16)
	if np.max(seq) == np.min(seq):
		return np.ones(len(seq))
	else:
		return (seq-np.min(seq))/(np.max(seq)-np.min(seq))


class SlidingWindow(object):
	"""
	Sliding Window Algorithm for segmenting time series.
	"""
	def __init__(self,seq,online=False,max_error=1):
		super(SlidingWindow, self).__init__()
		self._segmentation = list()
		
		seq = normalization(seq)
		if online:
			self.online(seq,max_error)
		else:
			self.offline(seq,max_error)


	def online(self,seq,max_error):
		pass

	def offline(self,seq,max_error):
		for index,num in enumerate(seq):
			if index == 0:
				self._segmentation.append(index)
				continue

			# print index,np.var(seq[self._segmentation[-1]:index+1]),seq[self._segmentation[-1]:index+1]
			if np.var(seq[self._segmentation[-1]:index+1]) >= max_error:
				self._segmentation.append(index)


class TopDown(object):
	"""
	Top-Down Algorithm for segmenting time series.
	"""
	def __init__(self,seq,max_error=1):
		super(TopDown, self).__init__()
		self._segmentation = list()
		
		seq = normalization(seq)
		self.offline(seq,max_error,range(len(seq)))
		self._segmentation.sort()

	def offline(self,seq,max_error,seq_index):
		best_so_far = 1
		breakpoint = 0
		left = 0
		right = 0

		for index in xrange(1,len(seq)-1):
			left = np.var(seq[:index+1])
			right = np.var(seq[index+1:])
			whole = np.var(seq)
			if (whole - left) > 0 and (whole - right) > 0 and ((whole - left)+(whole - right))/2 > best_so_far:
				breakpoint = index
				best_so_far = ((whole - left)+(whole - right))/2
			# print index,left,right,list(seq[:index+1])
		self._segmentation.append(seq_index[breakpoint])
		if left >= max_error:
			# print left,range(seq_index[0],breakpoint)
			self.offline(seq[:breakpoint+1],max_error,range(seq_index[0],seq_index[breakpoint+1]))
		if right >= max_error:
			self.offline(seq[breakpoint+1:],max_error,range(seq_index[breakpoint+1],seq_index[-1]+1))



class BottomUp(object):
	"""
	Bottom-Up Algorithm for segmenting time series.
	"""
	def __init__(self,seq,online=False,max_error=1):
		super(BottomUp, self).__init__()
		self._segmentation = list()
		
		seq = normalization(seq)
		if online:
			self.online(seq,max_error)
		else:
			self.offline(seq,max_error)


	def online(self,seq,max_error):
		pass


	def offline(self,seq,max_error):
		seq_block = list()
		merge_cost = list()
		for index in xrange(0,len(seq),2):
			if (index+4) > len(seq):
				seq_block.append(seq[index:])
				merge_cost.append(np.var(seq[index:]))
				break
			else:
				seq_block.append(seq[index:index+2])
				merge_cost.append(np.var(seq[index:index+2]))

		while np.min(merge_cost) < max_error:
			index = merge_cost.index(np.min(merge_cost))
			if index == len(seq_block) - 1:
				seq_block[index-1] = np.hstack(np.array([seq_block[index-1],seq_block[index]]))
				del seq_block[index]
				merge_cost[index-1] = np.var(seq_block[index-1])
				del merge_cost[index]
			else:
				seq_block[index] = np.hstack(np.array([seq_block[index],seq_block[index+1]]))
				del seq_block[index+1]
				merge_cost[index] = np.var(seq_block[index])
				del merge_cost[index+1]
			# print merge_cost

		base = 0
		for sequence in seq_block:
			if len(self._segmentation) == 0:
				self._segmentation.append(self.turnpoint(sequence))
			else:
				# if len(sequence)+self._segmentation[-1] >= len(seq):
				# 	continue
				# else:
				# 	self._segmentation.append(len(sequence)+self._segmentation[-1])
				self._segmentation.append(self.turnpoint(sequence)+base)

			base += len(sequence)

	def turnpoint(self,seq):
		average = np.mean(seq)
		MAX = 0
		record = 0
		for i,e in enumerate(seq):
			if abs(e-average) > MAX:
				MAX = abs(e-average)
				record = i
		return record


class PLR(object):
	"""
	Piecewise Linear Representation for time-series segmentation
	"""
	def __init__(self,seq,online=False,max_error=1):
		super(PLR, self).__init__()
		self._seq = seq
		self._segmentation = [0,len(seq)-1]
		
		self._weight = np.ones(len(seq))

		seq = normalization(seq)
		if online:
			self.online(seq,max_error)
		else:
			self.offline(seq,max_error,range(len(seq)))

		self._segmentation.sort()
		del self._segmentation[0]
		del self._segmentation[-1]


	def online(self,seq,max_error):
		pass


	def offline(self,seq,max_error,seq_index):
		dis_list = [0]*len(seq)
		for i,p in enumerate(seq):
			dis_list[i] = self.distance_P2L(0,seq[0],len(seq)-1,seq[-1],i,p)

		if np.max(dis_list) > max_error:
			turnpoint = dis_list.index(np.max(dis_list))
			self._segmentation.append(seq_index[turnpoint])
			self.offline(seq[:turnpoint+1],max_error,range(seq_index[0],seq_index[turnpoint+1]))
			self.offline(seq[turnpoint:],max_error,range(seq_index[turnpoint],seq_index[-1]+1))


	def weighPoint(self,labels,srA,scB):
		for index in xrange(len(self._segmentation)):
			if labels[self._segmentation[index]] == 1:
				while self._seq[self._segmentation[index]-1] == self._seq[self._segmentation[index]]:
					self._segmentation[index] = self._segmentation[index] - 1
				labels[self._segmentation[index]] = 2
			else:
				while self._seq[self._segmentation[index]-1] == self._seq[self._segmentation[index]]:
					self._segmentation[index] = self._segmentation[index] - 1
				labels[self._segmentation[index]] = 3

		# updata labels of samples
		for index in xrange(len(labels)):
			if labels[index] == -1:
				labels[index] = 1
				self._weight[index] = 1
			elif labels[index] == 2:
				self._weight[index] += srA
			elif labels[index] == 3:
				self._weight[index] += scB

		return (labels,self._weight)


	def distance_P2L(self,line_start_x,line_start_y,line_end_x,line_end_y,point_x,point_y):
		A = line_end_y - line_start_y;
		B = line_start_x - line_end_x;
		C = line_end_x * line_start_y - line_start_x * line_end_y;
		distance = np.abs(A * point_x + B * point_y + C)/np.power(A**2+B**2,0.5);
		return distance;



def main():
	'''
	Prepare the time series
	4,6,13
	6,13
	'''
	seq = [1,1,1,1,0,1,5,1,1,2,3,2,1,5,5,5,5]
	# 	   0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6

	'''
	Test algorithms
	'''
	# max_error = 0.05
	# task = SlidingWindow(seq=seq,online=False,max_error=max_error)
	# print task._segmentation

	# max_error = 0.05
	# task = TopDown(seq=seq,max_error=max_error)
	# print task._segmentation

	max_error = 0.005
	task = BottomUp(seq=seq,online=False,max_error=max_error)
	print task._segmentation

	# max_error = 0.5
	# task = PLR(seq=seq,online=False,max_error=max_error)
	# print task._segmentation


if __name__ == '__main__':main()