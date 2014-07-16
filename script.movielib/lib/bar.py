# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import sys
import os

__addon__               = xbmcaddon.Addon()
__addonname__           = __addon__.getAddonInfo('name')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib"))

class Bar:
    def __init__(self):
        self.ble = xbmcgui.DialogProgressBG()
    
    def create(self, message, heading):
        self.ble.create(heading, message)
    
    def update(self, percent, message, heading=0):
        if heading == 0:
            self.ble.update(percent, message=message)
        else:
            self.ble.update(percent, heading, message)
        
    def close(self):
        self.ble.close()