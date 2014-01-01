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
    
        URL = 'http://moje.polskieradio.pl'
        
        list = [
        ['Programy', 'http://moje.polskieradio.pl/programy', 'programy.png'],
        ['Słowo', 'http://moje.polskieradio.pl/slowo', 'slowo.png'],
        ['Muzyka', 'http://moje.polskieradio.pl/muzyka', 'muzyka.png']
        ]
        
        if self.opt2 == '':
        
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=__path_img__ + '//' + key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?polskie_menu_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        elif self.opt2[0:4] == 'menu':
        
            # wysłanie formularza
            opener = urllib2.build_opener()
            pageRadio = opener.open(list[int(self.opt2[5:])][1]).read()

            matchesRadio = re.compile('<li [^<]+<a href=\'([^\']+)\'[^<]+<[^<]+<[^<]+<[^<]+src=\'([^\']+)\' alt=\'([^\']+)\'').findall(pageRadio)
                        
            i = 0
            for v in matchesRadio:
            
                listItem = xbmcgui.ListItem(label=v[2], iconImage=URL+v[1])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?polskie_' + v[0], listitem=listItem, isFolder=False)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:
                
            opener = urllib2.build_opener()
            pageRadioPLS = opener.open(URL + self.opt2).read()
            
            matchesIP = re.compile('streamer\', \'([^\']+)\'[^,]+, \'([^\']+)\'').findall(pageRadioPLS)
            matchesTitle = re.compile('mp3title">[^>]+>([^<]+)</a>').findall(pageRadioPLS)
            matchesIcon = re.compile('imgStation" class="img" src="([^"]+)"').findall(pageRadioPLS)
            
            Title = matchesTitle[0]
            Icon = URL + '/' + matchesIcon[0]
            sURL = matchesIP[0][0] + '/' + matchesIP[0][1]

            import radioPlayer as player
            player.Main().start(Title, Icon, sURL)
            