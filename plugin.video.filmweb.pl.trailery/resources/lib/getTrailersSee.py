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
        
        # połączenie z adresem URL, pobranie zawartości strony
        opener = urllib2.build_opener()
        
        # sprawdzenie czy istnieje użytkownik
        try:
            page = opener.open(self.URL + '/user/' + self.settingsLogin + '/films/wanna-see').read()
        except:
            xbmcgui.Dialog().ok('Informacja', 'Podaj poprawnego użytkownika[CR]Filmweb.pl w ustawieniach wtyczki')
            return False
            
        if re.search('top.location.href=\'/404\'', page):
            xbmcgui.Dialog().ok('Informacja', 'Podaj poprawnego użytkownika[CR]Filmweb.pl w ustawieniach wtyczki')
            return False
        
        # pobranie linków do poszczególnych filmów
        matchesMovie = list(set(re.compile('overflow[^<]+<a href="([^"]+)"').findall(page)))

        # pobranie zawartości strony z trailerami
        for movieLink in matchesMovie:
            pageMovie = opener.open(self.URL + movieLink + '/video').read()
            
            # Trailer URL
            matchesStringsTrailer = re.compile('filmSubpageContent(.*?)filmSubpageMenu').findall(pageMovie)
            matchesLinkTrailer = list(set(re.compile('a href="(/video/trailer/[^"]+)"').findall(matchesStringsTrailer[0])))
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesLinkTrailer) != 0:
                import parseTrailerPage
                parseTrailerPage.main().parseTrailer(self, matchesLinkTrailer)
                    