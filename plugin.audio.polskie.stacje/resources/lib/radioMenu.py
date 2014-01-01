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

class Main:
        
    def start(self, selfGet):
    
        # vars
        self = selfGet
        
        list = [
        ['Radio ESKA', sys.argv[0] + '?eska', 'eska.png', ''],
        ['Radio Zet', sys.argv[0] + '?zet', 'zet.png', ''],
        ['Radio RMF', sys.argv[0] + '?rmf', 'rmf.png', ''],
        ['Radio Plus', sys.argv[0] + '?plus', 'plus.png', ''],
        ['Polskie Radio', sys.argv[0] + '?polskie', 'polskieradio.png', ''],
        ['Regionalne', sys.argv[0] + '?regionalne', 'regionalne.png', ''],
        ['Polska Stacja', sys.argv[0] + '?plst', 'polskastacja.png', ''],
        ['Anty Radio', sys.argv[0] + '?anty', 'anty.png', '']
            ]
                
        for v in list:
            listItem = xbmcgui.ListItem(label=v[0], iconImage=__path_img__ + '//' + v[2])
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=v[1], listitem=listItem, isFolder=True)
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        if self.opt != '':
            
            Title = list[int(self.opt)][0]
            Icon = list[int(self.opt)][2]
            URL = list[int(self.opt)][3]
            
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            