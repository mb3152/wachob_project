#!arch -i386 /usr/bin/python

"""
Download data from a Rigol DS1052E oscilloscope and graph with matplotlib.

Based on http://www.cibomahto.com/2010/04/controlling-a-rigol-oscilloscope-using-linux-and-python/
by Cibo Mahto and Ken Shirriff, http://righto.com/rigol
"""
import os, sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
from pyvisa.vpp43 import visa_library
visa_library.load_library("/Library/Frameworks/Visa.framework/VISA")
import visa
import time
from pylab import *
from scipy.ndimage.filters import gaussian_filter1d as smooth


recording_time = int(sys.argv[1])
ort = recording_time
recording_time = recording_time/5
file_name = str(sys.argv[2])
current_dir = os.getcwd()
os.system('mkdir %s/%s' %(current_dir,file_name))
sample_rate = 300
# Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
instruments = visa.get_instruments_list()
usb = filter(lambda x: 'USB' in x, instruments)
if len(usb) != 1:
    print 'Bad instrument list', instruments
    sys.exit(-1)

all_data = [] #all the data gets stored here
# collect the data from the tattoo machine
print 'Collecting data for %s' %(str(recording_time*5)) + ' minutes'
while recording_time > 0 :
    recording_time = recording_time - 1
    # Grab the raw data from channel 1
    scope = visa.instrument(usb[0], timeout=10^100, chunk_size=1024) # bigger timeout for long mem
    scope.write(":RUN")
    time.sleep(sample_rate)
    scope.write(":STOP")
    # Get the timescale
    timescale = scope.ask_for_values(":TIM:SCAL?")[0]

    # Get the timescale offset
    timeoffset = scope.ask_for_values(":TIM:OFFS?")[0]
    voltscale = scope.ask_for_values(':CHAN1:SCAL?')[0]

    # And the voltage offset
    voltoffset = scope.ask_for_values(":CHAN1:OFFS?")[0]

    # scope.write(":WAV:POIN:MODE RAW")
    rawdata = scope.ask(":WAV:DATA? CHAN1")[10:]
    data_size = len(rawdata)
    # sample_rate = scope.ask_for_values(':ACQ:SAMP?')[0]
    # print 'Data size:', data_size, "Sample rate:", sample_rate

    scope.write(":KEY:FORCE")
    scope.close()

    #Turns weird data into real data
    data = numpy.frombuffer(rawdata, 'B')

    # Walk through the data, and map it to actual voltages
    # Invert the data
    data = data * -1 + 255
    # Scope display range is actually 30-229.  So shift by 130 - the voltage offset in counts, then scale to get the actual voltage.
    data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale
    all_data.extend(data[:600])
    np.save('%s/%s_data' %(file_name,file_name), all_data)
    print 'Data saved! Collecting more...' + 'You have %s minutes left.' %(str(recording_time*5))

print 'Tattoo done, making the images now...'

# Plot the raw data
plt.plot(range(len(all_data)), all_data)
plt.title("Oscilloscope Channel 1")
plt.ylabel("Voltage (V)")
plt.xlabel("Time")
plt.savefig('%s/%s/%s_raw.pdf' %(current_dir,file_name,file_name),dpi=1000)

# Plot fancy data
all_data = np.array(all_data)
noise = np.random.normal(np.mean(all_data),(np.std(all_data)/3),len(all_data))
all_data = all_data + noise
x = smooth(all_data,sigma = np.std(all_data)*10)
grid = x.reshape(ort,-1)
figure(1)
imshow(grid, cmap = 'spectral', interpolation='gaussian')
plt.savefig('%s/%s/%s_fancy.pdf' %(current_dir,file_name,file_name),dpi=1000)

# Make movie!
def write_movie(data, fps=5):
    global x
    global current_dir
    global file_name
    print 'Making movie! Might take a bit of time (10-15 minutes). Be patient :)'
    name = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            name = name+1
            fname = '_tmp%06d.png'% name
            figure(1)
            image = data.copy()
            image[i+1:] = max(x) + 0.1
            image[i][j:] = max(x) + 0.1
            imshow(image, cmap = 'spectral', interpolation='gaussian')
            plt.savefig(fname) 
            plt.clf()
    os.system("ffmpeg -r "+str(fps)+" -b %s " %name +  '-i _tmp%06d.png movie.mp4')
    os.system("rm _tmp*.png")
    os.system('mv movie.mp4 /%s/%s/' %(current_dir,file_name))
write_movie(grid,40)

print 'All Done! Files are saved in %s/%s/' %(current_dir,file_name)


