# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:27:50 2020

@author: SIAR
"""

#Bibliotek
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import color_chooser
import numpy as np
import math
import os 


#Path definering
Mappenavn = 'Plots'
basepath = os.path.abspath(Mappenavn)


#Valg af Excel-filer
root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)
files = filedialog.askopenfilename(multiple=True) 
#%gui tk
var = root.tk.splitlist(files)

filePaths = []
for f in var:
  filePaths.append(f)
filePaths

filesNames = []
for x in range(len(filePaths)):
  tempNames = '\\'.join(filePaths[x].split('/'))
  filesNames.append(tempNames)
  
#Udtagning af data - Her fravælges blandt andet i Common_names ting, der ikke findes relevant - Dette kan tilføjes
data=[pd.read_excel(path) for path in filesNames]
Common_names =["X", "Varmeforbrug", "Samlet behov", "Lagertab"]
data_reduced = data
allLabels = []     

Timer=range(0,data[0].shape[0])
   
#Specifik lagring af data til brug i plots senere

for i in range(len(filesNames)):
    data[i] = data[i].apply(lambda x: pd.Series(x.dropna().values))
    data[i] = data[i].dropna(axis=1, how='all')
    globals()['dm%s' % i] = data[i].values
    globals()['names%s' % i] = globals()['dm%s' % i][0,:]
    data[i].columns = globals()['names%s' % i]
    globals()['dm_varmeforbrug%s' % i] = data[i]["Varmeforbrug"].values
    globals()['dm_varmeforbrug_values%s' % i] = globals()['dm_varmeforbrug%s' % i][1:globals()['dm_varmeforbrug%s' % i].shape[0]]
    globals()['VF%s' % i] = globals()['dm_varmeforbrug_values%s' % i].tolist()
    for String in Common_names:
        data_reduced[i] = data_reduced[i].drop([String],axis = 1)
    globals()['dm_reduced%s' % i] = data_reduced[i].values
    globals()['Used_names%s' % i] = globals()['dm_reduced%s' % i][0,1:globals()['dm_reduced%s' % i].shape[1]]
    globals()['Values%s' % i] = globals()['dm_reduced%s' % i][:,1:globals()['dm%s' % i].shape[1]]
    globals()['Values%s' % i] = globals()['Values%s' % i][1:globals()['Values%s' % i].shape[0],:]
    globals()['label%s' % i] = globals()['Used_names%s' % i]
    allLabels.extend(globals()['label%s' % i].tolist())
    
    globals()['m%s' % i] = []
    for k in range(0,globals()['Values%s' % i].shape[1]):
            globals()['Values_list%s' % i] = globals()['Values%s' % i][:,k].tolist()
            globals()['m%s' % i].append(globals()['Values_list%s' % i])
            


Index = globals()['dm_reduced%s' % 0][:,0]
Index = Index[1:Index.size]


#-------------- Farver -----------------------------------------------
allLabels = list(set(allLabels))

allLabelUser = allLabels
allLabelUser.sort()


canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

MsgBox = tk.messagebox.askquestion ('Farver','Vil du vælge farver til plots?',icon = 'question')
if MsgBox == 'yes':

    colors = [(250, 0, 0), (0, 250, 0), (0, 0, 250), (255, 255, 255)] * 4

    colorSaver = []
    print(f'Der skal vælges farve for ',allLabelUser)
    for Labels in allLabelUser:
        print(f'Vælg farve for ',Labels)
        chooser = color_chooser.ColorChooser()
        result_color = chooser.askcolor(colors)
        colorSaver.append(result_color)

    def RGB(color1): return '#%02x%02x%02x' % (color1)
    farverBrugt = []
    for farver in colorSaver:
        farverBrugt.append(RGB(farver))

    for i in range(len(filesNames)):
        globals()['colorsForYou%s' % i] = []
        for k in range(len(globals()['label%s' % i])): 
            globals()['colorsForYou%s' % i].append(farverBrugt[allLabelUser.index(globals()['label%s' % i][k])])
else:
    farverBrugt = []
    print('Ingen farver valgt')
#---------------------------------------------------------------------

# Plots laves her
for i in range(len(filesNames)):
    plt.figure()
    plt.rc('axes', axisbelow=True)
    plt.grid()
    hfont = {'fontname':'Verdana'}
    plt.axis([0, 8760, 0, math.ceil(np.amax(globals()['dm_varmeforbrug_values%s' % i])/5)*5])
    plt.xlabel('Timer på året', **hfont)
    plt.ylabel('Varmekapacitet, MW', **hfont)

    plt.plot(range(0,len(globals()['VF%s' % i])),globals()['VF%s' % i], label = "Varmebehov", color = "sandybrown", alpha=0.6)
    if farverBrugt != []:
        plt.stackplot(range(0,len(globals()['VF%s' % i])),globals()['m%s' % i], labels = globals()['label%s' % i], colors = globals()['colorsForYou%s' % i])    
    else:    
        plt.stackplot(range(0,len(globals()['VF%s' % i])),globals()['m%s' % i], labels = globals()['label%s' % i])    
    
    ax = plt.subplot(111)
    
    ax.plot()
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height])
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
                        fancybox=True, shadow=True, ncol=4)
    
    plt.tight_layout()
    
    name = 'myfig' + str(i) + '.png'
    try:
        plt.savefig(os.path.join(basepath,name), format='png', dpi = 1200)
    except:
        print(f'Eksisterende path findes ikke - Opret mappe der hedder:"{Mappenavn}", således følgende path oprettes: {basepath}')




  