"""
Make sure the python interpreter for Spyder is the conda environment for `oct-cbort` library.
That conda environment must also have `spyder-kernels` installed.

ref. https://github.com/spyder-ide/spyder/wiki/Working-with-packages-and-environments-in-Spyder 

Stephanie Nam (snam@alum.mit.edu)
"""

#Import required system libraries for file management
import sys,importlib,os

pc_path = 'C:\\Users\\vlab_eye\\Documents\\local_repo' #
# pc_path = 'C:\\Users\\UCL-SPARC\\Documents\\GitHub'
# Provide path to oct-cbort library
module_path = os.path.abspath(os.path.join(pc_path, 'oct-cbort'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
# Import oct-cbort library
from oct import *

# Import additional libraries
import shutil, time


#%% Load data
# session_name = '[p.Chicken052621][s.SANsChicken_smallV][05-26-2021_13-11-59]'
# path_dir = os.path.join(os.getcwd(), 'example_data', session_name)
path_dir = r'D:\OFDIData\legacy_pstest\[p.ps_test][s.phantom_noglass][10-14-2021_13-44-20]'
data = Load(directory = path_dir)
data.loadFringe(frame=5)


# #%%
# ch1 = np.array(data.ch1.get())
# ch2 = np.array(data.ch2.get())
# bg1 = np.array(data.bg1)
# bg2 = np.array(data.bg2)

# fig, ax = plt.subplots(1,1)
# ax.plot(ch1[:,1])
# ax.plot(bg1[:,1], 'k')

# fig, ax = plt.subplots(1,1)
# ax.plot(ch2[:,2])
# ax.plot(bg2, 'k')
# #%%
# fig, ax = plt.subplots(1,1)
# ax.plot(ch1[:,1] - bg1[:,1])
# ax.plot(ch2[:,1] - bg2[:,1])
# plt.show()

# sys.exit()
#%% Tomogram processing : complex tomogram, k-space fringe, stokes vectors  
data.reconstructionSettings['processState'] = 'struct+angio+ps+stokes+hsv'#'+kspace'
data.reconstructionSettings['spectralBinning'] = True
# data.reconstructionSettings['depthIndex'] = [950, 950+1024]
data.reconstructionSettings['binFract'] = 3
# data.reconstructionSettings['demodSet'] = [0.5, 0.0, 1.0, 0.0, 0.0, 0.0]

# data.processOptions['OOPAveraging'] = True
# data.processOptions['correctSystemOA'] = True


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

#%%



#%% Structure processing
data.structureSettings['contrastLowHigh'] = [0,195]# [-50, 160]
struct_obj = Structure(mode='log')
struct_out = struct_obj.reconstruct(data=data)
for key,val in struct_out.items():
    data.processedData[key] = struct_out[key]
    
print("struct_out.keys() >> ", struct_out.keys())
plt.imshow(cp.asnumpy(struct_out['struct']), aspect ='auto', cmap='gray')


#%% PS processing
data.psSettings['zOffset'] = 10 # this is deltaZ for differential calculation
data.psSettings['oopFilter']  = 2
data.psSettings['xFilter'] = 15
data.psSettings['zFilter']  = 3
data.psSettings['dopThresh'] = 0.85
data.psSettings['maxRet'] = 100
data.psSettings['binFract'] = data.reconstructionSettings['binFract']
data.psSettings['thetaOffset'] = 0

print(data.psSettings)
ps = Polarization('sb') # Polarization('sb')
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
plt.show()

SVF1, SVF2, SVN1, SVN2, QUV1, QUV2 = filtNormStokes(data.processedData['sv1'],
                                                    data.processedData['sv2'],
                                                    stokesFilter=ps.filter)

sys.exit()

#%%
"""
import napari

# Looking at QUV (filtered and normalized)
viewer = napari.Viewer()
viewer.add_image(cp.asnumpy(SVN1), name='SVN1', rgb=False, contrast_limits=(-1,1) )
viewer.add_image(cp.asnumpy(SVN2), name='SVN2', rgb=False, contrast_limits=(-1,1) )
viewer.add_image(cp.asnumpy( data.processedData['dop']/255), name='dop', contrast_limits=(0,1), rgb=False)
viewer.add_image(cp.asnumpy( data.processedData['struct']/255), name='nlog_struct', contrast_limits=(0,1), rgb=False)
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
data.reconstructionMode = {'tom': 'heterodyne', 
                           'struct': 'log', 
                           'angio': 'cdv', 
                           'ps': 'sym'}


data.generateEditSettings()
src = os.path.join(path_dir, 'editsettings.ini')
dst = os.path.join(path_dir, 'settings', 'spyder_used_editsettings.ini')
shutil.copy(src, dst)

# The data object still contains the settings parameters defined above carry over.
processor = Post()
processor.processFrameRange(data, procState='struct+ps+hsv', procAll=True, writeState=True)
                            # procAll=False, startFrame=1000, endFrame=1100, writeState=True)





#%%
disp_z =  np.arange(60) + 400 # np.arange(645,700) #
disp_x = np.array([750])

disp_SVN1 = cp.asnumpy(SVN1[disp_z, disp_x, :,  (data.psSettings['binFract']-1)])
disp_SVN2 = cp.asnumpy(SVN2[disp_z, disp_x, :,  (data.psSettings['binFract']-1)])

fig = plt.figure()
ax = plt.axes(projection='3d')

r = 1
phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0*np.pi:100j]
x = r*np.sin(phi)*np.cos(theta)
y = r*np.sin(phi)*np.sin(theta)
z = r*np.cos(phi)
ax.plot_surface(x, y, z,  rstride=1, cstride=1, color='c', alpha=0.1, linewidth=0)

# Data for a three-dimensional line
pdict_line1 = {'linewidth':0.5, 'color':'red'}
pdict_line2 = {'linewidth':0.5, 'color':'blue'}

ax.plot3D(disp_SVN1[:,0], disp_SVN1[:,1], disp_SVN1[:,2], **pdict_line1)
ax.plot3D(disp_SVN2[:,0], disp_SVN2[:,1], disp_SVN2[:,2], **pdict_line2)

# Data for three-dimensional scattered points
ax.scatter3D(disp_SVN1[:,0], disp_SVN1[:,1], disp_SVN1[:,2], c=disp_z, cmap='autumn')
ax.scatter3D(disp_SVN2[:,0], disp_SVN2[:,1], disp_SVN2[:,2], c=disp_z, cmap='winter')

