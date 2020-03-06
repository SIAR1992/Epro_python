# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 07:56:06 2020

@author: SIAR
"""
#Bibliotek--------------------------------------------------------------------------------------------
import pandas as pd #pandas og nympy er standard Python moduler, der indeholder mange vektor funktioner mm., som man kender det fra Matlab
#-----------------------------------------------------------------------------------------------------

def vector_func(i,filesNames, data, data_reduced, Common_names, allLabels):
        data[i] = data[i].apply(lambda x: pd.Series(x.dropna().values)) #Panda funktion, der tager alle NaN fundet i Excel-filen, det kan have noget at gøre med hvordan data ligger i Excel-filen
        data[i] = data[i].dropna(axis=1, how='all') #Tager alle NaN-værdier i søjler og fjerner dem, skulle det være rækker skulle man skrive axis=0

        globals()['dm%s' % i] = data[i].values #Omdanner dataframen til en matrix, hvorved andre funktioner kan benyttes (Bemærk Global funktionen, der opretter nye navne for dm, således det bliver dm0, dm1 osv alt efter antaller af valgte filer)
        globals()['names%s' % i] = globals()['dm%s' % i][0,:] #Henter navne, som bliver brugt til senere labeling af plot mm.
        data[i].columns = globals()['names%s' % i] #Omdanner navne i dataframe "data", som bruges til først at sætte det samlede varmeforbrug for analysens plot - Det bruges til at navigere i dataframen imellem navne såsom "Varmetab" mm.
        if "Lagertab" in globals()['names%s' % i]: #Hvis der er lagertab (Antaget lager med tab i EPRO) - kan det være at varmeforbruget i analysen er defineret som "Varmeforbrug" - OBS! - vær opmærksom på at EnergyPro skifter navne for flere forskellige analyser, har ikke selv gennemskuet fidusen endnu
            globals()['dm_varmeforbrug%s' % i] = data[i]["Varmeforbrug"].values #Antager at der er noget, der hedder "Varmeforbrug", foruddybning se overstående
        else: 
            globals()['dm_varmeforbrug%s' % i] = data[i].T.iloc[-1].values #Hvis der ikke er noget "Lagertab" så antages der at varmebehovet er samlet i sidste kolonne i Excel
    
        globals()['VF%s' % i] = globals()['dm_varmeforbrug%s' % i][1:globals()['dm_varmeforbrug%s' % i].shape[0]].tolist()  #Der sorteres, således at kun værdierne fremstår i vektorer, og omdannes med nympy, således at det kan bruges i plot senere
        removers = list(set(Common_names).intersection(set(globals()['names%s' % i].tolist()))) #Danner en liste med ord, der skal fjernes jf. "Common_names"
        for String in removers: #Gennemgår "removers" for at fjerne irrellevant data fra behandling
            data_reduced[i] = data_reduced[i].drop([String],axis = 1) #Her fjernes unødvendigt data igennem "String"
            
        globals()['dm_reduced%s' % i] = data_reduced[i].values #omformulerer "data_reduced" til noget der kan arbejdes med, tænker at denne kan komprimeres lidt
        globals()['Values%s' % i] = globals()['dm_reduced%s' % i][1:globals()['dm%s' % i].shape[0],1:globals()['dm%s' % i].shape[1]] #Tager kun værdierne ud, da disse skal bruges til plottene - fjerner indeks
    
        globals()['label%s' % i] = globals()['dm_reduced%s' % i][0,1:globals()['dm_reduced%s' % i].shape[1]] #Udtager navne, denne er en der kan tages
        allLabels.extend(globals()['label%s' % i].tolist()) #Alle labels der bruges i alle hentede Excel-filer bliver lagret i denne, hvilket skal bruges til farvelægningen
    
        globals()['m%s' % i] = [] #Opretter matrix til at indeholde værdier der skal bruges til stackplot senere, bliver nød til, foreløbigt at gøre det på denne måde, da Pythons .tolist()-function opstiller matrix forkert smides den på med det samme
        for k in range(0,globals()['Values%s' % i].shape[1]): #For loop over størrelsen af "Values"- Denne kan nok komprimeres lidt
            globals()['m%s' % i].append(globals()['Values%s' % i][:,k].tolist()) #Omdanner til værdier der kan bruges i plot (på bestemt måde) og samler disse i matrix      
        return globals()['m%s' % i], globals()['label%s' % i], globals()['VF%s' % i], allLabels        
#---------------------------------------------------------------------------------------------                