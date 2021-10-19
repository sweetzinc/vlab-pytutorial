"""
Make sure the python interpreter for Spyder is the conda environment for `oct-cbort` library.
That conda environment must also have `spyder-kernels` installed.

ref. https://github.com/spyder-ide/spyder/wiki/Working-with-packages-and-environments-in-Spyder 

Stephanie Nam (snam@alum.mit.edu)
"""

#Import required system libraries for file management
import sys,importlib,os

# pc_path = 'C:\\Users\\vlab_eye\\Documents\\local_repo' #
pc_path = 'C:\\Users\\UCL-SPARC\\Documents\\GitHub'
# Provide path to oct-cbort library
module_path = os.path.abspath(os.path.join(pc_path, 'oct-cbort'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
# Import oct-cbort library
from oct import *

# Import additional libraries
import shutil, time


#%% Load data
session_name = '[p.Chicken052621][s.SANsChicken_smallV][05-26-2021_13-11-59]'
path_dir = os.path.join(os.getcwd(), 'example_data', session_name)

data = Load(directory = path_dir)
data.loadFringe(frame=5)


#%%
ch1 = np.array(data.ch1.get())
ch2 = np.array(data.ch2.get())
bg1 = np.array(data.bg1)
bg2 = np.array(data.bg2)

fig, ax = plt.subplots(1,1)
ax.plot(ch1[:,1])
ax.plot(bg1[:,1], 'k')

fig, ax = plt.subplots(1,1)
ax.plot(ch2[:,2])
ax.plot(bg2, 'k')
#%%
fig, ax = plt.subplots(1,1)
ax.plot(ch1[:,1] - bg1[:,1])
ax.plot(ch2[:,1] - bg2[:,1])



#%% Tomogram processing : complex tomogram, k-space fringe, stokes vectors  
data.reconstructionSettings['processState'] = 'struct+angio+ps+kspace'
data.reconstructionSettings['spectralBinning'] = 1

tom = Tomogram(mode='heterodyne')
outtom = tom.reconstruct(data=data)
for key,val in outtom.items():
    data.processedData[key] = outtom[key]
    
    
print("outtom.keys() >> ", outtom.keys())
plt.imshow(cp.asnumpy(cp.log10(cp.abs(outtom['tomch1'][:,:]))), aspect ='auto', cmap='gray')

print("outtom['tomch1'].shape >> ", outtom['tomch1'].shape)
print("outtom['sv1'].shape >> ", outtom['sv1'].shape)
if outtom['k1'] is not None:
    print("outtom['k1'].shape >> ", outtom['k1'].shape)

#%% Structure processing
data.structureSettings['contrastLowHigh'] = [-50, 160]
struct_obj = Structure(mode='log')
struct_out = struct_obj.reconstruct(data=data)
for key,val in struct_out.items():
    data.processedData[key] = struct_out[key]
    
print("struct_out.keys() >> ", struct_out.keys())
plt.imshow(cp.asnumpy(struct_out['struct']), aspect ='auto', cmap='gray')


#%% PS processing
data.psSettings['zOffset'] = 15 # this is deltaZ for differential calculation
ps = Polarization('sb')
outps = ps.reconstruct(data=data)
for key,val in outps.items():
    data.processedData[key] = outps[key]
    
print("outps.keys() >> ", outps.keys())

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(221)
ax.imshow(data.processedData['dop'], cmap='gray', aspect='auto')
ax = fig.add_subplot(222)
ax.imshow(data.processedData['ret'], cmap='gray', aspect='auto')
ax = fig.add_subplot(223)
ax.imshow(data.processedData['theta'], aspect='auto')
ax = fig.add_subplot(224)
ax.imshow(data.processedData['oa'], aspect='auto')


# SVF1, SVF2, SVN1, SVN2, QUV1, QUV2 = filtNormStokes(data.processedData['sv1'],
#                                                     data.processedData['sv2'],
#                                                     stokesFilter=ps.filter)


sys.exit()
#%%
"""
import napari

# Looking at QUV (filtered and normalized)
viewer = napari.Viewer()
viewer.add_image(cp.asnumpy(SVN1), name='SVN1', rgb=False, contrast_limits=(-1,1) )
viewer.add_image(cp.asnumpy(SVN2), name='SVN2', rgb=False, contrast_limits=(-1,1) )


viewer2 = napari.Viewer()
viewer2.add_image(cp.asnumpy( data.processedData['dop']/255), name='dop', contrast_limits=(0,1), rgb=False)
viewer2.add_image(cp.asnumpy( data.processedData['struct']/255), name='nlog_struct', contrast_limits=(0,1), rgb=False)

%matplotlib qt 
"""


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

# The data object still contains the settings parameters defined above carry over.
processor = Post()
processor.processFrameRange(data, procState='struct+ps', procAll=False, 
                            startFrame=2, endFrame=3, writeState=True)