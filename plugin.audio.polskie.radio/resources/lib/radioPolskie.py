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
        ['Jedynka', 'mms://stream.polskieradio.pl/program1', 'http://www.odsluchane.eu/images/loga/jedynka_logo.png'],
        ['Dwójka', 'mms://stream.polskieradio.pl/program2', 'http://www.odsluchane.eu/images/loga/dwojka_logo.png'],
        ['Trójka', 'mms://stream.polskieradio.pl/program3', 'http://www.odsluchane.eu/images/loga/trojka_logo.png'],
        ['Czawórka', 'mms://stream.polskieradio.pl/program4', 'http://www.odsluchane.eu/images/loga/czworka_logo.png']
        ]
        
        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?polskie_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:
        
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = list[int(self.opt2)][1]
            
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            