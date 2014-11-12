"""
    CreateMovie( plotter, numberOfFrames)
    
    This function creates a movie called movie.mp4 in the current working directory
    which has a frame rate of 10 frames per second.
    
    Parameters:
    	plotter: This parameter is a function of the following form:
    				def plotter(frame_number)
    			 where frame_number is the current frame that needs to be plotted
    			 using the matplotlib.pyplot library.
    	numberOfFrames: The total number of frames in the movie.
    	fps: The frames per second. The default is 10.
    	
    Output:
    	The function will create a movie called movie.mp4. Make sure that you don't
    	have any files called movie.mp4 and _tmp*.png in the current working
    	directory because they will be deleted.
"""

def CreateMovie(plotter, numberOfFrames, fps=10):
	import os, sys
	import matplotlib.pyplot as plt

	for i in range(numberOfFrames):
		plotter(i)
		fname = '_tmp%05d.png'%i
		
		plt.savefig(fname)
		plt.clf()

	os.system("rm movie.mp4")
	os.system("ffmpeg -r "+str(fps)+" -b 1800 -i _tmp%05d.png movie.mp4")
	os.system("rm _tmp*.png")