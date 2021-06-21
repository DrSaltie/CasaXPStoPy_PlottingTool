# CasaXPStoPy_PlottingTool
Publishable XPS plots without the suffering

#import plotting and robust maths modules
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import re
import astropy
import os
import sys
import time
from astropy.io import ascii
from astropy import units as u
from astropy.visualization import quantity_support
quantity_support()

# Wish list
# Done - keep multiple plots open at once
# - make it display in a UI with input boxes
# Done - Ability to choose the colours for components somehow (so that we can ensure, e.g., that the individual C1s components, e.g, sp2 carbon, always have the same colour assignment even if the number of fitted components changes.)
# -	Documentation :)

filePath = input("File path and file name (e.g. E:\\me\\...\\my_ColumnsOfTables_ASCII_file): ") 
CASAfile = open(filePath, "r")
data = CASAfile.readlines()
lineCount = 0
indexes = np.zeros(0)
for line in data:
	if line.find('C') == 0 or line.find('K') == 0: #"Cycle" == data[lineCount] or "K.E." == data[lineCount]
		indexes = np.append(indexes,lineCount) 
	lineCount += 1
indexes = np.append(indexes, lineCount)
n = round(len(indexes)/2)
energy = input("K.E. (1) or B.E. (2)? ")
if energy in ("K.E.", "ke", "1"):
	energy = "K.E."
elif energy in ("B.E.", "be", "2"):
	energy = "B.E."
else:
	sys.exit("please restart and choose an energy scale.")
scale = input("Intensity (1) or CPS (2)? ")
if scale in ("intensity", "Intensity", "1"):
	scale = "Counts"
elif scale in ("CPS", "cps", "2"):
	scale = "CPS"
else:
	sys.exit("please restart and choose a count scale.")
for r in range(1, n): 
	i = indexes[r*2-1].astype(int)	#call indexes[odd int]
	j = indexes[r*2].astype(int)	#call indexes[even int]
	out = ascii.read(data[i:j], format='tab', guess=False, fast_reader=False)
	namesRaw = data[i]
	namesRaw = namesRaw.split("\t")
	names = list(filter(None, namesRaw)) #sets up the names list, otherwise not really needed as the range 'p' below is from 'numOfFits' that dosnt count the null value regardless
	names[len(names)-1] = "Envelope CPS" #needs this to call the data in column "Envelope CPS" because "Envelope CPS\n" from namesRaw wont work
	if scale == "Counts":
		numOfFits = range(1, namesRaw.index("Envelope")+1) 
	elif scale == "CPS":
		numOfFits = range(namesRaw.index("CPS")-1, namesRaw.index("Envelope CPS\n"))
		for n in range(namesRaw.index("CPS"), namesRaw.index("Background CPS")-1):
			ree = names[n]
			names[n] = ree.replace(names[n], names[n]+"_1") #the CPS data is denoted by an additional _1 but not in the headers 'names' list so have to manually add some how
	count = 0
	for p in numOfFits:
		if count == 0:
			points = np.array([out[names[p]]])
		else:
			points = np.append(points, np.array([out[names[p]]]), axis=0)
		count += 1
	energyax = np.array(out[energy])
	bec = 0
	fig, ax = plt.subplots()
	for x in range(0, len(points)):
		if x in range(namesRaw.index("Counts"), namesRaw.index("Background")-1): #just a hacky way of making sure the points relating to the deconvolution are the only ones filled in
			colour = input("Choose a colour to fill peak " + names[x+1] + ". Red(#ff0000) and black(#000000) are natively set to CPS/intensity, background and envelope. (Google \"hex colour\" for a useful tool): ")
			ax.fill_between(energyax, points[x], points[namesRaw.index("Background")-1], label=names[x+1], color=colour)
			ax.legend()
		else:
			BEC = ['#ff0000', '#000000', '#000000']
			ax.plot(energyax, points[x], label=names[x+1], color=BEC[bec])
			ax.legend()
			ax.set_xlabel(energy + ' (eV)')
			ax.set_ylabel(scale)
			bec += 1		
plt.show()	
