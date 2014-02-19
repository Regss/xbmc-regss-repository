# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import sys
import os
import urllib
import urllib2
import json
import xbmcvfs
from PIL import Image

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib" ))

import debug

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
        
        # prepare URL
        if self.settingsURL[-1:] != '/':
            self.settingsURL = self.settingsURL + '/'
        if self.settingsURL[:7] != 'http://':
            self.settingsURL = 'http://' + self.settingsURL
        
        self.optionURL = 'sync.php?option='
        
        # add token var
        self.tokenURL = '&token=' + self.settingsToken
        
        self.syncMovie()
        
    def syncMovie(self):
        # get movie id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100) + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showid' + self.tokenURL)
            return False
        movielibID = response.read().split()
        self.debug('movielibID: ' + str(movielibID))
        
        # get id from xbmc
        jsonGetMovieID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": []}, "id": 1}')
        jsonGetMovieID = unicode(jsonGetMovieID, 'utf-8', errors='ignore')
        jsonGetMovieIDResponse = json.loads(jsonGetMovieID)
        
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
            jsonGetMovieDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["cast", "title", "plot", "rating", "year", "thumbnail", "fanart", "runtime", "genre", "director", "originaltitle", "country", "trailer", "playcount", "lastplayed", "dateadded", "streamdetails", "file"], "movieid": ' + id + '}, "id": "1"}')
            jsonGetMovieDetails = unicode(jsonGetMovieDetails, 'utf-8', errors='ignore')
            jsonGetMovieDetailsResponse = json.loads(jsonGetMovieDetails)
            movie = jsonGetMovieDetailsResponse['result']['moviedetails']
            
            self.debug(str(jsonGetMovieDetailsResponse))
            
            if (movie['file'][-4:].lower() == '.iso') and ('true' in self.settingsISO):
                isoPass = True
            else:
                isoPass = False
                
            if (len(movie['streamdetails']['video']) > 0) or (isoPass == True):
                
                #poster
                if 'true' in self.settingsPosters:
                    poster_source = urllib2.unquote((movie['thumbnail']).encode('utf-8')).replace('\\', '/')
                    if (poster_source[:5] == 'image'):
                        if (poster_source[8:12] == 'http'):
                            poster = poster_source[8:][:-1]
                        else:
                            poster_temp = __datapath__ + '/temp_p'
                            if (poster_source[8:11].lower() == 'smb') or (poster_source[8:11].lower() == 'nfs'):
                                copyRes = xbmcvfs.copy(poster_source[8:][:-1], poster_temp)
                                if copyRes == True:
                                    poster_source = poster_temp
                                else:
                                    poster_source = ''
                            else:
                                poster_source = poster_source[8:][:-1]
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
                        if (fanart_source[8:12] == 'http'):
                            fanart = fanart_source[8:][:-1]
                        else:
                            fanart_temp = __datapath__ + '/temp_f'
                            if (fanart_source[8:11].lower() == 'smb') or (fanart_source[8:11].lower() == 'nfs'):
                                copyRes = xbmcvfs.copy(fanart_source[8:][:-1], fanart_temp)
                                if copyRes == True:
                                    fanart_source = fanart_temp
                                else:
                                    fanart_source = ''
                            else:
                                fanart_source = fanart_source[8:][:-1]
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
                    trailer = 'http://www.youtube.com/embed/' + movie['trailer'][-11:]
                else:
                    trailer = ''
                
                # cast
                actors = [];
                for cast in movie['cast']:
                    if 'true' in self.settingsActors:
                        if 'thumbnail' in cast:
                            actor_source = urllib2.unquote((cast['thumbnail']).encode('utf-8')).replace('\\', '/')
                            if (actor_source[:5] == 'image'):
                                if (actor_source[8:12] == 'http'):
                                    castThumb = actor_source[8:][:-1]
                                else:
                                    actor_temp = __datapath__ + '/temp_a'
                                    if (actor_source[8:11].lower() == 'smb') or (actor_source[8:11].lower() == 'nfs'):
                                        copyRes = xbmcvfs.copy(actor_source[8:][:-1], actor_temp)
                                        if copyRes == True:
                                            actor_source = actor_temp
                                        else:
                                            actor_source = ''
                                    else:
                                        actor_source = actor_source[8:][:-1]
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
                                    'actor': castThumb,
                                    'name': cast['name'].encode('utf-8')
                                }                    
                                data = urllib.urlencode(valueCast)
                                opener = urllib2.build_opener()
                                URL = self.settingsURL + self.optionURL + 'addactor' + self.tokenURL
                                try:
                                    response = opener.open(URL, data)
                                except:
                                    self.notify(__lang__(32100) + ': ' + self.settingsURL)
                                    self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'addactor' + self.tokenURL)
                                    return False
                                
                    actors.append(cast['name'])
                
                # push movie to script
                values = {
                    'id': id,
                    'title': movie['title'].encode('utf-8'),
                    'plot': movie['plot'].encode('utf-8'),
                    'rating': movie['rating'],
                    'year': movie['year'],
                    'cast': ' / '.join(actors).encode('utf-8'),
                    'poster': poster,
                    'fanart': fanart,
                    'trailer': trailer,
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
                URL = self.settingsURL + self.optionURL + 'addmovie' + self.tokenURL
                
                try:
                    response = opener.open(URL, data)
                except:
                    self.notify(__lang__(32100) + ': ' + self.settingsURL)
                    self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'addmovie' + self.tokenURL)
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
            self.notify(__lang__(32103) + ' ' + str(skippedCount))
        if addedCount > 0:
            self.notify(__lang__(32104) + ' ' + str(addedCount))

    # remove movies from database
    def removeMovie(self, toRemoveID):
        removedCount = 0
        for id in toRemoveID:
            values = { 'id': id }
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'removemovie' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100) + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'removemovie' + self.tokenURL)
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
            self.notify(__lang__(32105) + ' ' + str(removedCount))
