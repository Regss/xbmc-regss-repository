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
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append (__path__)
sys.path.append (__path_img__)

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        mc = [
            ['Nadchodzące', 'week'],
            ['Styczeń', '0'],
            ['Luty', '1'],
            ['Marzec', '2'],
            ['Kwiecień', '3'],
            ['Maj', '4'],
            ['Czerwiec', '5'],
            ['Lipiec', '6'],
            ['Sierpień', '7'],
            ['Wrzesień', '8'],
            ['Październik', '9'],
            ['Listopad', '10'],
            ['Grudzień', '11']
            ]
            
        if self.opt2 == '':

            for key in mc:
                listItem = xbmcgui.ListItem(label=key[0])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?dvd_' + key[1], listitem=listItem, isFolder=True)
            
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            
            if self.opt2 == 'week':
                page = opener.open(self.URL + '/dvd/premieres').read()
            else:
                page = opener.open(self.URL + '/dvd/premieres?month=' + self.opt2 + '&year=' + self.year).read()
                        
            # pobranie linków do poszczególnych filmów
            matchesPageString = list(set(re.compile('editionList.*?dvdNewsroom').findall(page)))
            matchesMovie = list(set(re.compile('href="([^"]+)/editions"').findall(matchesPageString[0])))
            
            # pobranie zawartości strony z trailerami
            for movieLink in matchesMovie:
                
                pageMovie = opener.open(self.URL + movieLink + '/video').read()
                
                # Trailer URL
                matchesTrailerString = re.compile('filmSubpageContent(.*?)filmSubpageMenu').findall(pageMovie)
                matchesLinkTrailer = list(set(re.compile('a href="(/video/trailer/[^"]+)"').findall(matchesTrailerString[0])))
                
                # jeśli istnieje trailer pobiera informacje
                if len(matchesLinkTrailer) != 0:
                    import parseTrailerPage
                    parseTrailerPage.main().parseTrailer(self, matchesLinkTrailer)
                    