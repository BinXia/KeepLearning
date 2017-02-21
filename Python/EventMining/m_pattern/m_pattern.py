#coding=UTF-8
import numpy as np
import pprint
pp = pprint.PrettyPrinter()
from itertools import combinations




class m_pattern(object):
	"""docstring for m_pattern"""
	def __init__(self, para):
		super(m_pattern, self).__init__()
		self.data = para["data"]
		self.minp = para["minp"]

		self.level_sup = list()			# Store supports of combinations in different levels

		event_comb,event_cat = self.Preprocessing()
		self.MP = self.DiscoverMPattern(event_comb,event_cat)


	def Preprocessing(self):
		event_comb = []
		event_cat = set()
		for datum in self.data:
			event_comb.append(set(datum))
			event_cat = event_cat.union(event_comb[-1])

		return (event_comb,event_cat)



	def isMPattern(self,comb,count):
		for item in comb:
			if float(count)/self.level_sup[len(item)-1][tuple(item)] < self.minp:
				return False
		return True


	def DiscoverMPattern(self,event_comb,event_cat):
		
		m_pattern_set = list()

		for length in xrange(len(event_cat)+1):
			sup = dict()
			mp_list = list()

			if length < 2:
				for comb in combinations(event_cat,length+1):
					occurrence = map(lambda x:1 if x.intersection(comb) == set(comb) else 0,event_comb).count(1)
					if occurrence != 0:
						sup[tuple(sorted(comb))] = occurrence
			else:
				for comb,count in self.level_sup[length-1].items():
					if self.isMPattern(comb,count):
						mp_list.append(comb)

				# mp_cand = list()
				# for mp in mp_list:
				# 	for ele in event_cat.difference(set(mp)):
				# 		comb = tuple(set(mp).union(ele))
				# 		mp_cand.append(comb)
				# for comb in mp_cand:
				# 	sup[comb] = 0
				# 	for item in comb:
				# 		if float(self.level_sup[len(comb)-2][tuple(sorted(set(comb).difference(item)))])/self.level_sup[0][tuple(item)] < self.minp:
				# 			del sup[comb]
				# 			break
				# for comb in sup.keys():
				# 	occurrence = map(lambda x:1 if x.intersection(comb) == set(comb) else 0,event_comb).count(1)
				# 	if occurrence != 0:
				# 		sup[comb] = occurrence

				for mp in mp_list:
					for ele in event_cat.difference(set(mp)):
						comb = tuple(sorted(set(mp).union(ele)))
						if comb not in sup.keys():
							occurrence = map(lambda x:1 if x.intersection(comb) == set(comb) else 0,event_comb).count(1)
							if occurrence != 0:
								sup[comb] = occurrence

				if len(sup) == 0:
					break

				m_pattern_set.append(mp_list)
			self.level_sup.append(sup)
		return m_pattern_set
		

def main():
	data = [
		["a","b","c","d","e","f","g"],
		["d","f","g"],
		["a","b","d","g"],
		["a","d","g"],
		["f","g"],
		["e","f","g"],
		["e","g"],
	]

	para = {
		"data":data,
		"minp":0.5
	}

	task = m_pattern(para)
	print task.MP



if __name__ == '__main__':main()