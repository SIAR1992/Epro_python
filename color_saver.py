# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:50:26 2020

@author: SIAR
"""

import sqlite3
from Color import *

conn = sqlite3.connect('colorBox.db') #Creating a connection to a database 
c = conn.cursor() #creating a cursor for that database 
        
class ColorSaver:
        """" Henter labels og farver ind, gemmer/overskriver gemte/henter gemte farver, hvis de eksisterer"""
#        def __init__(self, label, color):
#            self.labels = label
#            self.colors = color
#            create_table()
        def __init__(self, label):
            self.labels = label
            create_table()
            
        def dynamic_data_entry(self, color):
            label_name = self.labels
            color_code = color
            i = 0
            for i in range(len(color_code)):
                c.execute("INSERT OR REPLACE INTO labelColorTable(labels, colorcode) VALUES (?, ?)",
                          [label_name[i], color_code[i]]) #Indsætter værdier på de pågældende søjler (unix, datestamp, keyword, value)
                conn.commit()


        def read_from_db(self):
            labelsout = []
            colorsout = []
            existing_labels = []
            label_name = self.labels
            c.execute("SELECT * FROM labelColorTable") #Her vælges specifikke søjler
            data = c.fetchall()
            for j in range(len(data)):
                existing_labels.append(list(data[j])[0])
            not_existing_labels = list((set(label_name) - set(existing_labels)))
            label_name = list(set(label_name) - (set(label_name) - set(existing_labels)))
            label_name.sort()
            for i in range(len(label_name)):
                c.execute("SELECT * FROM labelColorTable WHERE labels = ?",
                          [label_name[i]]) #Her vælges specifikke søjler
                data = c.fetchall()
                labelsout.append(list(data[0])[0])
                colorsout.append(list(data[0])[1])
            if None in colorsout:
                print("Fejl i farver, enten luk Python og slet colorBox, eller overskriv eksisterende farver med nye")
                return labelsout, colorsout,not_existing_labels                
            else:
                for i in range(len(colorsout)):
                    rgb_colorsout = hex_to_rgb(colorsout[i])
                    print(GColor.RGB(rgb_colorsout[0],rgb_colorsout[1],rgb_colorsout[2]),labelsout[i], GColor.END)    
                return labelsout, colorsout,not_existing_labels                




def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS labelColorTable(labels TEXT PRIMARY KEY, colorcode TEXT)') #SQL command is everything that is all CAPITAL LETTERS (notice that SQL does not care about casing, it is only to help oneself)    
    
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))    