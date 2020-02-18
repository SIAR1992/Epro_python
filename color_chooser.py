# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:26:10 2020

@author: SIAR
"""



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
    
    
    def to_custom_color_array(self):
        custom_colors = [(250, 0, 0), (0, 250, 0), (0, 0, 250), (255, 255, 255)] * 4 #Nogle farvekoder der skal bruges i sammenhæng med "color_chooser"
        custom_int_colors = self.custom_color_array()

        for i in range(16):
            custom_int_colors[i] = rgb_to_int(*custom_colors[i])

        return custom_int_colors

    def askcolor(self):
        struct = CHOOSECOLOR()

        ctypes.memset(ctypes.byref(struct), 0, ctypes.sizeof(struct))
        struct.lStructSize = ctypes.sizeof(struct)
        struct.Flags = self.CC_SOLIDCOLOR | self.CC_FULLOPEN
        struct.lpCustColors = self.to_custom_color_array()

        if self.color_chooser(ctypes.byref(struct)):
            result1 = int_to_rgb(struct.rgbResult)
            result = RGB(result1)
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

def RGB(color1): return '#%02x%02x%02x' % (color1) #funktion der omdanner ovrestående farvekoder til noget der kan bruges i plottene