"""
The official quick start guide for h5py : https://docs.h5py.org/en/stable/quick.html 
"""
import sys,os
import numpy as np
from matplotlib import pyplot as plt
import h5py

#%% Create example array
array_example1 = np.zeros((11,3,7), dtype=np.float_)
b_good_practice = False


if b_good_practice: # faster with numpy's n dimensional looping
    for aa,bb,cc in np.ndindex(array_example1.shape):
        array_example1[aa,bb,cc] = aa+10*bb+100*cc
else:
    for aa in range(array_example1.shape[0]):
        for bb in range(array_example1.shape[1]):
            for cc in range(array_example1.shape[2]):
                array_example1[aa,bb,cc] = aa+10*bb+100*cc
            

if b_good_practice: # need to always close file object
    with h5py.File('myfile.hdf5','w') as hdf:
        dset = hdf.create_dataset('array_example1', data=array_example1)
        dset.attrs.create('dim1', (array_example1.shape[0]))
        dset.attrs.create('dim2', (array_example1.shape[1]))
else:
    hdf = h5py.File('myfile.hdf5','w')
    dset = hdf.create_dataset('array_example1', data=array_example1)
    dset.attrs.create('dim1', (array_example1.shape[0]))
    dset.attrs.create('dim2', (array_example1.shape[1]))
    hdf.close()


#%% h5 file object works like a Python Dictionary
hdf = h5py.File('myfile.hdf5','r')

print("f.keys() >> ", hdf.keys())
print("f['array_example1'].attrs.keys() >> ", hdf['array_example1'].attrs.keys())

attrs_dict = {}
for key in hdf['array_example1'].attrs.keys():
    attrs_dict[key] = hdf['array_example1'].attrs[key]

# Load a part of HDF to an array (using Python indexing!)
array_slice = np.array(hdf['array_example1'][1::2,2,:3])  

# Array is automatically squeezed
print("array_slice.shape >> ", array_slice.shape)


hdf.close()