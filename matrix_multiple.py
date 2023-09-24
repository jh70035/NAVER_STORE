##
import numpy as np
a=np.array([[1,2],[3,4]])
b=np.array([[5,6],[7,8]])
# print(a,b)
c=np.dot(a,b)
print(c)
d=a@b
print(d)
e=np.array([1,2])
f=np.dot(a,e)
print(f)
g=a@e
print(g)
g.shape
type(g)
f.shape

e=np.array([[1,2]])
e.shape

a@e.