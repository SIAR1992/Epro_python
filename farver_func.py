# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 08:21:49 2020

@author: SIAR
"""
#Bibliotek--------------------------------------------------------------------------------------------
import tkinter as tk #Henter tkinter modulet, some indeholder Tk værktøjskassen, skal henters for at arbejde med pop-op vinduer
from tkinter import filedialog #Henter funktionen, der gør det muligt at arbejde med filedialogs, det er dem, hvor vi kan browse rundt og vælge filer
from tkinter import messagebox #Henter funktionen, der gør det muligt at åbne messagebox, der bruges som dialog box imellem bruger og programmet
from color_saver import ColorSaver #Importerer farvegemmer, der gemmer farver til lokalt dannet database
from color_chooser import ColorChooser #Importerer farvevælger GUI'en, dermed rigtig vigtig at have i samme 
import numpy as np #se overstående
#-----------------------------------------------------------------------------------------------------

def farver_func(Labels):
    root = tk.Tk() #En starter, eller root, til det vindue/vinduer der skal laves igennem modellen
    root.withdraw() #Fjerner eventuelle oprettede vinduer uden at slette dem
    root.call('wm', 'attributes', '.', '-topmost', True) #Denne funktion tilføjes for at sikre at vinduet kommer på toppen af andre åbne vinduer, så skal man ikke lede efter det, når modellen kører og dermed misse det
    allLabelUser = Labels
    allLabelUser.sort() #Opretter ny parameter til at sorterer i labels - Kan være at denne kan komprimeres med nedstående
    farverBrugt = []
    starter = ColorSaver(allLabelUser) # Kalder klassen, der hedder ColorSaver, inde holder moduler, som henter og gemmer farver fra tidligere gemte labels og nye dannede labels
    MsgBox = tk.messagebox.askquestion ('Farver','Vil du vælge farver til plots?',icon = 'question') #Selve tekstboks funktionen til spørgsmål om man vil farvelægge eller ej
    if MsgBox == 'yes': #Hvis ja køres farvekoden igennem
        SavedLabels, SavedColors,Remaining_labels = starter.read_from_db() #Kører modulet read_from_db, som henter data fra classen ud fra de indsatte labels. Den henter SavedLabels, der er alle relevante gemte labels fra databasen, den henter SavedColors, der er alle gemte farver til de pågældende farver, og den henter Remaining_labels, der er alle de labels der er navngivet for plottet, men ikke er gemt i databasen
        Remaining_labels.sort()
        if SavedLabels != []:
            MsgBox = tk.messagebox.askquestion ('Farver','Der er eksisterende labels med valgte farver (Se output box), vil du genbruge dem? - HUSK AT RESTERENDE SKAL FARVELÆGGES',icon = 'question') #Opsætter message box, så man interaktivt kan vælge om man vil bruge de hentede farver, hvis ikke skal man farvelægge alle labels, som overskrives i den nuværende database, hvis de eksisterer
            if MsgBox == 'yes': #Hvis der vælges Yes for overstående messagebox
                existingLabels = [] #Danner parameter til at gemme labels til senere brugt
                if Remaining_labels == []: #Hvis at alle labels er kendte af databasen bruges denne
                    existingLabels = SavedLabels #Labels fra database gemmes oven i existingLabels parameteren
                    farverBrugt = SavedColors #Farver fra databasen gemmes oven i farverBrugt
                    if None in farverBrugt: #Hvis der er opståen en fejl tidligere, således at der ikke opstår en farvekode for labelen, altså at der står None ved labelen
                        res = [i for i in range(len(farverBrugt)) if farverBrugt[i] == None] #Der dannes en parameter res, som finder indekser fra farverBrugt, hvor der står None
                        for i in range(len(res)): #Der loopes igennem længden af res, for at farvelægge alle None fra farverBrugt, således de også kan overskrives i den eksisterende database
                            print(f'Vælg farve for ',existingLabels[res[i]]) #Printer i output hvilken label der skal farvelægges for - bemærk at den specifikke index vælges, således at det er den rigtige label man kigger på
                            chooser = ColorChooser() #Funktion der skal bruges til vinduet med farvevalg
                            result_color = chooser.askcolor() #Funktionen der kalder på farvevælgeren
                            farverBrugt[res[i]] = result_color #parameteren til at gemme de valgte farvekoder - Bemærk at der kun tages fat i de indeks hvor der står None i farverBrugt
                            idx = np.argsort(existingLabels) #Der opstilles index, som sorteres efter navne, lige som allLabelUser, for at sikre at rækkefølgen er den rigtige og de rigtige farver vælges til det rigtige label
                            farverBrugt = np.array(farverBrugt)[idx.astype(int)].tolist() #sortering af farverBrugt efter overstående index
                            starter.dynamic_data_entry(farverBrugt) #Her gemmes valgte farver i database
                else: #Hvis ikke alle er kendte skal de resterende farvelægges
                    for Labels in Remaining_labels: #Labels gennemgår Remaining_labels 
                        print(f'Vælg farve for ',Labels) #Printer i output Labels i Remaining_labels
                        chooser = ColorChooser() #Funktion der skal bruges til vinduet med farvevalg
                        result_color = chooser.askcolor() #Funktionen der kalder på farvevælgeren
                        farverBrugt.append(result_color) #De valgte farver er gemt her 
                    existingLabels = Remaining_labels + SavedLabels #Gemmer Remaining_labels og SavedLabels i samme parameter, således at de kan bearbejdes sammen
                    farverBrugt = farverBrugt + SavedColors #Smider gemte farver på efter de lige valgte farver, således at de kan behandles sammen
                    idx = np.argsort(existingLabels) #Der opstilles index, som sorteres efter navne, lige som allLabelUser, for at sikre at rækkefølgen er den rigtige og de rigtige farver vælges til det rigtige label
                    farverBrugt = np.array(farverBrugt)[idx.astype(int)].tolist() #sortering af farverBrugt efter overstående index
                    starter.dynamic_data_entry(farverBrugt) #Her gemmes valgte farver i database
                
            else:            
                print(f'Der skal vælges farve for ',allLabelUser) #skriver ud hvilke labels der skal vælges farver for
                for Labels in allLabelUser: #Der for loopet igennem alle labels, således at alle farver vælges. Tænker at jeg her kan gemme nogle af farvene til nogle labels, hvis de er ens
                    print(f'Vælg farve for ',Labels) #Viser den enkelte label, der skal vælges farve for, så man er klar over hvad man vælger for 
                    chooser = ColorChooser() #Funktion der skal bruges til vinduet med farvevalg
                    result_color = chooser.askcolor() #Funktionen der kalder på farvevælgeren
                    farverBrugt.append(result_color) #parameteren til at gemme de valgte farvekoder
                starter.dynamic_data_entry(farverBrugt) #Gemmer farver
        else:
            print(f'Der skal vælges farve for ',allLabelUser) #skriver ud hvilke labels der skal vælges farver for
            for Labels in allLabelUser: #Der for loopet igennem alle labels, således at alle farver vælges. Tænker at jeg her kan gemme nogle af farvene til nogle labels, hvis de er ens
                print(f'Vælg farve for ',Labels) #Viser den enkelte label, der skal vælges farve for, så man er klar over hvad man vælger for 
                chooser = ColorChooser() #Funktion der skal bruges til vinduet med farvevalg
                result_color = chooser.askcolor() #Funktionen der kalder på farvevælgeren
                farverBrugt.append(result_color) #parameteren til at gemme de valgte farvekoder
            starter.dynamic_data_entry(farverBrugt) #Gemmer farver
    else:
        farverBrugt = [None] #Danner parameter, det kan være der skal tænkes noget None ind i processen for at undgå denne kode
        print('Ingen farver valgt') #Skriver ud at der ikke er valgt nogen farver
    return farverBrugt, allLabelUser
