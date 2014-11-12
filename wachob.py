#!arch -i386 /usr/bin/python

"""
Download data from a Rigol DS1052E oscilloscope and graph with matplotlib.
By Ken Shirriff, http://righto.com/rigol

Based on http://www.cibomahto.com/2010/04/controlling-a-rigol-oscilloscope-using-linux-and-python/
by Cibo Mahto.
"""
import matplotlib.cm as cm
import numpy
import matplotlib.pyplot as plt
import sys
from pyvisa.vpp43 import visa_library
visa_library.load_library("/Library/Frameworks/Visa.framework/VISA")
import visa
import time
from pylab import *

all_data = []
all_time = []
iterations = 0
recording_time = 60
# Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
instruments = visa.get_instruments_list()
usb = filter(lambda x: 'USB' in x, instruments)
if len(usb) != 1:
    print 'Bad instrument list', instruments
    sys.exit(-1)
scope = visa.instrument(usb[0], timeout=10^100, chunk_size=1024) # bigger timeout for long mem
# Grab the raw data from channel 1
scope.write(":RUN")
time.sleep(recording_time)
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
sample_rate = scope.ask_for_values(':ACQ:SAMP?')[0]
print 'Data size:', data_size, "Sample rate:", sample_rate

scope.write(":KEY:FORCE")
scope.close()

#Turns weird data into real data
data = numpy.frombuffer(rawdata, 'B')

# Walk through the data, and map it to actual voltages
# Invert the data
data = data * -1 + 255
# Scope display range is actually 30-229.  So shift by 130 - the voltage offset in counts, then scale to get the actual voltage.
data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale
# Now, generate a time axis.
time = numpy.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data))
 
# See if we should use a different time axis
if (time[-1] < 1e-3):
    time = time * 1e6
    tUnit = "uS"
elif (time[-1] < 1):
    time = time * 1e3
    tUnit = "mS"
else:
    tUnit = "S"
# Plot the data
plt.plot(range(len(data)), data)
plt.title("Oscilloscope Channel 1")
plt.ylabel("Voltage (V)")
plt.xlabel("Time")
plt.show()
methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

grid = data.reshape(20,30)

figure(1)
imshow(grid, cmap = 'gist_rainbow', interpolation='nearest')
plt.show()
1/0



from PIL import Image
i = Image.open("amandawachob5.jpg")

pixels = i.load() # this is not a list, nor is it list()'able
width, height = i.size

all_pixels = []
for x in range(width):
    for y in range(height):
        cpixel = pixels[x, y]
        all_pixels.append(cpixel)


image_man_data = []
while len(image_man_data) < len(new_image):
	for x in image_data:
		image_man_data.append(x)


for i in range(len(image_array)):
	image_array[i] = image_array[i][0] * image_man_data[i],image_array[i][1] * image_man_data[i],image_array[i][2] * image_man_data[i]

