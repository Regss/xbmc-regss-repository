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

class syncWatched:

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
        if self.settingsURL[:7] != 'http://':
            self.settingsURL = 'http://' + self.settingsURL
        
        self.optionURL = 'sync.php?option='
        
        # add token var
        self.tokenURL = '&token=' + self.settingsToken
        
        self.syncWatched()
        
    def syncWatched(self):
        # get watched id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showwatchedid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100) + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showwatchedid' + self.tokenURL)
            return False
        movielibWatchedID = response.read().split()
        
        self.debug('movielibWatchedID: ' + str(movielibWatchedID))
        
        # get watched id from xbmc
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["playcount"], "filter": {"operator": "greaterthan", "field": "playcount", "value": "0"}}, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        self.debug(str(jsonGetMovieIDResponse))
    
        xbmcWatchedID = []
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcWatchedID.append(str(id['movieid']))
            
        self.debug('xbmcWatchedID: ' + str(xbmcWatchedID))
        
        # set id to watched
        toWatchedID = []
        for id in xbmcWatchedID:
            if id in movielibWatchedID:
                pass
            else:
                toWatchedID.append(id)
                
        self.debug('toWatchedID: ' + str(toWatchedID))
        
        # set id to unwatched
        toUnwatchedID = []
        for id in movielibWatchedID:
            if id in xbmcWatchedID:
                pass
            else:
                toUnwatchedID.append(id)
                
        self.debug('toUnwatchedID: ' + str(toUnwatchedID))
                    
        # start sync
        if len(toWatchedID) > 0:
            self.watchedMovie(toWatchedID)
            
        if len(toUnwatchedID) > 0:
            self.unwatchedMovie(toUnwatchedID)
    
    # sync watched movies
    def watchedMovie(self, toWatchedID):
        for id in toWatchedID:
            jsonGetMovieDetails = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["playcount", "lastplayed", "dateadded"], "movieid": ' + id + '}, "id": "1"}'
            jsonGetMovieDetailsResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieDetails))
            movie = jsonGetMovieDetailsResponse['result']['moviedetails']
            
            self.debug(str(jsonGetMovieDetailsResponse))
            
            values = {
                'id': id,
                'playcount': movie['playcount'],
                'lastplayed': movie['lastplayed'],
                'dateadded': movie['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'watchedmovie' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100) + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'watchedmovie' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102))
            
            self.debug(output)
    
    # sync unwatched movies
    def unwatchedMovie(self, toUnwatchedID):
        for id in toUnwatchedID:
            jsonGetMovieDetails = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["dateadded"], "movieid": ' + id + '}, "id": "1"}'
            jsonGetMovieDetailsResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieDetails))
            movie = jsonGetMovieDetailsResponse['result']['moviedetails']
            
            self.debug(str(jsonGetMovieDetailsResponse))
            
            values = {
                'id': id,
                'dateadded': movie['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'unwatchedmovie' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100) + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'unwatchedmovie' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102))
            
            self.debug(output)
