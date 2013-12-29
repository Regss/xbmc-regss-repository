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

class syncMovie:

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
        
        self.syncMovie()
        
    def syncMovie(self):
        # get movie id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + 'showid' + self.token
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100) + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL)
            return False
        movielibID = response.read().split()
        self.debug('movielibID: ' + str(movielibID))
        
        # get id from xbmc
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": []}, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        self.debug(str(jsonGetMovieIDResponse))
        
        xbmcID = []
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcID.append(str(id['movieid']))
        self.debug('xbmcID: ' + str(xbmcID))
        
        # set id to add
        toAddID = []
        for id in xbmcID:
            if id in movielibID:
                pass
            else:
                toAddID.append(id)
        self.debug('toAddID: ' + str(toAddID))
        
        # set id do remove
        toRemoveID = []
        for id in movielibID:
            if id in xbmcID:
                pass
            else:
                toRemoveID.append(id)
        self.debug('toRemoveID: ' + str(toRemoveID))
                    
        # start sync
        if len(toAddID) > 0:
            self.addMovie(toAddID)
            
        if len(toRemoveID) > 0:
            self.removeMovie(toRemoveID)

    # add movies to database
    def addMovie(self, toAddID):
        addedCount = 0
        skippedCount = 0
        
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
                'poster': urllib2.unquote(movie['thumbnail'][8:][:-1]) if movie['thumbnail'][8:12] == 'http' else '',
                'fanart': urllib2.unquote(movie['fanart'][8:][:-1]) if movie['fanart'][8:12] == 'http' else '',
                'runtime': movie['runtime'] / 60,
                'genre': ' / '.join(movie['genre']).encode('utf-8'),
                'director': ' / '.join(movie['director']).encode('utf-8'),
                'originaltitle': movie['originaltitle'].encode('utf-8'),
                'country': ' / '.join(movie['country']).encode('utf-8'),
                'v_codec': movie['streamdetails']['video'][0]['codec'] if len(movie['streamdetails']['video']) > 0 else '',
                'v_aspect': movie['streamdetails']['video'][0]['aspect'] if len(movie['streamdetails']['video']) > 0 else '',
                'v_width': movie['streamdetails']['video'][0]['width'] if len(movie['streamdetails']['video']) > 0 else '',
                'v_height': movie['streamdetails']['video'][0]['height'] if len(movie['streamdetails']['video']) > 0 else '',
                'v_duration': movie['streamdetails']['video'][0]['duration'] / 60 if len(movie['streamdetails']['video']) > 0 else '',
                'a_codec': movie['streamdetails']['audio'][0]['codec'] if len(movie['streamdetails']['audio']) > 0 else '',
                'a_chan': movie['streamdetails']['audio'][0]['channels'] if len(movie['streamdetails']['audio']) > 0 else '',
                'playcount': movie['playcount'],
                'lastplayed': movie['lastplayed'],
                'dateadded': movie['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + 'addmovie' + self.token
            
            if len(movie['streamdetails']['video']) > 0:
            
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
                else:
                    addedCount = addedCount + 1
                
                self.debug(output)
            else:
                skippedCount = skippedCount + 1
                
        if skippedCount > 0:
            self.notify(__lang__(32103) + str(skippedCount))
        if addedCount > 0:
            self.notify(__lang__(32104) + str(addedCount))

    # remove movies from database
    def removeMovie(self, toRemoveID):
        removedCount = 0
        for id in toRemoveID:
            values = { 'id': id }
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + 'removemovie' + self.token
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100) + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL)
                return False
            output = response.read()
            
            self.debug(URL)
            self.debug(str(values))
            
            #get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102))
            else:
                removedCount = removedCount + 1
            
            self.debug(output)

        if removedCount > 0:
            self.notify(__lang__(32105) + str(removedCount))
