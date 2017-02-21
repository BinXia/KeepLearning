#coding=UTF-8
import numpy as np
import pprint
pp = pprint.PrettyPrinter()
from itertools import combinations
import math



class p_pattern(object):
	"""docstring for p_pattern"""
	def __init__(self, para):
		super(p_pattern, self).__init__()
		self.data = para["data"]
		self.tol = int(para["tolerance"])
		self.conf = para["confidence"]
		self.alpha = para["alpha"]
		self.beta = para["beta"]

		self.level_sup = list()			# Store supports of combinations in different levels
		self.PP = dict()


		event_peri_cand = dict()
		event_seq = self.Processing()
		for event_type,seq in event_seq.items():
			for period in self.SearchUnknownPeriods(seq):
				event_peri_cand.setdefault(period,[])
				event_peri_cand[period].append(event_type)


		self.PeriodFirst(event_peri_cand)


	def Processing(self):
		event_seq = dict()
		win_left = 0
		win_right = 0
		for event in self.data:
			event_seq.setdefault(event[0],[])
			event_seq[event[0]].append(event[1])
			if event[1] < win_left:
				win_left = event[1]
			if event[1] > win_right:
				win_right = event[1]

		self.T = win_right-win_left
		# event_seq = filter(lambda x:x["Event"] == self.type,event_seq)

		for event_type,seq in event_seq.items():
			event_seq[event_type] = sorted(seq)

		return event_seq



	def SearchUnknownPeriods(self,seq):
		C_tau = dict()
		# Step(1) counts the occurrence of each inter-arrival time.
		for i in xrange(1,len(seq)):
			tau = seq[i] - seq[i-1]
			if C_tau.has_key(tau):
				C_tau[tau] += 1
			else:
				C_tau[tau] = 1

		# Step(2) groups inter-arrival times to account for time tolerance delta by merging into a single group counts whose tau values are within delta of one another
		C_tau_tol = dict()
		for tau in C_tau.keys():
			C_tau_tol.setdefault(tau,0)
			for i in xrange(tau-self.tol,tau+self.tol+1):
				C_tau_tol[tau] += C_tau[i] if C_tau.has_key(i) else 0


		# Step(3) computes the test threshold
		Period_cand = list()
		for tau in C_tau_tol.keys():
			LAMBDA = float(len(seq))/self.T
			P_tau = 2*self.tol*LAMBDA*math.e**(-LAMBDA*tau)
			threshold = math.sqrt(3.84*len(seq)*P_tau*(1-P_tau))+len(seq)*P_tau
			if C_tau_tol[tau] > threshold:
				Period_cand.append(tau)
			
		return Period_cand




	def DiscoverPPattern(self,event_cat,p):
		minsup = float(self.T)/p*self.alpha
		window = int(float(self.beta)*p)+1
		p_pattern_set = list()

		# prepare event_comb_w and event_comb_p 
		events = filter(lambda x:x[0] in event_cat,self.data)
		event_seq = list()
		for i in xrange(self.T):
			event_seq.append(filter(lambda x:x[1]>=i and x[1]<(i+window),events))
			event_seq[-1] = map(lambda x:x[0],event_seq[-1])
		event_seq = map(set,event_seq)

		start = window + p + self.tol

		event_comb_w = list()
		event_comb_p = list()
		for i in xrange(self.T):
			if (start+i)==self.T:
				break
			event_comb_w.append(event_seq[start+i])
			event_comb_p.append(event_seq[i])


		# count occurrences

		sup = dict()
		pp_list = list()

		for length in xrange(len(event_cat)+1):

			if length == 0:
				for comb in combinations(event_cat,1):
					occurrence = map(lambda x,y:1 if x.intersection(comb) == set(comb) and y.intersection(comb) == set(comb) else 0,event_comb_w,event_comb_p).count(1)
					if occurrence != 0:
						sup[tuple(sorted(comb))] = occurrence
				
			for comb,count in sup.items():
				if count > minsup:
					pp_list.append(comb)
			if len(pp_list) != 0:
				p_pattern_set.append(pp_list)
			self.level_sup.append(sup)

			sup = dict()
			for pp in pp_list:
				for ele in event_cat.difference(set(pp)):
					comb = tuple(sorted(set(pp).union(ele)))
					if comb not in sup.keys():
						occurrence = map(lambda x,y:1 if x.intersection(comb) == set(comb) and y.intersection(comb) == set(comb) else 0,event_comb_w,event_comb_p).count(1)
						if occurrence != 0:
							sup[comb] = occurrence

			pp_list = list()

			if len(sup) == 0:
				break
		
		return p_pattern_set



	def PeriodFirst(self,event_peri_cand):
		for period in event_peri_cand.keys():
			result = self.DiscoverPPattern(set(event_peri_cand[period]),period)
			if len(result) != 0:
				self.PP[period] = result
				

	def AssociationFirst(self):
		pass





def main():
	data = [
		("d",1),("a",2),("b",3),("c",3),("d",4),("c",5),("a",6),("d",6),("b",7),("c",7),("d",7),("a",10),("b",10),("c",12),("d",12),("d",13),("a",14),("b",14),("c",14),("c",16),("d",16),("a",18),("b",18),("d",20),
	]

	para = {
		"data":data,
		"tolerance":1,
		"confidence":0.95,
		"alpha":0.4,
		"beta":0.25
	}

	task = p_pattern(para)



if __name__ == '__main__':main()