# Short python and OCT-CBORT tutorial

This markdown note is prepared for `oct-cbort` python tutorial at CBORTT
by Stephanie Nam (snam@alum.mit.edu)

## Python Package for OCT

Vakoc Lab Repositiory [oct-cbort](https://github.com/BenVakocLab/oct-cbort), requires collaborator access. 

* MUST have two-factor authentication.
* Send github username to me in order to get access.  
* Use **Anaconda Prompt** on Windows, or terminal on Mac.

### Practical usage example 1. Using Jupyter notebook
```
conda activate oct38-gpu
cd C:\Users\UCL-SPARC\Documents\GitHub\test-cbort\damon_tutorials
jupyter lab
```
`shift-enter` to execute the code cell

### Practical usage example 2. Using SPYDER
```
conda activate spyerenv
spyder
```

```
fringe = cp.asnumpy(data.ch1)
bg = cp.asnumpy(data.bg1)
plt.plot(fringe[:,0])
plt.plot(bg[:,0])
```

## SPYDER Introduction
For setup, follw https://github.com/sweetzinc/vlab-pytutorial

### OCT-CBORT scripting on spyder
