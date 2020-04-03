# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:27:50 2020

@author: SIAR  
"""

#Bibliotek--------------------------------------------------------------------------------------------
import tkinter as tk #Henter tkinter modulet, some indeholder Tk værktøjskassen, skal henters for at arbejde med pop-op vinduer
from tkinter import filedialog #Henter funktionen, der gør det muligt at arbejde med filedialogs, det er dem, hvor vi kan browse rundt og vælge filer
import pandas as pd #pandas og nympy er standard Python moduler, der indeholder mange vektor funktioner mm., som man kender det fra Matlab
import matplotlib.pyplot as plt #Er Pythons plotter modul, som indeholder en masse funktioner til at plotte med

#-------------------------------------------------------------------------------------------------------
import farver_func as ffc
import vector_func as vcf
import plot_func as pltfc
#--------------------------------------------------------------------------------------------------------------
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
var = filedialog.askopenfilename(multiple=True) #Denne potter vinduet, hvor filerne der skal importeres vælges

if var != '':
    filePaths = [] #Opretter list, der bedre kan arbejde med overstående paths sammen med indbyggede Python funktioner
    filesNames = [] #Opetter list, der skal omformulere overstående paths til at kunne blive benyttet i nedstående funktion, hvor data hentes ind fra Excel-filer
    for f in var: #For-loop igennem alle valgte filer
        filePaths.append(f) #Tilføjer Paths til filePaths i forlængelse af hinanden
        tempNames = '\\'.join(filePaths[var.index(f)].split('/')) #Omdatter "/" til "\\", som virker for nedenstående funktion, der henter data ind. Der arbejdes over index her 
        filesNames.append(tempNames) #Tilføjer omdannede path-navne i forlængelse af hinanden 
#-----------------------------------------------------------------------------------------------------  
  

#Udtagning og behandling af data fra Excel------------------------------------------------------------
    data=[pd.read_excel(path) for path in filesNames] #Panda funktion, som henter data ind fra præfabrikerede Excel-filer 
    Common_names =["X", "Varmeforbrug", "Samlet behov", "Lagertab", "Behov alene"] #Her skrives der nogle "Almindelig" navne, det forventes at EnergyPro bruger, det er til fra sortering af Data, således at man kun får det mest nødvendige - Det kan være man er nødsagt til at kigge gennem Excel-filen her


    data_reduced = data #Opretter en ny dataframe til at bearvejde data, uden at noget går tabt - Det kan være at denne skal fjernes på et senere tidspunkt
 
    allLabels = [] #Opretter list til at hente alle labels brugt i Excel, samt at koordinere farvevalg derimellem.      
   
#Specifik lagring af data til brug i plots senere

    for i in range(len(filesNames)): #For loop for behandling af data, der loopes igennem antallet af filer valgt
        globals()['m%s' % i], globals()['label%s' % i], globals()['VF%s' % i], allLabels = vcf.vector_func(i,filesNames, data, data_reduced, Common_names, allLabels)
   
#-----------------------------------------------------------------------------------------------------

#-------------- Farver -----------------------------------------------
    allLabels = list(set(allLabels)) #Fjerner alle ens elementer, således at når der skal farvelægges farvelægges der kun et element adgangen

    canvas1 = tk.Canvas(root, width = 300, height = 300) #Informationer der skal bruges til at lave vinduet til spørgsmålet der stilles omkring farverlægningen 
    canvas1.pack() #funktion der skal bruges til at lave vinduet for spørgsmålet
    farverBrugt, allLabelUser = ffc.farver_func(allLabels)

    if None not in farverBrugt:
        for i in range(len(filesNames)): #Danner for loop til at smide farvene ind for hver Excel-fil
            globals()['colorsForYou%s' % i] = [] #Laver parameter til gemme farver for hver Excel-fil
            for k in range(len(globals()['label%s' % i])): #Kører igennem længden af "Labels", da farvekoderne skal matches med deres pågældende label
                globals()['colorsForYou%s' % i].append(farverBrugt[allLabelUser.index(globals()['label%s' % i][k])]) #Her matches farvekoder med deres pågældende label og farve kode og gemmes i den nye parameter "colorsForYou"
    else:
        for i in range(len(filesNames)): #Danner for loop til at smide farvene ind for hver Excel-fil
            globals()['colorsForYou%s' % i] = [] #Laver parameter til gemme farver for hver Excel-fil
 
#---------------------------------------------------------------------

# Plots laves her-----------------------------------------------------
    font = 'Verdana'            
    for i in range(len(filesNames)): #For loop, der laver plots for alle valgte Excel-filer
        VF = globals()['VF%s' % i]
        m = globals()['m%s' % i]
        Labels = globals()['label%s' % i]
        colorsForYou = globals()['colorsForYou%s' % i]
        pltfc.plot_func(i,VF,m,Labels,colorsForYou,farverBrugt,font)
#---------------------------------------------------------------------    

# Figurer gemmes her--------------------------------------------------    
    
        name = os.path.basename(var[i]) + str(i) + '.png' #Navngivning af figur, der kaldes på navnet efter excel-filerne man vælger - OBS! - Sørg for at 
        try: #Prøv at lave nedenstående fil med givne path
            plt.savefig(os.path.join(basepath,name), format='png', dpi = 1200, bbox_inches='tight') #Gemmer figur på pathen "basepath"
        except: #Eksisterer bathpath ikke skrives nedenstående, for at gøre opmærksom på at man skal oprette pathen for at gemme figurerne 
            print(f'Eksisterende path findes ikke - Opret mappe der hedder:"{Mappenavn}", således følgende path bør oprettes: {basepath}') #Skrift der forklarer at der mangler at blive oprettet basepath
else:
    print('Der er ikke valgt nogle filer, kør programmet igen')