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
            ['Radio Białystok', 'http://bh2.pl:9938', 'http://miasto.augustow.pl/wp-content/uploads/2011/11/logo_radia.jpg'],
            ['Radio Bydgoszcz', 'http://stream1.radiopik.pl:9004', ''],
            ['Radio Dla Ciebie', 'http://panel.nadaje.com:9174/rdc.ogg', 'http://dzwonek2013.pl/wp-content/uploads/2013/03/RADIO_DLA_CIEBIE1.jpg'],
            ['Radio Gdańsk', 'http://stream.task.gda.pl:8000/rg1', 'http://radiogdansk.pl/images/stories/rg_icons/online_rg_logo.png'],
            ['Radio Gorzów', 'http://stream01.zachod.pl:10105', 'http://www.zdrowezatoki.pl/uploads/patron/5d0ddb2ad489b5fc87c308713f037bc1185445fa.png'],
            ['Radio Katowice', 'http://panel.nadaje.com:9212/radiokatowice', 'http://www.zachod.pl/files/2012/12/04-radio-katowice-2009-rgb.jpg'],
            ['Radio Kielce', 'http://gra.radio.kielce.com.pl:8000/rk1', 'http://portalmedialny.pl/media/images/original/md5/0/a/0a7d6c09fa8d9669919fc70c6104f917/Logo%20Radio%20Kielce.png'],
            ['Radio Kołobrzeg', 'http://194.24.244.11:8000', 'http://www.radiokolobrzeg.pl/wp-content/themes/radiokg/images/logo.png'],
            ['Radio Koszalin', 'http://87.98.235.103:9092/', 'http://www.radio.koszalin.pl/Content/img/logo-rk.png'],
            ['Radio Kraków', 'http://stream3.nadaje.com:9116', 'http://www3.radiokrakow.pl/web/JPAK-8Z6H92/JPAK-8Z6H92588x300.jpg'],
            ['Radio Łódź', 'http://217.113.224.166:8000', 'http://100kamienic.wlodzi.org/wp-content/uploads/2011/03/radio_lodz.jpg'],
            ['Radio Lublin', 'http://94.230.19.202:8000/64k', 'http://moje.radio.lublin.pl/images/logo.png'],
            ['Radio Merkury Poznań', 'http://warszawa1-3.radio.pionier.net.pl:8000', 'http://halinabenedyk.pl/wp-content/uploads/2012/08/radio-merkury.jpg'],
            ['Radio Olsztyn', 'http://213.73.25.178:7055', 'http://www.wydatkikontrolowane.pl/pub/Radio_Olsztyn.jpg'],
            ['Radio Opole', 'http://193.47.151.3:8035', 'http://www.marcinstyczen.art.pl/downloads/partner/logo.jpg'],
            ['Radio Rzeszów', 'http://radiointernetowe.net:9500/', 'http://portalmedialny.pl/media/images/original/md5/3/4/3403186baaddf26e34bdb4af5023c4c7/radio%20rzeszow.jpg'],
            ['Radio Szczecin', 'http://stream.nadaje.com:8056', 'http://portalmedialny.pl/media/images/original/md5/c/0/c06738d8cbf245cd061a54dbf5ecd99f/logo_radio.szczecin.jpg'],
            ['Radio Warszawa', 'http://stream2.nadaje.com:8044/', 'http://radiowarszawa.com.pl/wp-content/uploads/2011/06/radio_Warszawa_logo1.jpg'],
            ['Radio Wrocław', 'http://stream4.nadaje.com:9240', 'http://www.soksir.sobotka.pl/userfiles/image/RW_Ogolne_poziom.JPG'],
            ['Radio Zachód', 'http://stream01.zachod.pl:10103/', 'http://www.zachod.pl/files/2010/10/radio-zachod.jpg'],
            ['Radio Zielona Góra', 'http://stream01.zachod.pl:10107/', 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/c23.23.284.284/s160x160/154649_442523975796115_848218480_n.jpg']
            ]

        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?regionalne_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = list[int(self.opt2)][1]
        
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            