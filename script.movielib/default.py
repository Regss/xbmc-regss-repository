# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import sys
import os
import urllib
import urllib2
import re
import json

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, "resources" )

sys.path.append(__path__)

class Movielib:

    def __init__(self):
        
        self.settingsURL    = __addon__.getSetting('url')
        self.settingsLogin  = __addon__.getSetting('login')
        self.settingsToken  = __addon__.getSetting('token')
        self.settingsNotify = __addon__.getSetting('notify')
        self.settingsDebug  = __addon__.getSetting('debug')
        
        if self.settingsURL[-1:] != '/':
            self.settingsURL = self.settingsURL + '/'
        
        self.token = '&token=' + self.settingsToken
        
        self.checkConn()
    
    def checkConn(self):
    
        # CHECK CONNECTION
        try:
            urllib2.urlopen(self.settingsURL + 'admin.php?option=showid' + self.token,timeout=2)
        except:
            self.notify('Can\'t connect to: ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL)
            return False
        else:
            self.debug('Connected to: ' + self.settingsURL)
            self.checkToken()
            
    def checkToken(self):
            opener = urllib2.build_opener()
            URL = self.settingsURL + 'admin.php?option=checktoken' + self.token
            response = opener.open(URL)
            checkToken = response.read()
            self.debug(URL)
            self.debug('Check Token')
            self.debug(checkToken)
            
            if checkToken != 'true':
                self.debug('Wrong Token')
                self.notify('Wrong Token')
                return False
                        
            self.debug('Run Sync Movies')
            
            self.syncMovie()
            
            self.debug('Run Sync Watched')
            
            self.syncWatched()
            
            self.debug('Run Sync LastPlayed')
            
            self.syncLastPlayed()
    
    # SYNC MOVIES
    def syncMovie(self):
    
        # GET MOVIE ID FROM MOVIELIB DATABASE
        opener = urllib2.build_opener()
        URL = self.settingsURL + 'admin.php?option=showid' + self.token
        response = opener.open(URL)
        movielibID = response.read().split()
        self.debug('movielibID: ' + str(movielibID))
        
        # GET MOVIE ID FROM XBMC
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": []}, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        self.debug(str(jsonGetMovieIDResponse))
        
        xbmcID = []
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcID.append(str(id['movieid']))
        self.debug('xbmcID: ' + str(xbmcID))
        
        # SET MOVIE ID TO ADD
        toAddID = []
        for id in xbmcID:
            if id in movielibID:
                pass
            else:
                toAddID.append(id)
        self.debug('toAddID: ' + str(toAddID))
        
        # SET MOVIE ID DO REMOVE
        toRemoveID = []
        for id in movielibID:
            if id in xbmcID:
                pass
            else:
                toRemoveID.append(id)
        self.debug('toRemoveID: ' + str(toRemoveID))
                    
        # SYNC DATABASE
        if len(toAddID) > 0:
            self.addMovie(toAddID)
            
        if len(toRemoveID) > 0:
            self.removeMovie(toRemoveID)
            
    def addMovie(self, toAddID):
        addedCount = 0
        for id in toAddID:
            jsonGetMovieDetails = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["title", "plot", "rating", "year", "thumbnail", "fanart", "runtime", "genre", "director", "originaltitle", "country", "trailer", "playcount", "lastplayed", "dateadded", "streamdetails"], "movieid": ' + id + '}, "id": "1"}'
            jsonGetMovieDetailsResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieDetails))
            movie = jsonGetMovieDetailsResponse['result']['moviedetails']
            
            self.debug(str(jsonGetMovieDetailsResponse))
            
            values = {
                'id': id,
                'title': movie['title'].encode('utf-8'),
                'plot': movie['plot'].encode('utf-8'),
                'rating': movie['rating'],
                'year': movie['year'],
                'poster': urllib2.unquote(movie['thumbnail'][8:][:-1]),
                'fanart': urllib2.unquote(movie['fanart'][8:][:-1]),
                'runtime': movie['runtime'] / 60,
                'genre': ' / '.join(movie['genre']).encode('utf-8'),
                'director': ' / '.join(movie['director']).encode('utf-8'),
                'originaltitle': movie['originaltitle'].encode('utf-8'),
                'country': ' / '.join(movie['country']).encode('utf-8'),
                'v_codec': movie['streamdetails']['video'][0]['codec'] if 'codec' in movie['streamdetails']['video'] else '',
                'v_aspect': movie['streamdetails']['video'][0]['aspect'] if 'aspect' in movie['streamdetails']['video'] else '',
                'v_width': movie['streamdetails']['video'][0]['width'] if 'width' in movie['streamdetails']['video'] else '',
                'v_height': movie['streamdetails']['video'][0]['height'] if 'height' in movie['streamdetails']['video'] else '',
                'v_duration': movie['streamdetails']['video'][0]['duration'] / 60 if 'duration' in movie['streamdetails']['video'] else '',
                'a_codec': movie['streamdetails']['audio'][0]['codec'] if 'codec' in movie['streamdetails']['audio'] else '',
                'a_channels': movie['streamdetails']['audio'][0]['channels'] if 'channels' in movie['streamdetails']['audio'] else '',
                'playcount': movie['playcount'],
                'lastplayed': movie['lastplayed'],
                'dateadded': movie['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + 'admin.php?option=addmovie' + self.token
            response = opener.open(URL, data)
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify('Sync error')
            else:
                addedCount = addedCount + 1
            
            self.debug(output)
            
            break

        if addedCount > 0:
            self.notify('Added ' + str(addedCount))

    def removeMovie(self, toRemoveID):
        removedCount = 0
        for id in toRemoveID:
            values = { 'id': id }
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + 'admin.php?option=removemovie' + self.token
            response = opener.open(URL, data)
            output = response.read()
            
            self.debug(URL)
            self.debug(str(values))
            
            #GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify('Sync error')
            else:
                removedCount = removedCount + 1
            
            self.debug(output)

        if removedCount > 0:
            self.notify('Removed ' + str(removedCount))
    
    # SYNC WATCHED
    def syncWatched(self):
    
        # GET WATCHED MOVIE ID FROM MOVIELIB DATABASE
        opener = urllib2.build_opener()
        URL = self.settingsURL + 'admin.php?option=showwatchedid' + self.token
        response = opener.open(URL)
        movielibWatchedID = response.read().split()
        
        self.debug('movielibWatchedID: ' + str(movielibWatchedID))
        
        # GET WATCHED MOVIE ID FROM XBMC
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["playcount"], "filter": {"operator": "greaterthan", "field": "playcount", "value": "0"}}, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        self.debug(str(jsonGetMovieIDResponse))
    
        xbmcWatchedID = []
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcWatchedID.append(str(id['movieid']))
            
        self.debug('xbmcWatchedID: ' + str(xbmcWatchedID))
        
        # SET MOVIE ID TO WATCHED
        toWatchedID = []
        for id in xbmcWatchedID:
            if id in movielibWatchedID:
                pass
            else:
                toWatchedID.append(id)
                
        self.debug('toWatchedID: ' + str(toWatchedID))
        
        # SET MOVIE ID TO UNWATCHED
        toUnwatchedID = []
        for id in movielibWatchedID:
            if id in xbmcWatchedID:
                pass
            else:
                toUnwatchedID.append(id)
                
        self.debug('toUnwatchedID: ' + str(toUnwatchedID))
                    
        # SYNC DATABASE
        if len(toWatchedID) > 0:
            self.watchedMovie(toWatchedID)
            
        if len(toUnwatchedID) > 0:
            self.unwatchedMovie(toUnwatchedID)
    
    def watchedMovie(self, toWatchedID):
        watchedCount = 0
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
            URL = self.settingsURL + 'admin.php?option=watchedmovie' + self.token
            response = opener.open(URL, data)
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify('Sync error')
            else:
                watchedCount = watchedCount + 1
            
            self.debug(output)
            
        if watchedCount > 0:
            self.notify('Sync Watched ' + str(watchedCount))
    
    def unwatchedMovie(self, toUnwatchedID):
        unwatchedCount = 0
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
            URL = self.settingsURL + 'admin.php?option=unwatchedmovie' + self.token
            response = opener.open(URL, data)
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify('Sync error')
            else:
                unwatchedCount = unwatchedCount + 1
            
            self.debug(output)

        if unwatchedCount > 0:
            self.notify('Sync UnWatched ' + str(unwatchedCount))
    
    # SYNC LASTPLAYED
    def syncLastPlayed(self):
    
        # GET LASTPLAYED DATE FROM MOVIELIB DATABASE
        opener = urllib2.build_opener()
        URL = self.settingsURL + 'admin.php?option=showlastplayed' + self.token
        response = opener.open(URL)
        movielibLastPlayed = str(response.read())
        
        self.debug('movielibLastPlayed: ' + movielibLastPlayed)
        
        # GET LASTPLAYED MOVIE ID FROM XBMC
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["lastplayed"], "filter": {"operator": "greaterthan", "field": "lastplayed", "value": "' + movielibLastPlayed + '"}}, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        self.debug(str(jsonGetMovieIDResponse))
        
        # SET MOVIE ID TO SYNC DATE
        xbmcLastPlayedID = []
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcLastPlayedID.append(str(id['movieid']))
                
        self.debug('xbmcLastPlayedID: ' + str(xbmcLastPlayedID))
        
        # SYNC LASTPLAYED
        if len(xbmcLastPlayedID) > 0:
            self.lastPlayed(xbmcLastPlayedID)
        
    def lastPlayed(self, xbmcLastPlayedID):
        lastPlayedCount = 0
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
            URL = self.settingsURL + 'admin.php?option=lastplayed' + self.token
            response = opener.open(URL, data)
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify('Sync error')
            else:
                lastPlayedCount = lastPlayedCount + 1
            
            self.debug(output)

        if lastPlayedCount > 0:
            self.notify('Sync LastPlayed ' + str(lastPlayedCount))
            
    def debug(self, debug):
        if 'true' in self.settingsDebug:
            xbmc.log('>>>> Movielib <<<< ' + debug)
            
    def notify(self, notify):
        if 'true' in self.settingsNotify:
            xbmc.executebuiltin("Notification(Movielib," + notify + ")")
        
Movielib()
