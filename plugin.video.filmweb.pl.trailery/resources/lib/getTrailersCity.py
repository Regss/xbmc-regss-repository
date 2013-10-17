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
        
        day = [
            ['Poniedziałek', 'poniedzialek'],
            ['Wtorek', 'wtorek'],
            ['Środa', 'sroda'],
            ['Czwartek', 'czwartek'],
            ['Piątek', 'piatek'],
            ['Sobota', 'sobota'],
            ['Niedziela', 'niedziela']
            ]
        
        if self.opt2 == '':

            for key in day:
                listItemKino = xbmcgui.ListItem(label=key[0])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?city_' + key[1], listitem=listItemKino, isFolder=True)
            
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:
        
            # połączenie z adresem URL, pobranie zawartości strony
            encodeCity = urllib.quote(self.settingsCity)
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/city/' + encodeCity + '/day/' + self.opt2).read()
            
            # pobranie linków do poszczególnych filmów
            matchesMovie = list(set(re.compile('(div class="dropdownTarget.*?trailerLink[^>]+>)').findall(page)))
            
            # pobranie zawartości strony z trailerami
            for movieLink in matchesMovie:
                
                # Trailer URL
                matchesLinkTrailer = re.compile('trailerLink" href="([^"]+)"').findall(movieLink)
                
                # jeśli istnieje trailer pobiera informacje
                if len(matchesLinkTrailer) != 0:
                    import parseTrailerPage
                    parseTrailerPage.main().parseTrailer(self, matchesLinkTrailer)
                    