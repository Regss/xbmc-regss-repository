# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import sys
import os
import urllib
import urllib2
import json
import xbmcvfs
from PIL import Image
import cStringIO
import base64

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib" ))

import debug
import bar

class syncMovie:

    def __init__(self):
        self.settingsURL     = __addon__.getSetting('url')
        self.settingsToken   = __addon__.getSetting('token')
        self.settingsActors  = __addon__.getSetting('actors')
        self.settingsPosters = __addon__.getSetting('posters')
        self.settingsFanarts = __addon__.getSetting('fanarts')
        self.settingsISO     = __addon__.getSetting('ISO')
        
        self.notify = debug.Debuger().notify
        self.debug = debug.Debuger().debug
        
        self.progBar = bar.Bar()
        
        # prepare URL
        if self.settingsURL[-1:] != '/':
            self.settingsURL = self.settingsURL + '/'
        if self.settingsURL[:7] != 'http://':
            self.settingsURL = 'http://' + self.settingsURL
        
        self.optionURL = 'sync.php?option='
        
        # add token var
        self.tokenURL = '&token=' + self.settingsToken
        
        # sync movie
        if self.syncMovie() is not False:
        
            # sync movie watched status
            self.syncMovieWatched()
            
            # sync movie last played
            self.syncMovieLastPlayed()
        
    def syncMovie(self):
        # get movie id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showmovieid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showmovieid' + self.tokenURL)
            return False
        movielibID = response.read().split()
        self.debug('movielibMovieID: ' + str(movielibID))
        
        # get id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": []}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
        
        xbmcID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'movies' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['movies']:
                xbmcID.append(str(id['movieid']))
        self.debug('xbmcMovieID: ' + str(xbmcID))
        
        # set id to add
        toAddID = []
        for id in xbmcID:
            if id not in movielibID:
                toAddID.append(id)
        self.debug('toAddMovieID: ' + str(toAddID))
        
        # set id do remove
        toRemoveID = []
        for id in movielibID:
            if id not in xbmcID:
                toRemoveID.append(id)
        self.debug('toRemoveMovieID: ' + str(toRemoveID))
                    
        # start sync
        if len(toAddID) > 0:
            self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32204) + ' ' + __lang__(32201))
            if self.addMovie(toAddID) is False:
                return False
            self.progBar.close()
            
        if len(toRemoveID) > 0:
            self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32205) + ' ' + __lang__(32201))
            if self.removeMovie(toRemoveID) is False:
                return False
            self.progBar.close()

    # add movies to database
    def addMovie(self, toAddID):
    
        addedCount = 0
        skippedCount = 0
        countToAdd = len(toAddID)
        
        # check status of allow_url_fopen on server
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'checkallowurlfopen' + self.tokenURL
        response = opener.open(URL)
        allowURLfopen = response.read()
        self.debug('allow_url_fopen: ' + allowURLfopen)
        
        for id in toAddID:

            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["cast", "title", "plot", "rating", "year", "thumbnail", "fanart", "runtime", "genre", "director", "originaltitle", "country", "set", "trailer", "playcount", "lastplayed", "dateadded", "streamdetails", "file"], "movieid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            movie = jsonGetDetailsResponse['result']['moviedetails']
            
            # force sync if iso or ifo file
            isoPass = False
            if (movie['file'][-4:].lower() == '.iso') or (movie['file'][-4:].lower() == '.ifo') or (movie['file'][-5:].lower() == '.bdmv'):
                if 'true' in self.settingsISO:
                    isoPass = True
            
            if (len(movie['streamdetails']['video']) > 0) or (isoPass == True):
                
                # progress bar
                p = int((float(100) / float(countToAdd)) * float(addedCount + skippedCount))
                self.progBar.update(p, str(addedCount + skippedCount + 1) + '/' + str(countToAdd) + ' - ' + movie['title'] + ' (' + str(movie['year']) + ')')
            
                # poster
                if 'true' in self.settingsPosters:
                    poster_source = urllib2.unquote((movie['thumbnail']).encode('utf-8')).replace('\\', '/')
                    if (poster_source[:5] == 'image'):
                        # check status of allow_url_fopen on server
                        if (poster_source[8:12] == 'http') and ('true' in allowURLfopen):
                            poster = poster_source[8:][:-1]
                        else:
                            poster_temp = __datapath__ + '/temp_p'
                            # if file is stored in smb or nfs copy it to addon_data
                            if (poster_source[8:11].lower() == 'smb') or (poster_source[8:11].lower() == 'nfs'):
                                copyRes = xbmcvfs.copy(poster_source[8:][:-1], poster_temp)
                                if copyRes == True:
                                    poster_source = poster_temp
                                else:
                                    poster_source = ''
                            # if it is a URL
                            elif poster_source[8:12] == 'http':
                                poster_source = cStringIO.StringIO(urllib.urlopen(poster_source[8:][:-1]).read())
                            else:
                                poster_source = poster_source[8:][:-1]
                            # resize image
                            try:
                                image = Image.open(poster_source)
                                if (image.size[1] > 198):
                                    image.load()
                                    image.thumbnail((140, 198), Image.ANTIALIAS)
                                    image.save(poster_temp, "JPEG")
                                    poster_bin = xbmcvfs.File(poster_temp)
                                else:
                                    poster_bin = xbmcvfs.File(poster_temp)
                                poster = poster_bin.read()
                                poster_bin.close()
                            except Exception as Error:
                                poster = ''
                                self.debug(str(Error))
                    else:
                        poster = ''
                else:
                    poster = ''
                
                # fanart
                if 'true' in self.settingsFanarts:
                    fanart_source = urllib2.unquote((movie['fanart']).encode('utf-8')).replace('\\', '/')
                    if (fanart_source[:5] == 'image'):
                        # check status of allow_url_fopen on server
                        if (fanart_source[8:12] == 'http') and ('true' in allowURLfopen):
                            fanart = fanart_source[8:][:-1]
                        else:
                            fanart_temp = __datapath__ + '/temp_f'
                            # if file is stored in smb or nfs copy it to addon_data
                            if (fanart_source[8:11].lower() == 'smb') or (fanart_source[8:11].lower() == 'nfs'):
                                copyRes = xbmcvfs.copy(fanart_source[8:][:-1], fanart_temp)
                                if copyRes == True:
                                    fanart_source = fanart_temp
                                else:
                                    fanart_source = ''
                            # if it is a URL
                            elif fanart_source[8:12] == 'http':
                                fanart_source = cStringIO.StringIO(urllib.urlopen(fanart_source[8:][:-1]).read())
                            else:
                                fanart_source = fanart_source[8:][:-1]
                            # resize image
                            try:
                                image = Image.open(fanart_source)            
                                if (image.size[0] > 1280):
                                    image.load()
                                    image.thumbnail((1280, 720), Image.ANTIALIAS)
                                    image.save(fanart_temp, "JPEG")
                                    fanart_bin = xbmcvfs.File(fanart_temp)
                                else:
                                    fanart_bin = xbmcvfs.File(fanart_temp)
                                fanart = fanart_bin.read()
                                fanart_bin.close()
                            except Exception as Error:
                                fanart = ''
                                self.debug(str(Error))
                    else:
                        fanart = ''
                else:
                    fanart = ''
                
                # trailer
                if (movie['trailer'][:4] == 'http'):
                    trailer = movie['trailer']
                elif (movie['trailer'][:29] == 'plugin://plugin.video.youtube'):
                    ytid = movie['trailer'].split('=')
                    trailer = 'http://www.youtube.com/embed/' + ytid[2][0:11]
                else:
                    trailer = ''
                
                # cast
                actors = [];
                for cast in movie['cast']:
                    if 'true' in self.settingsActors:
                        if 'thumbnail' in cast:
                            actor_source = urllib2.unquote((cast['thumbnail']).encode('utf-8')).replace('\\', '/')
                            if (actor_source[:5] == 'image'):
                                # check status of allow_url_fopen on server
                                if (actor_source[8:12] == 'http') and ('true' in allowURLfopen):
                                    castThumb = actor_source[8:][:-1]
                                else:
                                    actor_temp = __datapath__ + '/temp_a'
                                    # if file is stored in smb or nfs copy it to addon_data
                                    if (actor_source[8:11].lower() == 'smb') or (actor_source[8:11].lower() == 'nfs'):
                                        copyRes = xbmcvfs.copy(actor_source[8:][:-1], actor_temp)
                                        if copyRes == True:
                                            actor_source = actor_temp
                                        else:
                                            actor_source = ''
                                    # if it is a URL
                                    elif actor_source[8:12] == 'http':
                                        actor_source = cStringIO.StringIO(urllib.urlopen(actor_source[8:][:-1]).read())
                                    else:
                                        actor_source = actor_source[8:][:-1]
                                    # resize image
                                    try:
                                        image = Image.open(actor_source)
                                        if (image.size[1] > 100):
                                            image.load()
                                            image.thumbnail((75, 100), Image.ANTIALIAS)
                                            image.save(actor_temp, "JPEG")
                                            actor_bin = xbmcvfs.File(actor_temp)
                                        else:
                                            actor_bin = xbmcvfs.File(actor_temp)
                                        castThumb = actor_bin.read()
                                        actor_bin.close()
                                    except Exception as Error:
                                        castThumb = ''
                                        self.debug(str(Error))
                            else:
                                castThumb = '';
                                
                            # push actor thumb
                            if len(castThumb) > 0:
                                valueCast = {
                                    'actor': base64.b64encode(castThumb),
                                    'name': cast['name'].encode('utf-8')
                                }                    
                                data = urllib.urlencode(valueCast)
                                opener = urllib2.build_opener()
                                URL = self.settingsURL + self.optionURL + 'addactor' + self.tokenURL
                                try:
                                    response = opener.open(URL, data)
                                except:
                                    self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                                    self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'addactor' + self.tokenURL)
                                    return False
                                
                    actors.append(cast['name'])
                
                # push movie to script
                values = {
                    'id': id,
                    'title': movie['title'].encode('utf-8'),
                    'plot': movie['plot'].encode('utf-8'),
                    'rating': str(round(float(movie['rating']), 1)),
                    'year': movie['year'],
                    'cast': ' / '.join(actors).encode('utf-8'),
                    'poster': base64.b64encode(poster),
                    'fanart': base64.b64encode(fanart),
                    'trailer': trailer,
                    'runtime': movie['runtime'] / 60,
                    'genre': ' / '.join(movie['genre']).encode('utf-8'),
                    'director': ' / '.join(movie['director']).encode('utf-8'),
                    'originaltitle': movie['originaltitle'].encode('utf-8'),
                    'country': ' / '.join(movie['country']).encode('utf-8'),
                    'sets': movie['set'].encode('utf-8'),
                    'v_codec': movie['streamdetails']['video'][0]['codec'] if len(movie['streamdetails']['video']) > 0 else '',
                    'v_aspect': movie['streamdetails']['video'][0]['aspect'] if len(movie['streamdetails']['video']) > 0 else '',
                    'v_width': movie['streamdetails']['video'][0]['width'] if len(movie['streamdetails']['video']) > 0 else '',
                    'v_height': movie['streamdetails']['video'][0]['height'] if len(movie['streamdetails']['video']) > 0 else '',
                    'v_duration': movie['streamdetails']['video'][0]['duration'] / 60 if len(movie['streamdetails']['video']) > 0 else '',
                    'a_codec': movie['streamdetails']['audio'][0]['codec'] if len(movie['streamdetails']['audio']) > 0 else '',
                    'a_chan': movie['streamdetails']['audio'][0]['channels'] if len(movie['streamdetails']['audio']) > 0 else '',
                    'file': movie['file'].replace('\\', '/').encode('utf-8'),
                    'play_count': movie['playcount'],
                    'last_played': movie['lastplayed'],
                    'date_added': movie['dateadded']
                    }
                
                self.debug(str(values))
                
                data = urllib.urlencode(values)
                opener = urllib2.build_opener()
                URL = self.settingsURL + self.optionURL + 'addmovie' + self.tokenURL
                
                try:
                    response = opener.open(URL, data, 60)
                except:
                    self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                    self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'addmovie' + self.tokenURL)
                    return False
                output = response.read()
            
                self.debug(URL)
                
                # get errors
                if len(output) > 0:
                    if 'ERROR:' in output:
                        self.notify(__lang__(32102).encode('utf-8'))
                else:
                    addedCount += 1
                
                self.debug(output)
            else:
                skippedCount += 1
                
        if skippedCount > 0:
            self.notify(__lang__(32103).encode('utf-8') + ' ' + str(skippedCount) + ' ' + __lang__(32106).encode('utf-8'))
        if addedCount > 0:
            self.notify(__lang__(32104).encode('utf-8') + ' ' + str(addedCount) + ' ' + __lang__(32106).encode('utf-8'))

    # remove movies from database
    def removeMovie(self, toRemoveID):
        
        removedCount = 0
        countToRemove = len(toRemoveID)
        
        for id in toRemoveID:
        
            # progress bar update
            p = int((float(100) / float(countToRemove)) * float(removedCount))
            self.progBar.update(p, str(removedCount+1) + ' / ' + str(countToRemove))
            
            # remove
            values = { 'id': id }
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'removemovie' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'removemovie' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            self.debug(str(values))
            
            #get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            else:
                removedCount += 1
            
            self.debug(output)

        if removedCount > 0:
            self.notify(__lang__(32105).encode('utf-8') + ' ' + str(removedCount) + ' ' + __lang__(32106).encode('utf-8'))
            
    def syncMovieWatched(self):
        # get watched id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showwatchedmovieid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showwatchedmovieid' + self.tokenURL)
            return False
        movielibWatchedID = response.read().split()
        
        self.debug('movielibWatchedMovieID: ' + str(movielibWatchedID))
        
        # get watched id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["playcount"], "filter": {"operator": "greaterthan", "field": "playcount", "value": "0"}}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
    
        xbmcWatchedID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'movies' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['movies']:
                xbmcWatchedID.append(str(id['movieid']))
            
        self.debug('xbmcWatchedMovieID: ' + str(xbmcWatchedID))
        
        # set id to watched
        toWatchedID = []
        for id in xbmcWatchedID:
            if id not in movielibWatchedID:
                toWatchedID.append(id)
                
        self.debug('toWatchedMovieID: ' + str(toWatchedID))
        
        # set id to unwatched
        toUnwatchedID = []
        for id in movielibWatchedID:
            if id not in xbmcWatchedID:
                toUnwatchedID.append(id)
                
        self.debug('toUnwatchedMovieID: ' + str(toUnwatchedID))
                    
        # start sync
        if len(toWatchedID) > 0:
            self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32206) + ' ' + __lang__(32201))
            self.watchedMovie(toWatchedID)
            self.progBar.close()
            
        if len(toUnwatchedID) > 0:
            self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32207) + ' ' + __lang__(32201))
            self.unwatchedMovie(toUnwatchedID)
            self.progBar.close()
            
    # sync watched movies
    def watchedMovie(self, toWatchedID):
        
        countToWatched = len(toWatchedID)
        i = 0
        
        for id in toWatchedID:
        
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["title", "year", "playcount", "lastplayed", "dateadded"], "movieid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            movie = jsonGetDetailsResponse['result']['moviedetails']
            
            # progress bar update
            p = int((float(100) / float(countToWatched)) * float(i))
            self.progBar.update(p, str(i+1) + ' / ' + str(countToWatched) + ' - ' + movie['title'] + ' (' + str(movie['year']) + ')')
            i += 1
            
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
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'watchedmovie' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
    
    # sync unwatched movies
    def unwatchedMovie(self, toUnwatchedID):
    
        countToUnwatched = len(toUnwatchedID)
        i = 0
        
        for id in toUnwatchedID:
            
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["title", "year", "dateadded"], "movieid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            movie = jsonGetDetailsResponse['result']['moviedetails']
            
            # progress bar update
            p = int((float(100) / float(countToUnwatched)) * float(i))
            self.progBar.update(p, str(i+1) + ' / ' + str(countToUnwatched) + ' - ' + movie['title'] + ' (' + str(movie['year']) + ')')
            i += 1
            
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
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'unwatchedmovie' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
            
    def syncMovieLastPlayed(self):
        # get lastplayed date from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showlastplayedmovie' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showlastplayedmovie' + self.tokenURL)
            return False
        movielibLastPlayed = str(response.read())
        
        self.debug('movielibLastPlayedMovieID: ' + movielibLastPlayed)
        
        # get lastplayed movie id from xbmc
        jsonGetMovieID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["lastplayed"], "filter": {"operator": "greaterthan", "field": "lastplayed", "value": "' + movielibLastPlayed + '"}}, "id": 1}')
        jsonGetMovieID = unicode(jsonGetMovieID, 'utf-8', errors='ignore')
        jsonGetMovieIDResponse = json.loads(jsonGetMovieID)
        
        self.debug(str(jsonGetMovieIDResponse))
        
        # set movie id to sync date
        xbmcLastPlayedID = []
        if 'result' not in jsonGetMovieIDResponse:
            return False
        if 'movies' in jsonGetMovieIDResponse['result']:
            for id in jsonGetMovieIDResponse['result']['movies']:
                xbmcLastPlayedID.append(str(id['movieid']))
                
        self.debug('xbmcLastPlayedMovieID: ' + str(xbmcLastPlayedID))
        
        # sync lastplayed
        if len(xbmcLastPlayedID) > 0:
            self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32208) + ' ' + __lang__(32201))
            self.lastPlayedMovie(xbmcLastPlayedID)
            self.progBar.close()
            
    def lastPlayedMovie(self, xbmcLastPlayedID):
        
        countLastPlayed = len(xbmcLastPlayedID)
        i = 0
        
        for id in xbmcLastPlayedID:
            jsonGetMovieDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["title", "year", "playcount", "lastplayed"], "movieid": ' + id + '}, "id": "1"}')
            jsonGetMovieDetails = unicode(jsonGetMovieDetails, 'utf-8', errors='ignore')
            jsonGetMovieDetailsResponse = json.loads(jsonGetMovieDetails)
            
            movie = jsonGetMovieDetailsResponse['result']['moviedetails']
            
            self.debug(str(jsonGetMovieDetailsResponse))
            
            # progress bar update
            p = int(float((100) / float(countLastPlayed)) * float(i))
            self.progBar.update(p, str(i+1) + ' / ' + str(countLastPlayed) + ' - ' + movie['title'] + ' (' + str(movie['year']) + ')')
            i += 1
            
            values = {
                'id': id,
                'playcount': movie['playcount'],
                'lastplayed': movie['lastplayed']
                }
            
            self.debug(str(values))
    
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'lastplayedmovie' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'lastplayedmovie' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
            