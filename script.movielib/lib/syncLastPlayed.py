# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import sys
import os
import urllib
import urllib2
import json

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib" ))

import debug

class syncLastPlayed:

    def __init__(self):
        self.settingsURL    = __addon__.getSetting('url')
        self.settingsLogin  = __addon__.getSetting('login')
        self.settingsToken  = __addon__.getSetting('token')
        self.settingsNotify = __addon__.getSetting('notify')
        self.settingsDebug  = __addon__.getSetting('debug')
        self.notify = debug.Debuger().notify
        self.debug = debug.Debuger().debug
        
        # prepare URL
        if self.settingsURL[-1:] != '/':
            self.settingsURL = self.settingsURL + '/'
        self.settingsURL = self.settingsURL + 'sync.php?option='
        
        # add token var
        self.token = '&token=' + self.settingsToken
        
        self.syncLastPlayed()
        
    def syncLastPlayed(self):
        # get lastplayed date from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + 'showlastplayed' + self.token
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100) + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL)
            return False
        movielibLastPlayed = str(response.read())
        
        self.debug('movielibLastPlayed: ' + movielibLastPlayed)
        
        # get lastplayed movie id from xbmc
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["lastplayed"], "filter": {"operator": "greaterthan", "field": "lastplayed", "value": "' + movielibLastPlayed + '"}}, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        self.debug(str(jsonGetMovieIDResponse))
        
        # set movie id to sync date
        xbmcLastPlayedID = []
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcLastPlayedID.append(str(id['movieid']))
                
        self.debug('xbmcLastPlayedID: ' + str(xbmcLastPlayedID))
        
        # sync lastplayed
        if len(xbmcLastPlayedID) > 0:
            self.lastPlayed(xbmcLastPlayedID)
        
    def lastPlayed(self, xbmcLastPlayedID):
        for id in xbmcLastPlayedID:
            jsonGetMovieDetails = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["playcount", "lastplayed"], "movieid": ' + id + '}, "id": "1"}'
            jsonGetMovieDetailsResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieDetails))
            movie = jsonGetMovieDetailsResponse['result']['moviedetails']
            
            self.debug(str(jsonGetMovieDetailsResponse))
            
            values = {
                'id': id,
                'playcount': movie['playcount'],
                'lastplayed': movie['lastplayed']
                }
            
            self.debug(str(values))
    
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + 'lastplayed' + self.token
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100) + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102))
            
            self.debug(output)
