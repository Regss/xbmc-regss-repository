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
__addonpath__       = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
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
        ['Radio ESKA', sys.argv[0] + '?eska', 'http://www.odsluchane.eu/images/loga/eska_logo.png', True, ''],
        ['Radio Zet', sys.argv[0] + '?zet', 'http://www.odsluchane.eu/images/loga/radio_zet_logo.png', True, ''],
        ['Polska Stacja - radio internetowe', sys.argv[0] + '?plst', 'http://cdn.polskastacja.pl/images/polskastacja.gif', True, ''],
        ['Polskie Radio', sys.argv[0] + '?polskie', '', True, ''],
        ['Radio Plus', sys.argv[0] + '?4', 'http://www.odsluchane.eu/images/loga/radio_plus_logo.png', False, 'http://94.23.89.48:8500'],
        ['Radio Gorzów', sys.argv[0] + '?5', '', False, 'http://stream01.zachod.pl:10105']
            ]
                
        for v in list:
            listItem = xbmcgui.ListItem(label=v[0], iconImage=v[2])
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=v[1], listitem=listItem, isFolder=v[3])
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        if self.opt != '':
            
            Title = list[int(self.opt)][0]
            Icon = list[int(self.opt)][2]
            URL = list[int(self.opt)][4]
            
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            