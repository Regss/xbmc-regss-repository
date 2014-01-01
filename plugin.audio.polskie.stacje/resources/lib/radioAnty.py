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
            ['Anty Radio', 'http://94.23.89.48:7000/', 'http://www.zdrojowainvest.pl/images/stories/ANTYRADIO_LOGO.jpg'],
            ['Ballads', 'antbal-01.cdn.eurozet.pl:8002', 'http://gfx.antyradio.pl/var/ezflow_site/storage/images/radio/kanaly-muzyczne/antyradio-ballads/1345952-1-pol-PL/Antyradio-Ballads.png'],
            ['Covers', '	antcov-01.cdn.eurozet.pl:8006', 'http://gfx.antyradio.pl/var/ezflow_site/storage/images/radio/kanaly-muzyczne/antyradio-covers/1345938-1-pol-PL/Antyradio-Covers.png'],
            ['Hard', 'http://anthar-01.cdn.eurozet.pl:8010', 'http://gfx.antyradio.pl/var/ezflow_site/storage/images/radio/kanaly-muzyczne/antyradio-hard/1345945-1-pol-PL/Antyradio-Hard.png'],
            ['Greatest', 'antgre-01.cdn.eurozet.pl:8008', 'http://gfx.antyradio.pl/var/ezflow_site/storage/images/radio/kanaly-muzyczne/antyradio-greatest/1345924-1-pol-PL/Antyradio-Greatest.png'],
            ['Rock Classic', 'antcla-01.cdn.eurozet.pl:8004', 'http://gfx.antyradio.pl/var/ezflow_site/storage/images/radio/kanaly-muzyczne/antyradio-classic-rock/1345917-1-pol-PL/Antyradio-Classic-Rock.png'],
            ['Made in Poland', 'antpol-01.cdn.eurozet.pl:8012', 'http://gfx.antyradio.pl/var/ezflow_site/storage/images/radio/kanaly-muzyczne/antyradio-made-in-poland/1345931-1-pol-PL/Antyradio-Made-in-Poland.png']
            ]

        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?anty_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = list[int(self.opt2)][1]
        
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            