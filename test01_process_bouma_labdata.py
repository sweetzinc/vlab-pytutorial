"""
Make sure the python interpreter for Spyder is the conda environment for `oct-cbort` library.
That conda environment must also have `spyder-kernels` installed.

ref. https://github.com/spyder-ide/spyder/wiki/Working-with-packages-and-environments-in-Spyder 

Stephanie Nam (snam@alum.mit.edu)
"""

#Import required system libraries for file management
import sys,importlib,os

# Provide path to oct-cbort library
module_path=os.path.abspath('C:\\Users\\vlab_eye\\Documents\\local_repo\\oct-cbort')
if module_path not in sys.path:
    sys.path.append(module_path)

# Import oct-cbort library
from oct import *

# Import additional libraries
import shutil, time


#%% Load data
path_dir = r'D:\OFDIData\temp_jian\[Test][08-12-2021_15-57-11]'

data = Load(directory = path_dir)
data.loadFringe(frame=1)

sys.exit()
#%%
ch1 = data.ch1.get()
ch2 = data.ch2.get()
bg1 = data.bg1.get()
bg2 = data.bg2.get()

fig, ax = plt.subplots(1,1)
ax.plot(ch1[:,1])
ax.plot(bg1[:,1], 'k')

fig, ax = plt.subplots(1,1)
ax.plot(ch2[:,2])
ax.plot(bg2, 'k')
#%% Tomogram processing : complex tomogram, k-space fringe, stokes vectors  
data.reconstructionSettings['processState'] = 'struct+kspace'
data.reconstructionSettings['spectralBinning'] = 1

tom = Tomogram(mode='heterodyne')
outtom = tom.reconstruct(data=data)
for key,val in outtom.items():
    data.processedData[key] = outtom[key]
    
    
print("outtom.keys() >> ", outtom.keys())
plt.imshow(cp.asnumpy(cp.log10(cp.abs(outtom['tomch1'][:,:]))), aspect ='auto', cmap='gray')

print("outtom['tomch1'].shape >> ", outtom['tomch1'].shape)


#%% Structure processing
data.structureSettings['contrastLowHigh'] = [50, 300]
struct_obj = Structure(mode='log')
struct_out = struct_obj.reconstruct(data=data)
for key,val in struct_out.items():
    data.processedData[key] = struct_out[key]
    
print("struct_out.keys() >> ", struct_out.keys())
plt.imshow(cp.asnumpy(struct_out['struct']), aspect ='auto', cmap='gray')

sys.exit()

#%% Process and save the whole volume
# Set up logging to print on Spyder console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.__dict__

# Initialize the post processor. 
# Write editsettings.ini file and copy to the settings folder
data.generateEditSettings()
src = os.path.join(path_dir, 'editsettings.ini')
dst = os.path.join(path_dir, 'settings', 'used_editsettings.ini')
shutil.copy(src, dst)

time_start = time.time()
# The data object still contains the settings parameters defined above carry over.
processor = Post()
processor.processFrameRange(data, procState='struct', procAll=True, writeState=True)
                            # startFrame=2, endFrame=3,  writeState=True)
time_end = time.time()
print(f"processing time: {time_end-time_start}s")