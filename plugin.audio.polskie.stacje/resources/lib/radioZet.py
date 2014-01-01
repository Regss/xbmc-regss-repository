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
        ['Radio ZET online', 'http://radiozetmp3-07.eurozet.pl:8400', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/radio-zet-online/3411387-23-pol-PL/Radio-ZET-online_resize126x90.png'],
        ['Radio ZET Slow', 'http://zetslw-01.cdn.eurozet.pl:8456', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-slow/3315839-32-pol-PL/ZET-Slow_resize126x90.png'],
        ['Radio ZET 90', 'http://zet090-01.cdn.eurozet.pl:8404', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-90/5201463-9-pol-PL/ZET-90_resize126x90.png'],
        ['Radio ZET PL', 'http://zetpl1-01.cdn.eurozet.pl:8446', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-pl/3316292-50-pol-PL/ZET-PL_resize126x90.png'],
        ['Radio ZET 80', 'http://zet080-02.cdn.eurozet.pl:8402', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-80/5004199-16-pol-PL/ZET-80_resize126x90.png'],
        ['Radio ZET Hits', 'http://zethit-01.cdn.eurozet.pl:8428', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-hits/3315906-34-pol-PL/ZET-Hits_resize126x90.png'],
        ['Radio ZET Rock', 'http://zetrok-01.cdn.eurozet.pl:8448', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-rock/3315980-35-pol-PL/ZET-Rock_resize126x90.png'],
        ['Radio ZET Dance', 'http://zetdan-02.cdn.eurozet.pl:8416', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-dance/3316085-40-pol-PL/ZET-Dance_resize126x90.png'],
        ['Radio ZET Klasyka pop', 'http://zetgol-01.cdn.eurozet.pl:8424', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-klasyka-pop/3316156-42-pol-PL/ZET-Klasyka-pop_resize126x90.png'],
        ['Radio ZET SuperGold', 'http://zetspg-02.cdn.eurozet.pl:8460', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-supergold/3316316-47-pol-PL/ZET-SuperGold_resize126x90.png'],
        ['Radio ZET Film', 'http://zetfil-01.cdn.eurozet.pl:8418', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-film/4893016-21-pol-PL/ZET-Film_resize126x90.png'],
        ['Radio ZET Fitness', 'http://zetfit-01.cdn.eurozet.pl:8420', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-fitness/5272313-5-pol-PL/ZET-Fitness_resize126x90.png'],
        ['Radio ZET Soul', 'http://zetsou-01.cdn.eurozet.pl:8458', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-soul/3316234-47-pol-PL/ZET-Soul_resize126x90.png'],
        ['Radio ZET Beatles', 'http://zetlen-02.cdn.eurozet.pl:8438', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-beatles/3315633-27-pol-PL/ZET-Beatles_resize126x90.png'],
        ['Radio ZET Lato', 'http://zetlat-01.cdn.eurozet.pl:8436', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/lato-zet/3315738-31-pol-PL/Lato-ZET_resize126x90.png'],
        ['Radio ZET Kids', 'http://zetkid-01.cdn.eurozet.pl:8434', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-kids/3316104-38-pol-PL/ZET-Kids_resize126x90.png'],
        ['Radio ZET Hot', 'http://zethot-01.cdn.eurozet.pl:8430', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-hot/3316128-37-pol-PL/ZET-Hot_resize126x90.png'],
        ['Radio ZET Party', 'http://zetpar-01.cdn.eurozet.pl:8444', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-party/3316215-40-pol-PL/ZET-Party_resize126x90.png'],
        ['Radio ZET Do biegania', 'http://zetrun-01.cdn.eurozet.pl:8452', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-do-biegania/5251632-4-pol-PL/ZET-Do-Biegania_resize126x90.png'],
        ['Radio ZET 2000', 'http://zet200-01.cdn.eurozet.pl:8406', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-2000/3315891-37-pol-PL/ZET-2000_resize126x90.png'],
        ['Radio ZET Love', 'http://zetlov-01.cdn.eurozet.pl:8440', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-love/3316001-35-pol-PL/ZET-Love_resize126x90.png'],
        ['Radio ZET Sade', 'http://zetsad-01.cdn.eurozet.pl:8454', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-sade/3316331-49-pol-PL/ZET-Sade_resize126x90.png'],
        ['Radio ZET Classic Rock', 'http://zetcrk-02.cdn.eurozet.pl:8414', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-classic-rock/3316249-43-pol-PL/ZET-Classic-Rock_resize126x90.png'],
        ['Radio ZET Osiecka', 'http://zetosi-01.cdn.eurozet.pl:8442', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-osiecka/3310618-23-pol-PL/ZET-Osiecka_resize126x90.png'],
        ['Radio ZET Classic', 'http://zetcla-02.cdn.eurozet.pl:8412', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-classic/3316200-42-pol-PL/ZET-Classic_resize126x90.png'],
        ['Radio ZET Smooth Jazz', 'http://chizsj-01.cdn.eurozet.pl:8114', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-smooth-jazz/3315876-32-pol-PL/ZET-Smooth-Jazz_resize126x90.png'],
        ['Radio ZET Chopin', 'http://zetcho-02.cdn.eurozet.pl:8410', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-chopin/3315929-34-pol-PL/ZET-Chopin_resize126x90.png'],
        ['Radio ZET Grechuta', 'http://zetgre-01.cdn.eurozet.pl:8426', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-grechuta/4250886-26-pol-PL/ZET-Grechuta_resize126x90.png'],
        ]
        
        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?zet_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:
        
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = list[int(self.opt2)][1]
            
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            