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
        self.settingsBar  = __addon__.getSetting('bar')
        self.xbmc_version = int(xbmc.getInfoLabel('System.BuildVersion')[0:2])
        if self.xbmc_version > 12:
            self.b = xbmcgui.DialogProgressBG()
        else:
            self.b = xbmcgui.DialogProgress()
            
    def create(self, message, heading):
        if 'true' in self.settingsBar:
            self.b.create(heading, message)
            
    def update(self, percent, message):
        if 'true' in self.settingsBar:
            if self.xbmc_version > 12:
                self.b.update(percent, message=message)
            else:
                self.b.update(percent, line1=message)
                
    def close(self):
        if 'true' in self.settingsBar:
            self.b.close()