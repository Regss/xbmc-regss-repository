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
            ['Plus Polska', 'http://gramy01.eska.fm:8000/plus-sieciowy-1.mp3', 'http://thumbs.eska.pl/common/4/3/s/4357HEhI.jpg/ru-0-r-244,244-n-4357HEhI.jpg'],
            ['Plus Bydgoszcz', 'http://plus-bydgoszcz-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/POL_Bydgoszcz_COA.svg/256px-POL_Bydgoszcz_COA.svg.png'],
            ['Plus Gdańsk', 'http://plus-gdansk-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/9/91/POL_Gda%C5%84sk_COA.svg/256px-POL_Gda%C5%84sk_COA.svg.png'],
            ['Plus Głogów', 'http://plus-glogow-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/8/83/POL_G%C5%82og%C3%B3w_COA.svg/256px-POL_G%C5%82og%C3%B3w_COA.svg.png'],
            ['Plus Gniezno', 'http://plus-gniezno-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/POL_Gniezno_COA.svg/256px-POL_Gniezno_COA.svg.png'],
            ['Plus Gorzów Wlkp.', 'http://plus-gorzow-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/POL_Gorz%C3%B3w_Wielkopolski_COA_1.svg/256px-POL_Gorz%C3%B3w_Wielkopolski_COA_1.svg.png'],
            ['Plus Gryfice', 'http://gramy01.eska.fm:8000/plus-sieciowy-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/POL_Gryfice_COA_1.svg/256px-POL_Gryfice_COA_1.svg.png'],
            ['Plus Kielce', 'http://plus-kielce-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Herb_miasta_Kielce.svg/256px-Herb_miasta_Kielce.svg.png'],
            ['Plus Koszalin', 'http://gramy01.eska.fm:8000/plus-koszalin-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/POL_Koszalin_COA.svg/256px-POL_Koszalin_COA.svg.png'],
            ['Plus Kraków', 'http://gramy01.eska.fm:8000/plus-krakow-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/4/41/POL_Krak%C3%B3w_COA.svg/256px-POL_Krak%C3%B3w_COA.svg.png'],
            ['Plus Legnica', 'http://gramy01.eska.fm:8000/plus-sieciowy-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Legnica_herb.svg/256px-Legnica_herb.svg.png'],
            ['Plus Lipiany', 'http://gramy01.eska.fm:8000/plus-sieciowy-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/8/87/POL_Lipiany_COA.svg/256px-POL_Lipiany_COA.svg.png'],
            ['Plus Łódź', 'http://gramy01.eska.fm:8000/plus-lodz-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/POL_%C5%81%C3%B3d%C5%BA_COA.svg/256px-POL_%C5%81%C3%B3d%C5%BA_COA.svg.png'],
            ['Plus Olsztyn', 'http://gramy01.eska.fm:8000/plus-olsztyn-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/9/92/POL_Olsztyn_COA.svg/256px-POL_Olsztyn_COA.svg.png'],
            ['Plus Opole', 'http://gramy01.eska.fm:8000/plus-sieciowy-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/POL_Opole_COA.svg/256px-POL_Opole_COA.svg.png'],
            ['Plus Podhale', 'http://gramy01.eska.fm:8000/plus-podhale-1.mp3', ''],
            ['Plus Radom', 'http://plus-radom-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/POL_Radom_COA.svg/256px-POL_Radom_COA.svg.png'],
            ['Plus Szczecin', 'http://gramy01.eska.fm:8000/plus-szczecin-1.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/POL_Szczecin_COA.svg/256px-POL_Szczecin_COA.svg.png'],
            ['Plus Śląsk', 'http://gramy01.eska.fm:8000/plus-sieciowy-1.mp3', ''],
            ['Plus Warszawa', 'http://plus-warszawa-01.eurozet.pl:8500', 'http://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/POL_Warszawa_COA.svg/256px-POL_Warszawa_COA.svg.png']
            ]

        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?plus_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = list[int(self.opt2)][1]
        
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            