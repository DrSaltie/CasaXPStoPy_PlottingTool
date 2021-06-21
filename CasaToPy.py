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

#Run from CMD: py "E:\Archive\Mphil\Data\XPS\CasaToPy.py"
#path_to_file = E:\\Archive\\Mphil\\Data\\XPS\\Lab_2\\15_05_2019\\ag111_ 60_minutes_deposition_ColumnsOfTables

# Wish list
# Done - keep multiple plots open at once
# - make it display in a UI with input boxes
# Done - Ability to choose the colours for components somehow (so that we can ensure, e.g., that the individual C1s components, e.g, sp2 carbon, always have the same colour assignment even if the number of fitted components changes.)
# -	Documentation :)

#compile to .exe
#CMD: pyinstaller E:\Archive\Mphil\Data\XPS\CasaToPy.py

# Path = "E:\\ArchiveMasters\\Data\\XPS\\Lab_2\\15_05_2019\\"
# filelist = os.listdir(Path)
# for i in filelist:
	# if i.endswith(".txt"):
		# CASAfile = open(filePath, "r")
		# data = CASAfile.readlines()
		# lineCount = 0
		# indexes = []
		# for line in data:
			# #sindexes = line.find('C')
			# #print(indexes)
			# if line.find('C') == 0 or line.find('K') == 0: #"Cycle" == data[lineCount] or "K.E." == data[lineCount]
				# print(lineCount)
				# indexes.append(lineCount) 
			# lineCount += 1
			# #data += line+"\n"
		# #out=ascii.read(data[breaks], format='tab', guess=False, fast_reader=False)
		# print(indexes)
		# #print(i)

filePath = input("File path and file name (e.g. E:\\me\\...\\my_ColumnsOfTables_ASCII_file): ") 
#filePath = "E:\\ArchiveMasters\\Data\\XPS\\Lab_2\\15_05_2019\\ag111_ 60_minutes_deposition_COT" #Testing fielpath
CASAfile = open(filePath, "r")
data = CASAfile.readlines()
lineCount = 0
indexes = np.zeros(0)
#print(indexes)
for line in data:
	if line.find('C') == 0 or line.find('K') == 0: #"Cycle" == data[lineCount] or "K.E." == data[lineCount]
		#print(lineCount)
		#print(type(lineCount) is int)
		#print(type(indexes) is list)
		indexes = np.append(indexes,lineCount) 
	lineCount += 1
#lineCount -= 1 #Reduce lineCount to be last desired line of CASAdata
indexes = np.append(indexes, lineCount)
#print(indexes)
n = round(len(indexes)/2)
#print(n)
energy = input("K.E. (1) or B.E. (2)? ")
if energy in ("K.E.", "ke", "1"):
	energy = "K.E."
	#print("1")
elif energy in ("B.E.", "be", "2"):
	energy = "B.E."
	#print("2")
else:
	sys.exit("please restart and choose an energy scale.")
	
scale = input("Intensity (1) or CPS (2)? ")
if scale in ("intensity", "Intensity", "1"):
	scale = "Counts"
	#print(1)
elif scale in ("CPS", "cps", "2"):
	scale = "CPS"
	#print(2)
else:
	sys.exit("please restart and choose a count scale.")

for r in range(1, n): 
	i = indexes[r*2-1].astype(int)	#call indexes[odd int]
	j = indexes[r*2].astype(int)	#call indexes[even int]
	#print(type(i))
	#print(i)
	#print(j)
	out = ascii.read(data[i:j], format='tab', guess=False, fast_reader=False)
	#print(data[i:j])
	#print(type(out))
	#print(out)
	
	namesRaw = data[i]
	namesRaw = namesRaw.split("\t")
	#print(type(namesRaw))
	#print(namesRaw)
	#print([i for i,x in enumerate(namesRaw) if not x])
	names = list(filter(None, namesRaw)) #sets up the names list, otherwise not really needed as the range 'p' below is from 'numOfFits' that dosnt count the null value regardless
	names[len(names)-1] = "Envelope CPS" #needs this to call the data in column "Envelope CPS" because "Envelope CPS\n" from namesRaw wont work
	#print(names)
	#print(list(range(namesRaw.index("CPS"), namesRaw.index("Background CPS")-1)))
	#for y in range(namesRaw.index("CPS"), namesRaw.index("Background CPS")-1):
	#	print(names[y])
	
	if scale == "Counts":
		numOfFits = range(1, namesRaw.index("Envelope")+1) 
	elif scale == "CPS":
		numOfFits = range(namesRaw.index("CPS")-1, namesRaw.index("Envelope CPS\n"))
		for n in range(namesRaw.index("CPS"), namesRaw.index("Background CPS")-1):
			ree = names[n]
			names[n] = ree.replace(names[n], names[n]+"_1") #the CPS data is denoted by an additional _1 but not in the headers 'names' list so have to manually add some how

	#print("scale: ", scale)
	#print("list headers: ", names)
	#print(namesRaw)
	#print(out)
	#points = [[]]
	#print(points)
	count = 0
	for p in numOfFits:
		#print(p)
		if count == 0:
			points = np.array([out[names[p]]])
		else:
			points = np.append(points, np.array([out[names[p]]]), axis=0)
		count += 1
	#print(len(points))
	#print("position of background in data: ", namesRaw.index("Background"))
	#print(points)
	#print(points[namesRaw.index("Background")])
	energyax = np.array(out[energy])
	#print(energyax)
	#print(energy)
	bec = 0
	fig, ax = plt.subplots()
	#ax.fill_between(energyax, points[0], points[namesRaw.index("Background")]) #actually gives between points[0] and the envelope because index's are shifted by 1 because points dose not include energy
	for x in range(0, len(points)):
		
		if x in range(namesRaw.index("Counts"), namesRaw.index("Background")-1): #just a hacky way of making sure the points relating to the deconvolution are the only ones filled in
			#print(x)
			#print(names[x+1])
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
		#plt.pause(1)
	#plt.figure()
plt.show()	
