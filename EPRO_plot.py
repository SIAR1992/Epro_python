# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:27:50 2020

@author: SIAR
"""

#Bibliotek--------------------------------------------------------------------------------------------
import tkinter as tk #Henter tkinter modulet, some indeholder Tk værktøjskassen, skal henters for at arbejde med pop-op vinduer
from tkinter import filedialog #Henter funktionen, der gør det muligt at arbejde med filedialogs, det er dem, hvor vi kan browse rundt og vælge filer
import pandas as pd #pandas og nympy er standard Python moduler, der indeholder mange vektor funktioner mm., som man kender det fra Matlab
import numpy as np #se overstående
import matplotlib.pyplot as plt #Er Pythons plotter modul, som indeholder en masse funktioner til at plotte med
#----------------------------------OBS!!!!---------------------------------------------------------------------
import color_chooser #Er en selv defineret class, SOM SKAL KØRES INDEN MODELLEN, ELLERS KAN DEN IKKE KØRER (Lav exception, der observerer om color_chooser er opdateret)
#--------------------------------------------------------------------------------------------------------------
import math #Standard Python modul med matematik funktioner hentes ind her
import os #OS modulet hjælper Python med funktioner til at arbejde rundt i Operative System (Computeren)
#-----------------------------------------------------------------------------------------------------

#Path (Sti) definering--------------------------------------------------------------------------------
Mappenavn = 'Plots' #OBS! - Definering af mappe, som figurer skal ligge i defineres det ikke, smider Python en besked om at den skal oprettes med pathen defineret for basepath
basepath = os.path.abspath(Mappenavn) #Pathen, som bruges til at gemme figurer at plots senere 
#-----------------------------------------------------------------------------------------------------

#Valg af Excel-filer----------------------------------------------------------------------------------
root = tk.Tk() #En starter, eller root, til det vindue/vinduer der skal laves igennem modellen
root.withdraw() #Fjerner eventuelle oprettede vinduer uden at slette dem
root.call('wm', 'attributes', '.', '-topmost', True) #Denne funktion tilføjes for at sikre at vinduet kommer på toppen af andre åbne vinduer, så skal man ikke lede efter det, når modellen kører og dermed misse det
#files = filedialog.askopenfilename(multiple=True) #Denne potter vinduet, hvor filerne der skal importeres vælges
#%gui tk
#var = root.tk.splitlist(files)
var = filedialog.askopenfilename(multiple=True) #Denne potter vinduet, hvor filerne der skal importeres vælges _ Overstående skal fjernes på et tidspunkt

filePaths = [] #Opretter list, der bedre kan arbejde med overstående paths sammen med indbyggede Python funktioner
for f in var: #For-loop igennem alle valgte filer
  filePaths.append(f) #Tilføjer Paths til filePaths i forlængelse af hinanden
#filePaths

filesNames = [] #Opetter list, der skal omformulere overstående paths til at kunne blive benyttet i nedstående funktion, hvor data hentes ind fra Excel-filer
for x in range(len(filePaths)): #Looper over længden af filePaths for at sikre at alle filePaths kommer med - Denne burde fjernes i fremtiden
  tempNames = '\\'.join(filePaths[x].split('/')) #Omdatter "/" til "\\", som virker for nedenstående funktion, der henter data ind
  filesNames.append(tempNames) #Tilføjer omdannede path-navne i forlængelse af hinanden 
#-----------------------------------------------------------------------------------------------------  
  

#Udtagning og behandling af data fra Excel------------------------------------------------------------
data=[pd.read_excel(path) for path in filesNames] #Panda funktion, som henter data ind fra præfabrikerede Excel-filer 
Common_names =["X", "Varmeforbrug", "Samlet behov", "Lagertab", "Behov alene"] #Her skrives der nogle "Almindelig" navne, det forventes at EnergyPro bruger, det er til fra sortering af Data, således at man kun får det mest nødvendige - Det kan være man er nødsagt til at kigge gennem Excel-filen her
data_reduced = data #Opretter en ny dataframe til at bearvejde data, uden at noget går tabt - Det kan være at denne skal fjernes på et senere tidspunkt

allLabels = [] #Opretter list til at hente alle labels brugt i Excel, samt at koordinere farvevalg derimellem.      

#Timer=range(0,data[0].shape[0])
   
#Specifik lagring af data til brug i plots senere

for i in range(len(filesNames)): #For loop for behandling af data, der loopes igennem antallet af filer valgt
    data[i] = data[i].apply(lambda x: pd.Series(x.dropna().values)) #Panda funktion, der tager alle NaN fundet i Excel-filen, det kan have noget at gøre med hvordan data ligger i Excel-filen
    data[i] = data[i].dropna(axis=1, how='all') #Tager alle NaN-værdier i søjler og fjerner dem, skulle det være rækker skulle man skrive axis=0
    globals()['dm%s' % i] = data[i].values #Omdanner dataframen til en matrix, hvorved andre funktioner kan benyttes (Bemærk Global funktionen, der opretter nye navne for dm, således det bliver dm0, dm1 osv alt efter antaller af valgte filer)
    globals()['names%s' % i] = globals()['dm%s' % i][0,:] #Henter navne, som bliver brugt til senere labeling af plot mm.
    data[i].columns = globals()['names%s' % i] #Omdanner navne i dataframe "data", som bruges til først at sætte det samlede varmeforbrug for analysens plot
    if "Lagertab" in globals()['names%s' % i]: #Hvis der er lagertab (Antaget lager med tab) - kan det være at varmeforbruget i analysen er defineret som "Varmeforbrug" - OBS! - vær opmærksom på at EnergyPro skifter navne for flere forskellige analyser, har ikke selv gennemskuet fidusen endnu
        globals()['dm_varmeforbrug%s' % i] = data[i]["Varmeforbrug"].values
    else:
        globals()['dm_varmeforbrug%s' % i] = data[i].T.iloc[-1].values
    
    globals()['dm_varmeforbrug_values%s' % i] = globals()['dm_varmeforbrug%s' % i][1:globals()['dm_varmeforbrug%s' % i].shape[0]]
    globals()['VF%s' % i] = globals()['dm_varmeforbrug_values%s' % i].tolist()
    for String in Common_names:
        if String in globals()['names%s' % i]:
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
#Det kan være at der på et tidspunkt skal gemmes farvekoder, hvis der opstår noget ensartet, eventuelt labels. Så kan man lave en funktion, der akkumulerer valgte farver
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
    
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height])
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25),
                        fancybox=True, shadow=True, ncol=4)
    
#    plt.tight_layout()
    
    name = 'myfig' + str(i) + '.png'
    try:
        plt.savefig(os.path.join(basepath,name), format='png', dpi = 1200)
    except:
        print(f'Eksisterende path findes ikke - Opret mappe der hedder:"{Mappenavn}", således følgende path oprettes: {basepath}')


 # hello

  