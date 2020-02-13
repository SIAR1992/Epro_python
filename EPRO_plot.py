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
        globals()['dm_varmeforbrug%s' % i] = data[i]["Varmeforbrug"].values #Antager at der er noget, der hedder "Varmeforbrug", foruddybning se overstående
    else: 
        globals()['dm_varmeforbrug%s' % i] = data[i].T.iloc[-1].values #Hvis der ikke er noget "Lagertab" så antages der at varmebehovet er samlet i sidste kolonne i Excel
    
    globals()['dm_varmeforbrug_values%s' % i] = globals()['dm_varmeforbrug%s' % i][1:globals()['dm_varmeforbrug%s' % i].shape[0]] #Der sorteres, således at kun værdierne fremstår i vektorer
    globals()['VF%s' % i] = globals()['dm_varmeforbrug_values%s' % i].tolist() #Omdanner overstående til nympy list, som der kan arbejdes med i plots senere - Tænker overstående kan kombineres med overstående linje 
    for String in Common_names: #Gennemgår "Common_names" for at fjerne irrellevant data fra behandling
        if String in globals()['names%s' % i]: #Denne smides op for at undgå konflikt med ikke eksisterende strings i "Common_names"
            data_reduced[i] = data_reduced[i].drop([String],axis = 1) #Her fjernes unødvendigt data igennem "String"
    globals()['dm_reduced%s' % i] = data_reduced[i].values #omformulerer "data_reduced" til noget der kan arbejdes med, tænker at denne kan komprimeres lidt
    globals()['Used_names%s' % i] = globals()['dm_reduced%s' % i][0,1:globals()['dm_reduced%s' % i].shape[1]] #Udtager navne, denne er en der kan tages
    globals()['Values%s' % i] = globals()['dm_reduced%s' % i][:,1:globals()['dm%s' % i].shape[1]] #Tager værdierne og navne ud, da disse skal bruges til plottene 
    globals()['Values%s' % i] = globals()['Values%s' % i][1:globals()['Values%s' % i].shape[0],:] #Denne tager kun værdierne ud - tænker at denne kan komprimeres lidt med overstående
    globals()['label%s' % i] = globals()['Used_names%s' % i] #Gemmer de brugte navne, der ikke er fra sorteret 
    allLabels.extend(globals()['label%s' % i].tolist()) #Alle labels der bruges i alle hentede Excel-filer bliver lagret i denne, hvilket skal bruges til farvelægningen
    
    globals()['m%s' % i] = [] #Opretter matrix til at indeholde værdier der skal bruges til stackplot senere
    for k in range(0,globals()['Values%s' % i].shape[1]): #For loop over størrelsen af "Values"- Denne kan nok komprimeres lidt
            globals()['Values_list%s' % i] = globals()['Values%s' % i][:,k].tolist() #Omdanner til værdier der kan bruges i plot
            globals()['m%s' % i].append(globals()['Values_list%s' % i]) #Samler disse værdier i matrix
            


#-------------- Farver -----------------------------------------------
#Det kan være at der på et tidspunkt skal gemmes farvekoder, hvis der opstår noget ensartet, eventuelt labels. Så kan man lave en funktion, der akkumulerer valgte farver
allLabels = list(set(allLabels)) #Fjerner alle ens elementer, således at når der skal farvelægges farvelægges der kun et element adgangen

allLabelUser = allLabels #Opretter ny parameter til at sorterer i labels - Kan være at denne kan komprimeres med nedstående
allLabelUser.sort() # Her sorteres det 


canvas1 = tk.Canvas(root, width = 300, height = 300) #Informationer der skal bruges til at lave vinduet til spørgsmålet der stilles omkring farverlægningen 
canvas1.pack() #funktion der skal bruges til at lave vinduet for spørgsmålet

MsgBox = tk.messagebox.askquestion ('Farver','Vil du vælge farver til plots?',icon = 'question') #Selve tekstboks funktionen til spørgsmål om man vil farvelægge eller ej
if MsgBox == 'yes': #Hvis ja køres farvekoden igennem

    colors = [(250, 0, 0), (0, 250, 0), (0, 0, 250), (255, 255, 255)] * 4 #Nogle farvekoder der skal bruges i sammenhæng med "color_chooser"

    colorSaver = [] #Opretter en parameter der skal tage farvekoder ind fra "color_saver"
    print(f'Der skal vælges farve for ',allLabelUser) #skriver ud hvilke labels der skal vælges farver for
    for Labels in allLabelUser: #Der for loopet igennem alle labels, således at alle farver vælges. Tænker at jeg her kan gemme nogle af farvene til nogle labels, hvis de er ens
        print(f'Vælg farve for ',Labels) #Viser den enkelte label, der skal vælges farve for, så man er klar over hvad man vælger for 
        chooser = color_chooser.ColorChooser() #Funktion der skal bruges til vinduet med farvevalg
        result_color = chooser.askcolor(colors) #Funktionen der kalder på farvevælgeren
        colorSaver.append(result_color) #parameteren til at gemme de valgte farvekoder

    def RGB(color1): return '#%02x%02x%02x' % (color1) #funktion der omdanner ovrestående farvekoder til noget der kan bruges i plottene 
    farverBrugt = [] #Danner parameter til at gemme farverne 
    for farver in colorSaver: #For looper igennem "colorSaver" for at omdanne alle farver
        farverBrugt.append(RGB(farver)) #De omdannede farver gemmes i parameteren

    for i in range(len(filesNames)): #Danner for loop til at smide farvene ind for hver Excel-fil
        globals()['colorsForYou%s' % i] = [] #Laver parameter til gemme farver for hver Excel-fil
        for k in range(len(globals()['label%s' % i])): #Kører igennem længden af "Labels", da farvekoderne skal matches med deres pågældende label
            globals()['colorsForYou%s' % i].append(farverBrugt[allLabelUser.index(globals()['label%s' % i][k])]) #Her matches farvekoder med deres pågældende label og farve kode og gemmes i den nye parameter "colorsForYou"
else:
    farverBrugt = [] #Danner parameter, det kan være der skal tænkes noget None ind i processen for at undgå denne kode
    print('Ingen farver valgt') #Skriver ud at der ikke er valgt nogen farver
#---------------------------------------------------------------------

# Plots laves her-----------------------------------------------------
for i in range(len(filesNames)): #For loop, der laver plots for alle valgte Excel-filer
    plt.figure() #Funktion, der starter figure plot
    plt.rc('axes', axisbelow=True) #Sørger for at begge akser starter og mødes i 0,0 
    plt.grid() #Sætter grid på plot
    hfont = {'fontname':'Verdana'} #Styre font på plot - OBS! - sikre lige at denne svarer til der bruges i rapport eller powerpoint mm.
    plt.axis([0, 8760, 0, math.ceil(np.amax(globals()['dm_varmeforbrug_values%s' % i])/5)*5]) #styrer view på akser, og runder op til nærmeste 5-er
    plt.xlabel('Timer på året', **hfont)  #Sætter navn på x-akse
    plt.ylabel('Varmekapacitet, MW', **hfont) #Sætter navn på y.akse

    plt.plot(range(0,len(globals()['VF%s' % i])),globals()['VF%s' % i], label = "Varmebehov", color = "sandybrown", alpha=0.6) #Plotter varmebehovet
    if farverBrugt != []: # Hvis der er valgt farver plottes stackplot af hentede værdier
        plt.stackplot(range(0,len(globals()['VF%s' % i])),globals()['m%s' % i], labels = globals()['label%s' % i], colors = globals()['colorsForYou%s' % i]) #Stackplot af værdier, hvor er der valgt farver i "colorsForYou"
    else:    #Ellers plottes der uden farver
        plt.stackplot(range(0,len(globals()['VF%s' % i])),globals()['m%s' % i], labels = globals()['label%s' % i])    #stackplot af værdier der plottes uden valg farve
    
    ax = plt.subplot(111) #Subplot deres laves for labels, der kommer til at stå neden under figuren
    
    box = ax.get_position() #Laver box omkring labels
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height]) #Gør størrelsen af boxens højde til 10% af dens default værdi
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25),
                        fancybox=True, shadow=True, ncol=4) #funktion der placerer labels under plot og styre placeringen mere specifikt med givne tal
    
#    plt.tight_layout()
    
    name = 'myfig' + str(i) + '.png' #parameter der laves til at for nu at lave navngivning myfig 1-antal af excel filer - Der skal nok tænkes noget bedre ind, så man kan finde rundt i det, antaget man har mange
    try: #Prøv at lave nedenstående fil med givne path
        plt.savefig(os.path.join(basepath,name), format='png', dpi = 1200) #Gemmer figur på pathen "basepath"
    except: #Eksisterer bathpath ikke skrives nedenstående, for at gøre opmærksom på at man skal oprette pathen for at gemme figurerne 
        print(f'Eksisterende path findes ikke - Opret mappe der hedder:"{Mappenavn}", således følgende path oprettes: {basepath}') #Skrift der forklarer at der mangler at blive oprettet basepath


 # hello

  