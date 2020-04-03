# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 08:58:54 2020

@author: SIAR
"""
#Bibliotek--------------------------------------------------------------------------
import matplotlib.pyplot as plt #Er Pythons plotter modul, som indeholder en masse funktioner til at plotte med
import math #Standard Python modul med matematik funktioner hentes ind her
import numpy as np #se overstående


#-----------------------------------------------------------------------------------


def plot_func(i,VF,m,Labels,colorsForYou,farverBrugt,font):
    plt.figure() #Funktion, der starter figure plot
    plt.rc('axes', axisbelow=True) #Sørger for at begge akser starter og mødes i 0,0 
    plt.grid() #Sætter grid på plot
    hfont = {'fontname':font} #Styre font på plot - OBS! - sikre lige at denne svarer til der bruges i rapport eller powerpoint mm.
    plt.axis([0, 8760, 0, math.ceil(np.amax(VF)/5)*5]) #styrer view på akser, og runder op til nærmeste 5-er
    plt.xlabel('Timer på året', **hfont)  #Sætter navn på x-akse
    plt.ylabel('Varmekapacitet, MW', **hfont) #Sætter navn på y.akse

    plt.plot(range(0,len(VF)),VF, label = "Varmebehov", color = "sandybrown", alpha=0.6, linewidth=0.5) #Plotter varmebehovet
    if None not in farverBrugt: # Hvis der er valgt farver plottes stackplot af hentede værdier
        plt.stackplot(range(0,len(VF)),m, labels = Labels, colors = colorsForYou) #Stackplot af værdier, hvor er der valgt farver i "colorsForYou"
    else:    #Ellers plottes der uden farver
        plt.stackplot(range(0,len(VF)),m, labels = Labels)    #stackplot af værdier der plottes uden valg farve

    ax = plt.subplot(111) #Subplot deres laves for labels, der kommer til at stå neden under figuren
    
    box = ax.get_position() #Laver box omkring labels
    ax.set_position([box.x0, box.y0 + box.height * 0.25,
                     box.width, box.height]) #Gør størrelsen af boxens højde til 10% af dens default værdi
    
    handles,labels = ax.get_legend_handles_labels() #Henter handles og labels til at justerer, hvordan de skal stå (rækkefølgen heraf)
    
    handles.append(handles[0]) #Tilføjer første handle (dette tilfælde varmebehovs kurven) til sidst
    handles.remove(handles[0]) #Fjerner første handle

    labels.append(labels[0]) #Tilføjer første label (dette tilfælde varmebehovs kurven) til sidst
    labels.remove(labels[0]) #Fjerner første label 

    ax.legend(handles,labels,loc='upper center', bbox_to_anchor=(0.5, -0.15),
                        fancybox=True, shadow=False, ncol=4) #funktion der placerer labels under plot og styre placeringen mere specifikt med givne tal

    plt.tight_layout() #Til at give et tæt look at plottet