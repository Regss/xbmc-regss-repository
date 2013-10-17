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

class Trailers:
    def __init__(self):
        self.settingsAutoPlay   = __addon__.getSetting('autoPlay')
        self.settingsLogin      = __addon__.getSetting('login')
        self.settingsCity       = __addon__.getSetting('city')
        self.settingsInfo       = __addon__.getSetting('info')
        self.settingsLimit      = int(__addon__.getSetting('limit'))
        self.URL                = 'http://www.filmweb.pl'
        self.MOVIES             = []
        self.parseHtml          = HTMLParser.HTMLParser()
        date                    = datetime.datetime.now()
        self.year               = str(date.year)
        
        optMatches = re.compile('\?([^_]+)_?').findall(sys.argv[2])
        if len(optMatches) == 0:
            self.opt = ''
        else:
            self.opt = optMatches[0]
        
        optMatches2 = re.compile('_([^_]+)_?').findall(sys.argv[2])
        if len(optMatches2) == 0:
            self.opt2 = ''
        else:
            self.opt2 = optMatches2[0]
        
        if self.opt == 'kino':
            import getTrailersKino as load
        elif self.opt == 'dvd':
            import getTrailersDVD as load
        elif self.opt == 'filmweb':
            import getTrailersFilmweb as load
        elif self.opt == 'top':
            import getTrailersTop as load
        elif self.opt == 'wannasee':
            import getTrailersSee as load
        elif self.opt == 'city':
            import getTrailersCity as load
        elif self.opt == 'user':
            import getTrailersUser as load
        else:
            import menu as load
        
        load.main().parse(self)
        self.playList()
    
    # PLAYLIST
    def playList(self):
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        # utworzenie Playlisty
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        for playListItem in self.MOVIES:
            playList.add(playListItem['url'], playListItem['item'])
        xbmc.executebuiltin('xbmc.playercontrol(RepeatAll)')
        
        # autoodtwarzanie playlisty
        if self.settingsAutoPlay == 'true':
            xbmc.Player().play(playList)
    
Trailers()
    