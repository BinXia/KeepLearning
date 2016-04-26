#coding=utf-8
import numpy as np



# numpy array (数组实例)
# flatten & micro for (铺平与简易循环实例)
# print np.array([[np.arange(1,31)]*4]).flatten()
# print np.array([np.arange(1,31) for x in range(4)]).flatten()


# map (map实例)
# print map(lambda x:max(x,0),[1,1,2,-1])
# filter (filter实例)
# def function(x):
# 	return x!=0
# print filter(function,[0,1,2,3,4,5,6,7,8,9])


# norm (范数实例)
# print np.linalg.norm([1,2,3],ord=2)


# sort (排序实例)
# a = [['a',1],['b',2],['c',3]]
# a.sort(key=lambda x:x[1],reverse=True)
# print a

# list (列表实例)
a = list([10,1,2,3,4,5,5,6,7,7,7])
# print a.count(8)
# zip (合并实例)
# print zip(a,a)
# set, intersection, union, difference (交集、并集、差集实例)
# print set(a).intersection(a)
# print set(a).union(a)
# print set(a).difference(a)

# dict (字典实例)
# a = {1:'a',2:'b',3:'c'}
# for x in a:
# 	print x


# mat (矩阵实例)
from scipy.sparse import coo_matrix
x = np.array([0,1,2,1])
y = np.array([0,1,2,2])
data = np.array([1,2,3,4])
# sparse mat (稀疏矩阵)
z = coo_matrix((data,(x,y)),shape=(3,3)).todense()
# SVD (SVD分解)
# (u,s,v) = np.linalg.svd(z)
# mat extension (矩阵扩展)
# print np.vstack((z,np.zeros((3,3))))
# print np.hstack((z,coo_matrix((3,3)).todense()))
# judge zero in a row (判断数组中全为零或全不为零)
# if np.array([[0]*3]).all():
# 	print 'all'
# if np.array([[0]*3]).any():
# 	print 'any'
# sum (求和实例)
print z
print np.sum(z,axis=0)*2

















