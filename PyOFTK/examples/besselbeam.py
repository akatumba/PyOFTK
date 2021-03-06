# *********************************************
#	Bessel beam generation with a thin 
#   annular aperture
#	
#
#
#
#	Author: 	Martin Laprise
#		    	Universite Laval
#				martin.laprise.1@ulaval.ca
#                 
# *********************************************

import Image
import time
import pyfits
import pylab as pl
from numpy import *
from scipy import fftpack
from PyOFTK.freespace import *


premierStep = 1.0
dx = 0.00003
nbPoints = 1024
print "Largeur de la fenetre: " + str(nbPoints*dx*1e3) + " mm"
step = 15
dz = 2.0/step
champ_in = Image.open("data/annular_aperture.gif")
intensiteArchive = zeros([512,512,step])
champ_in_fld = zeros([1024,1024], complex)
tampon = list(champ_in.getdata())


for x in range(1024):
	for y in range(1024):
		champ_in_fld[x,y] = float(tampon[(1024*y)+x])

t1 = time.time()

# First step at 1.0
fkabcd.Prop(champ_in_fld, 632e-9, dx, 1.0, premierStep, 0.0, 1.0, 1.0 ,premierStep, 0.0, 1.0)

# Step from 0.2 to 0.7
for i in range(step):
	fkabcd.Prop(champ_in_fld, 632e-9, dx, 1.0, dz, 0.0, 1.0, 1.0 ,dz, 0.0, 1.0)
	intensiteArchive[:,:,i] = pow(abs(champ_in_fld),2)[256:512+256,256:512+256]

# Bench
elapsed = time.time() - t1
print "Processing time: " + str(elapsed) + " secondes" + "(" + str(elapsed/60) + " minutes)"

pl.imshow(pow(abs(champ_in_fld),2), aspect='equal', interpolation='bicubic')
pl.show()

