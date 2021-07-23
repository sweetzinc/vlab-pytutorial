# Short python and OCT-CBORT tutorial

This repository is prepared for `oct-cbort` python tutorial at Vakoc Group
by Stephanie Nam (snam@alum.mit.edu)

## Opening
We’ve discussed the advantages of transitioning our post-processing framework from MATLAB to python, I wanted to have a short hands-on session (~1hr) to nudge you to take that first step of transitioning to python. You will bring your laptop and I will:

1. Introduce SPYDER, an environment similar to MATLAB user interface
2. Give overview of similarities and differences using Numpy and MATLAB for OCT processing
3. Show example workflow of OCT-CBORT library
4. Discuss good practices (using Git and h5 file format)


## Prerequisites
The oct-cbort python tutorial is scheduled as a topic for Vakoc Lab group meeting on Fri, 07/23 at 2pm. We will meet at Deutsch conference room - please bring your laptops with all required installations to get the most out of this session. Zoom link will be available too. 
In the following installations, I recommend just using default settings. Just talk to me if you have questions. 

1. Install Anaconda (https://www.anaconda.com/products/individual)
2. Create a github user account and become a member of BenVakocLab teams.
3. If you are not familiar with Git, install GitHub Desktop (https://desktop.github.com/).  Link your user account to the application (just log in form the app).
4. Download the example data (https://www.dropbox.com/s/now7z1465jtqbtm/example_data.zip?dl=0)

Disclaimer: 
I do not consider my python to be “industry standard”, I learned python on my own (through books, various online resources and countless trial and errors), so what I cover today is what I think would have made it easier for me if someone spent a dedicated hour to help me get started on python as a Matlab user.



## Spyder and Python
For windows, I recommend using Anaconda Prompt. For MacOS, standard terminal works. GUIs exist, but a lot of tutorials on the internet already assume that you know basics of the commandline interface, so we use it on the tutorial. 


### Install

* Anaconda prompt and Conda's "environments"
* Compare `pip install` vs. `conda install`

```bash
# Create conda environment
conda create -n spyderenv python=3.8

# Activate your environment
conda activate spyderenv

# Install basic libraries
conda install numpy scipy matplotlib h5py
conda install spyder=5.0.5 

# Run SPYDER
spyder
```


### Introduce SPYDER and python

[SPYDER](https://www.spyder-ide.org/) provides similar user interface to MATLAB. You can

* See the variables
* Work on console
* Have breakpoints and debug
* Work with 'cells' with `#%%` and `shift+enter`

The following shows a brief comparison of the syntax. 
Files are included: `ex01_matlab.m` and `ex01_python.py`

```matlab
% MATLAB's basic datatype is a vector
a = [1,2,3,4]
b = 2*a

% MATLAB looping syntax needs `end`
for c = ['q','u','v']
disp(['c: ', c]);
end

% MATLAB can create vectors with colons, and indexing starts with 1
x = 0:2:999;
y = sin(2*pi*x/250);
z = (x/100).^2;

disp(['x(1) = ', num2str(x(1))]);
disp(['x(end) = ', num2str(x(1))]);
disp(['length(x) = ', num2str(length(x))]);

% MATLAB uses built-in functions
figure;
subplot(2,1,1); plot(x,y);
subplot(2,1,2); plot(x,z);
```


```python
# Python's built-in data types are different. [] makes a list. You don't need ;
a = [1,2,3,4]
b = 2*a 

# Looping needs :, and proper indentation
for c in ['q','u','v']:
    print(f"c:{c}")

# For MATLAB like operations, we need Numpy and arrays
# Here the indexing starts with 0, ends with -1
import numpy as np
x = np.arange(0,1000,2)
y = np.sin(2*np.pi*x/250)
z = (x/100)**2

print(f"x[0] = {x[0]}")
print(f"x[-1] = {x[-1]}")
print(f"x.size = {x.size}")


# For plotting, we need matplotlib
from matplotlib import pyplot as plt
fig = plt.figure(1)
plt.subplot(2,1,1)
plt.plot(x, y)
plt.subplot(2,1,2)
plt.plot(x, z)
```



## OCT-CBORT
1. From github app, clone `oct-cbort`
2. Install for cpu processing. (Create a new environment) 
3. Create a separate folder outside the repository, copy the tutorials
4. Launch Jupyter Notebook and run Damon's tutorial
5. Clone [this](https://github.com/sweetzinc/vlab-pytutorial) repository for scripting example.
2. Install for cpu processing. 
```bash
# Follow Damon's readme. Go to repository directory
conda crate --name oct38-cpu python=3.8
conda activate oct38-cpu
pip install -r requirements.txt
```
3. Create a separate folder outside the repository, copy the tutorials
4. Launch Jupyter Notebook and run Damon's tutorial
```bash
jupyter notebook
```
5. Clone Stephanie's test-cbort for scripting example.
6. Go to Spyder, change the python interpreter, run Stephanie's example for VakocLab's legacy chicken nerve dataset. 


## HDF 
Hierarchical Data Format (HDF) can be advantageous for storing our data. 
* Flexible slicing when opening multi-dimensional dataset
* Storing metadata 
* Grouping different data groups
* ImageJ compatibility (with a plugin)

Advantages are well explained at the [official website](https://www.hdfgroup.org/solutions/hdf5/).


## Git 
From GitHub App, see the changes made to the example python file. 
Fetch to obtain all example files I've shown you today. 




## Useful resources

1. MATLAB vs. Numpy - Numpy's official documentation (https://numpy.org/doc/stable/user/numpy-for-matlab-users.html)
2. Python Data Science Handbook - cool e-book with lots of plotting examples (https://jakevdp.github.io/PythonDataScienceHandbook/)
