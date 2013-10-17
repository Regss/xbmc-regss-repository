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
        
        mc = [
            ['Top Nowości', '/rankings/film/premiere/world'],
            ['Top Świat', '/rankings/film/world'],
            ['Top Polska', '/rankings/film/poland'],
            ['Najbardziej oczekiwane: Nadchodzące premiery w Polsce', '/base/top/wantToSee/next30daysPoland'],
            ['Najbardziej oczekiwane: Nadchodzące premiery na świecie', '/base/top/wantToSee/next12monthsWorld'],
            ['Najbardziej chcecie obejrzeć: Premiery w Polsce', '/base/top/wantToSee/last30daysPoland'],
            ['Najbardziej chcecie obejrzeć: Premiery na świecie', '/base/top/wantToSee/last12monthsWorld'],
            ['Najbardziej chcecie obejrzeć: Filmy ostatnie dekady', '/base/top/wantToSee/lastDecadeFilms'],
            ['Najbardziej chcecie obejrzeć: Klasyki', '/base/top/wantToSee/classicalFilms']
            ]
            
        if self.opt2 == '':
        
            i = 0
            for key in mc:
                listItem = xbmcgui.ListItem(label=key[0])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?top_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        elif self.opt2 == '0' or self.opt2 == '1' or self.opt2 == '2':
        
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + mc[int(self.opt2)][1]).read()
            
            # pobranie linków do poszczególnych filmów
            matchesMovie = list(re.compile('<a href="([^"]+)"[^"]+"filmOtherInfo').findall(page))
            
            # pobranie zawartości strony z trailerami
            i = 1
            for movieLink in matchesMovie:
            
                # ograniczenie pozycji
                if i > self.settingsLimit:
                    break
                    
                pageMovie = opener.open(self.URL + movieLink + '/video').read()
                
                # Trailer URL
                matchesStringsTrailer = re.compile('filmSubpageContent(.*?)filmSubpageMenu').findall(pageMovie)
                matchesLinkTrailer = list(set(re.compile('a href="(/video/trailer/[^"]+)"').findall(matchesStringsTrailer[0])))
                
                # jeśli istnieje trailer pobiera informacje
                if len(matchesLinkTrailer) != 0:
                    import parseTrailerPage
                    parseTrailerPage.main().parseTrailer(self, matchesLinkTrailer)
                    i = i + 1
        
        else:
            
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + mc[int(self.opt2)][1]).read()
            
            # pobranie linków do poszczególnych filmów
            matchesMovie = list(re.compile('filmOtherInfo"?[^"]+"([^"]+)"').findall(page))
            
            # pobranie zawartości strony z trailerami
            i = 1
            for movieLink in matchesMovie:
            
                # ograniczenie pozycji
                if i > self.settingsLimit:
                    break
                    
                pageMovie = opener.open(self.URL + movieLink + '/video').read()
                
                # Trailer URL
                matchesStringsTrailer = re.compile('filmSubpageContent(.*?)filmSubpageMenu').findall(pageMovie)
                matchesLinkTrailer = list(set(re.compile('a href="(/video/trailer/[^"]+)"').findall(matchesStringsTrailer[0])))
                
                # jeśli istnieje trailer pobiera informacje
                if len(matchesLinkTrailer) != 0:
                    import parseTrailerPage
                    parseTrailerPage.main().parseTrailer(self, matchesLinkTrailer)
                    i = i + 1
            