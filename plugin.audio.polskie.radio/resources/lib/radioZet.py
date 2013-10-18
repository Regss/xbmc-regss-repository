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
        ['Radio ZET', 'http://radiozetmp3-07.eurozet.pl:8400', ''],
        ['Radio ZET Hot', 'http://zethot-01.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-hot/3316128-37-pol-PL/ZET-Hot_resize126x90.png'],
        ['Radio ZET Soul', 'http://zetsoul-01.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-soul/3316234-47-pol-PL/ZET-Soul_resize126x90.png'],
        ['Radio ZET Love', 'http://zetlove-01.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-love/3316001-35-pol-PL/ZET-Love_resize126x90.png'],
        ['Radio ZET Polskie', 'http://zetpl-01.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-pl/3316292-50-pol-PL/ZET-PL_resize126x90.png'],
        ['Radio ZET Dance', 'http://zetdance-02.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-dance/3316085-40-pol-PL/ZET-Dance_resize126x90.png'],
        ['Radio ZET Gold', 'http://zetgold-01.eurozet.pl:8000', ''],
        ['Radio ZET SuperGold', 'http://zetsupergold-01.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-supergold/3316316-47-pol-PL/ZET-SuperGold_resize126x90.png'],
        ['Radio ZET Classic', 'http://zetclassic-02.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-classic/3316200-42-pol-PL/ZET-Classic_resize126x90.png'],
        ['Radio ZET Chopin', 'http://zetchopin-01.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-chopin/3315929-34-pol-PL/ZET-Chopin_resize126x90.png'],
        ['Radio ZET Smooth Jazz', 'http://zet-smoothjazz-02.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-smooth-jazz/3315876-32-pol-PL/ZET-Smooth-Jazz_resize126x90.png'],
        ['Radio ZET Rock', 'http://zetrock-01.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-rock/3315980-35-pol-PL/ZET-Rock_resize126x90.png'],
        ['Radio ZET Classic Rock', 'http://zetclassicrock-01.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-classic-rock/3316249-43-pol-PL/ZET-Classic-Rock_resize126x90.png'],
        ['Radio ZET Rock and Rap', 'http://zet-rockrap-01.eurozet.pl:8000', ''],
        ['Radio ZET Beatles', '', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-beatles/3315633-27-pol-PL/ZET-Beatles_resize126x90.png'],
        ['Radio ZET Sade', 'http://zet-sade-01.eurozet.pl:8500', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-sade/3316331-49-pol-PL/ZET-Sade_resize126x90.png'],
        ['Radio ZET Kids', 'http://zetkids-01.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-kids/3316104-38-pol-PL/ZET-Kids_resize126x90.png'],
        ['Radio ZET Party', 'http://zetparty-01.eurozet.pl:8100', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-party/3316215-40-pol-PL/ZET-Party_resize126x90.png'],
        ['Radio ZET Slow', 'http://zet-slow-02.eurozet.pl:8200', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-slow/3315839-32-pol-PL/ZET-Slow_resize126x90.png'],
        ['Radio ZET Hits', 'http://zet-hits-02.eurozet.pl:8000', 'http://gfx.radiozet.pl/var/ezflow_site/storage/images/muzyka/kanaly-muzyczne-radia-zet/zet-hits/3315906-34-pol-PL/ZET-Hits_resize126x90.png']
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
            