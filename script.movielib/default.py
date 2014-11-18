# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import sys
import os

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')

sys.path.append(os.path.join(__addonpath__, "lib"))

import sync

class Movielib:

    def __init__(self):
        sync.start(self)

# check if script is running
if(xbmcgui.Window(10000).getProperty(__addon_id__ + '_running') != 'True'):
    
    # create a lock prevent to run script duble time
    xbmcgui.Window(10000).setProperty(__addon_id__ + '_running', 'True')
    
    Movielib()
    
    # remove lock
    xbmcgui.Window(10000).clearProperty(__addon_id__ + '_running')
    