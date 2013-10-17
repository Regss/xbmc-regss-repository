# -*- coding: utf-8 -*-

import urllib
import urllib2
import os
import re
import sys
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import HTMLParser
import datetime

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append (__path__)
sys.path.append (__path_img__)

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        menu = [
        ['Premiery Kino', 'kino', __path_img__ + '//kino.png'],
        ['Premiery DVD', 'dvd', __path_img__ + '//dvd.png'],
        ['Polecane przez Filmweb', 'filmweb', __path_img__ + '//star.png'],
        ['Rankingi', 'top', __path_img__ + '//top.png'],
        ['Chcę zobaczyć', 'wannasee', __path_img__ + '//see.png'],
        ['W moim mieście', 'city', __path_img__ + '//city.png'],
        ['Filmy użytkownika', 'user', __path_img__ + '//user.png']
        ]

        for key in menu:
            listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?' + key[1], listitem=listItem, isFolder=True)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        