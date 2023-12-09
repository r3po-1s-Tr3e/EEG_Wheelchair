#!/usr/bin/env python
# coding: utf-8

# In[74]:


import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]


letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

mat_contents = sio.loadmat('mat_files/'+filename+'.mat')
# d = mat_contents['ALLERP']['bindata'][0][0][3]
d = mat_contents['bindata'][3]

b=[]
for j in range(26):
  temp = []
  for i in range(300,600):
    temp.append(d[i][2*j]-d[i][2*j+1])
  b.append(temp)

###########peak_array############
peak_array = []
for i in range(26):
  peak_array.append(max(b[i]))

peak_array = np.array(peak_array)

res = peak_array.argsort()[-10:][::-1]
print(res)
# print('peak_array',peak_array)

for i in range(len(res)):
    print(letters[res[i]],end="  ")
print('\n')
###########avg_array###########


avg_array = []
for i in range(26):
  avg_array.append(sum(b[i])/400) 
# print('avg_array',avg_array)

avg_array = np.array(avg_array)

res = avg_array.argsort()[-15:][::-1]
print(res)


# print(letters[np.argmax(peak_array)],letters[np.argmax(avg_array)])

for i in range(len(res)):
    print(letters[res[i]],end="  ")

