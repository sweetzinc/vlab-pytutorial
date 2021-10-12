#%%

#Import required system libraries for file management
import sys,importlib,os

# Provide path to oct-cbort library
# module_path = os.path.abspath(r'C:\Users\vlab_eye\Documents\local_repo\oct-cbort')
module_path = os.path.abspath(r'C:\Users\UCL-SPARC\Documents\GitHub\oct-cbort')
if module_path not in sys.path:
    sys.path.append(module_path)

# Import oct-cbort library
from oct import *

# Import additional libraries
import shutil

#%%
foldername = r'G:\cbort_testdata'
list_sessions = os.listdir(foldername)
print(list_sessions)
qq_session = 0
session_name = list_sessions[qq_session]
path_dir = os.path.join(foldername, session_name)

#%%
data = Load(directory = path_dir)
frame= 1 #int(data.scanSettings['numFrames']/2)
data.loadFringe(frame=frame)
print(f"Loaded frame:{frame}")


#%% Tomogram processing : complex tomogram, k-space fringe, stokes vectors  
data.reconstructionSettings['processState'] = 'struct+ps+kspace' #''angio+sv'
data.reconstructionSettings['spectralBinning'] = True

tom = Tomogram(mode='heterodyne')
outtom = tom.reconstruct(data=data)
for key,val in outtom.items():
    data.processedData[key] = outtom[key]
    
    
print("outtom.keys() >> ", outtom.keys())
plt.imshow(cp.asnumpy(cp.log10(cp.abs(outtom['tomch1'][:,:]))), aspect ='auto', cmap='gray')

print("outtom['tomch1'].shape >> ", outtom['tomch1'].shape)
if outtom['sv1'] is not None:
    print("outtom['sv1'].shape >> ", outtom['sv1'].shape)
if outtom['k1'] is not None:
    print("outtom['k1'].shape >> ", outtom['k1'].shape)

#%% Structure processing
data.structureSettings['contrastLowHigh'] = [-50, 130]
data.structureSettings['invertGray'] = False
struct_obj = Structure(mode='log')
struct_out = struct_obj.reconstruct(data=data)
for key,val in struct_out.items():
    data.processedData[key] = struct_out[key]
    
print("struct_out.keys() >> ", struct_out.keys())
plt.imshow(cp.asnumpy(struct_out['struct']), aspect ='auto', cmap='gray')


#%% Angiography processing
data.angioSettings['invertGray']=False

angiography = Angiography(mode='cdv')
aout = angiography.reconstruct(data=data)
for key,val in aout.items():
    data.processedData[key] = aout[key]
    
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(121)
ax.imshow(data.processedData['angio'],cmap='gray', aspect='auto')
ax = fig.add_subplot(122)
ax.imshow(data.processedData['weight'],cmap='gray', aspect='auto')

#%% PS processing
data.psSettings['zOffset'] = 2 # this is deltaZ for differential calculation
data.psSettings['xFilter'] = 11
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


sys.exit()

#%% Process and save the whole volume
# Set up logging to print on Spyder console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.__dict__


# Write editsettings.ini file and copy to the settings folder
# The data object still contains the settings parameters defined above carry over.
data.storageSettings['storageFileType'] = 'mgh' # 'h5' # this saves h5 file
data.generateEditSettings()
src = os.path.join(path_dir, 'editsettings.ini')
dst = os.path.join(path_dir, 'settings', 'used_editsettings.ini')
shutil.copy(src, dst)

# Initialize the post processor. 
time_start = time.time()
processor = Post()
processor.processFrameRange(data, procState='struct+ps+kspace+stokes', procAll=True, writeState=True) 
# processor.processFrameRange(data, procState='struct', startFrame=2, endFrame=2, writeState=True)

time_end = time.time()
print(f"processing time: {time_end-time_start}s")


#%% See the sessions
for session in list_sessions:
    print(session)
#%% Batch Processing : need to check the settings parameter 
for qq_session, session_name in enumerate(list_sessions):
# if True:
    path_dir = os.path.join(foldername, session_name)
    data = Load(directory = path_dir)
    frame_middle= int(data.scanSettings['numFrames']/2)
    # Define the settings.
    data.reconstructionMode = {'tom': 'heterodyne', 'struct': 'log', 'angio': 'cdv', 'ps': 'classic'}
    data.reconstructionSettings['spectralBinning'] = False
    
    data.structureSettings['contrastLowHigh'] = [-50, 130]
    data.structureSettings['invertGray'] = False
    
    data.psSettings['zOffset'] = 11 # this is deltaZ for differential calculation
    data.psSettings['xFilter'] = 15
    
    data.storageSettings['storageFileType'] = 'mgh' 
    
    # Save and copy the settings. 
    data.generateEditSettings()
    src = os.path.join(path_dir, 'editsettings.ini')
    dst = os.path.join(path_dir, 'settings', 'used_editsettings.ini')
    shutil.copy(src, dst)

    # Initialize the post processor and start processing
    time_start = time.time()
    processor = Post()
    # processor.processFrameRange(data, procState='struct+ps+stokes', procAll=True, writeState=True) 
    processor.processFrameRange(data, procState='struct+ps+stokes', 
                                startFrame=frame_middle-1, endFrame=frame_middle+3, writeState=True)
    time_end = time.time()
    print(f"session processed: {session_name}")
    print(f"processing time: {time_end-time_start}s")
        
    