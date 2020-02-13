# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:26:10 2020

@author: SIAR
"""


#from tkinter.colorchooser import askcolor
#def colorcode(*args):
#    color = askcolor()
#    label = Label(text='Vælg farve for {args}',bg=color[1]).pack()
#    print(f'Farven valgt for {args} er nedenstående')
#    return color



#from tkinter import *
#colorchooser.askcolor()

#a = Tk()
#def mcolor():
#    color = colorchooser.askcolor()
#    label = Label(text='your choosen color',bg=color[1]).pack()
#button = Button(text="choose color",width = 30,command= mcolor).pack()
#a.mainloop()

import ctypes
import ctypes.wintypes as wtypes


class CHOOSECOLOR(ctypes.Structure):
    """" a class to represent CWPRETSTRUCT structure
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms646830(v=vs.85).aspx """

    _fields_ = [('lStructSize', wtypes.DWORD),
                ('hwndOwner', wtypes.HWND),
                ('hInstance', wtypes.HWND),
                ('rgbResult', wtypes.COLORREF),
                ('lpCustColors', ctypes.POINTER(wtypes.COLORREF)),
                ('Flags', wtypes.DWORD),
                ('lCustData', wtypes.LPARAM),
                ('lpfnHook', wtypes.LPARAM),
                ('lpTemplateName', ctypes.c_char_p)]


class ColorChooser:
    """ a class to represent Color dialog box
    https://msdn.microsoft.com/en-gb/library/windows/desktop/ms646912(v=vs.85).aspx """
    CC_SOLIDCOLOR = 0x80
    CC_FULLOPEN = 0x02
    custom_color_array = ctypes.c_uint32 * 16
    color_chooser = ctypes.windll.Comdlg32.ChooseColorW

    def to_custom_color_array(self, custom_colors):
        custom_int_colors = self.custom_color_array()

        for i in range(16):
            custom_int_colors[i] = rgb_to_int(*custom_colors[i])

        return custom_int_colors

    def askcolor(self, custom_colors):
        struct = CHOOSECOLOR()

        ctypes.memset(ctypes.byref(struct), 0, ctypes.sizeof(struct))
        struct.lStructSize = ctypes.sizeof(struct)
        struct.Flags = self.CC_SOLIDCOLOR | self.CC_FULLOPEN
        struct.lpCustColors = self.to_custom_color_array(custom_colors)

        if self.color_chooser(ctypes.byref(struct)):
            result = int_to_rgb(struct.rgbResult)
        else:
            result = None

        return result


def rgb_to_int(red, green, blue):
    return red + (green << 8) + (blue << 16)


def int_to_rgb(int_color):
    red = int_color & 255
    green = (int_color >> 8) & 255
    blue = (int_color >> 16) & 255

    return red, green, blue

#colors = [(250, 0, 0), (0, 250, 0), (0, 0, 250), (255, 255, 255)] * 4

#chooser = ColorChooser()
#result_color = chooser.askcolor(colors)

#print(result_color)