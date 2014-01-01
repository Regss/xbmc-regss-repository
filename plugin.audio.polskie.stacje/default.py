# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import os
import sys
import re
import urllib
import urllib2 
import cookielib

__addon__           = xbmcaddon.Addon()
__addon_id__        = __addon__.getAddonInfo('id')
__addonname__       = __addon__.getAddonInfo('name')
__icon__            = __addon__.getAddonInfo('icon')
__addonpath__       = xbmc.translatePath(__addon__.getAddonInfo('path'))
__lang__            = __addon__.getLocalizedString
__path__            = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__        = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append(__path__)
sys.path.append (__path_img__)

class Radio:
    def __init__(self):
    
        optMatches = re.compile('\?([^_]+)_?').findall(sys.argv[2])
        if len(optMatches) == 0:
            self.opt = ''
        else:
            self.opt = optMatches[0]
        
        optMatches2 = re.compile('_(.+)').findall(sys.argv[2])
        if len(optMatches2) == 0:
            self.opt2 = ''
        else:
            self.opt2 = optMatches2[0]


        if self.opt == 'eska':
            import radioEska as start
        elif self.opt == 'zet':
            import radioZet as start
        elif self.opt == 'rmf':
            import radioRmf as start
        elif self.opt == 'plst':
            import polskaStacja as start
        elif self.opt == 'polskie':
            import radioPolskie as start
        elif self.opt == 'plus':
            import radioPlus as start
        elif self.opt == 'anty':
            import radioAnty as start
        elif self.opt == 'regionalne':
            import radioRegionalne as start
        else:
            import radioMenu as start
            
        start.Main().start(self)
        
Radio()
