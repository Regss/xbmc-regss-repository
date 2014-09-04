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

class syncTVshow:

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
        
        # sync tvshow
        if self.syncTVshow() is not False:
        
            # sync tvshow watched status
            self.syncTVshowWatched()
            
            # sync tvshow last played
            self.syncTVshowLastPlayed()
        
    def syncTVshow(self):
        # get tvshow id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showtvshowid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showtvshowid' + self.tokenURL)
            return False
        movielibID = response.read().split()
        self.debug('movielibTVshowID: ' + str(movielibID))
        
        # get id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": []}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
        
        xbmcID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'tvshows' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['tvshows']:
                xbmcID.append(str(id['tvshowid']))
        self.debug('xbmcTVshowID: ' + str(xbmcID))
        
        # set id to add
        toAddID = []
        for id in xbmcID:
            if id not in movielibID:
                toAddID.append(id)
        self.debug('toAddTVshowID: ' + str(toAddID))
        
        # set id do remove
        toRemoveID = []
        for id in movielibID:
            if id not in xbmcID:
                toRemoveID.append(id)
        self.debug('toRemoveTVshowID: ' + str(toRemoveID))
                    
        # start sync
        if len(toAddID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Adding TVShows...')
            if self.addTVshow(toAddID) is False:
                return False
            self.progBar.close()
            
        if len(toRemoveID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Adding TVShows...')
            if self.removeTVshow(toRemoveID) is False:
                return False
            self.progBar.close()
            
    # add tvshow to database
    def addTVshow(self, toAddID):
        
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
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": {"properties": ["title", "originaltitle", "plot", "genre", "cast", "thumbnail", "fanart", "rating", "premiered", "playcount", "lastplayed", "dateadded"], "tvshowid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            tvshow = jsonGetDetailsResponse['result']['tvshowdetails']
            
            # progress bar
            p = int((100 / countToAdd) * addedCount)
            self.progBar.update(p, str(addedCount+1) + '/' + str(countToAdd) + ' - ' + tvshow['title'])
                
            # poster
            if 'true' in self.settingsPosters:
                poster_source = urllib2.unquote((tvshow['thumbnail']).encode('utf-8')).replace('\\', '/')
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
                fanart_source = urllib2.unquote((tvshow['fanart']).encode('utf-8')).replace('\\', '/')
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
            
            # cast
            actors = [];
            for cast in tvshow['cast']:
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
            
            # push tvshow to script
            values = {
                'id': id,
                'title': tvshow['title'].encode('utf-8'),
                'plot': tvshow['plot'].encode('utf-8'),
                'rating': str(round(float(tvshow['rating']), 1)),
                'cast': ' / '.join(actors).encode('utf-8'),
                'poster': base64.b64encode(poster),
                'fanart': base64.b64encode(fanart),
                'genre': ' / '.join(tvshow['genre']).encode('utf-8'),
                'originaltitle': tvshow['originaltitle'].encode('utf-8'),
                'premiered': tvshow['premiered'],
                'play_count': tvshow['playcount'],
                'last_played': tvshow['lastplayed'],
                'date_added': tvshow['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'addtvshow' + self.tokenURL
            
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'addtvshow' + self.tokenURL)
                return False
            output = response.read()
        
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            else:
                addedCount = addedCount + 1
            
            self.debug(output)
            
        if addedCount > 0:
            self.notify(__lang__(32104).encode('utf-8') + ' ' + str(addedCount) + ' ' + __lang__(32107).encode('utf-8'))

    # remove tvshow from database
    def removeTVshow(self, toRemoveID):
        
        removedCount = 0
        countToRemove = len(toRemoveID)
        
        for id in toRemoveID:
            
            # progress bar update
            p = int((100 / countToRemove) * removedCount)
            self.progBar.update(p,'Removeing TVShows...' ,__addonname__ + ' Remove ' + str(removedCount+1) + ' / ' + str(countToRemove))
            
            # remove
            values = { 'id': id }
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'removetvshow' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'removetvshow' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            self.debug(str(values))
            
            #get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            else:
                removedCount = removedCount + 1
            
            self.debug(output)

        if removedCount > 0:
            self.notify(__lang__(32105).encode('utf-8') + ' ' + str(removedCount) + ' ' + __lang__(32107).encode('utf-8'))
            
    def syncTVshowWatched(self):
        # get watched id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showwatchedtvshowid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showwatchedtvshowid' + self.tokenURL)
            return False
        movielibWatchedID = response.read().split()
        
        self.debug('movielibWatchedTVshowID: ' + str(movielibWatchedID))
        
        # get watched id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["playcount"], "filter": {"operator": "greaterthan", "field": "playcount", "value": "0"}}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
    
        xbmcWatchedID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'tvshows' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['tvshows']:
                xbmcWatchedID.append(str(id['tvshowid']))
            
        self.debug('xbmcWatchedTVshowID: ' + str(xbmcWatchedID))
        
        # set id to watched
        toWatchedID = []
        for id in xbmcWatchedID:
            if id not in movielibWatchedID:
                toWatchedID.append(id)
                
        self.debug('toWatchedTVshowID: ' + str(toWatchedID))
        
        # set id to unwatched
        toUnwatchedID = []
        for id in movielibWatchedID:
            if id not in xbmcWatchedID:
                toUnwatchedID.append(id)
                
        self.debug('toUnwatchedTVshowID: ' + str(toUnwatchedID))
                    
        # start sync
        if len(toWatchedID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Syncing TVShow Watched...')
            self.watchedTVshow(toWatchedID)
            self.progBar.close()
            
        if len(toUnwatchedID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Syncing TVShow Unwatched...')
            self.unwatchedTVshow(toUnwatchedID)
            self.progBar.close()
            
    # sync watched tvshows
    def watchedTVshow(self, toWatchedID):
    
        countToWatched = len(toWatchedID)
        i = 0
        
        for id in toWatchedID:
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": {"properties": ["title", "playcount", "lastplayed", "dateadded"], "tvshowid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            tvshow = jsonGetDetailsResponse['result']['tvshowdetails']
            
            # progress bar update
            p = int((100 / countToWatched) * i)
            self.progBar.update(p, str(i+1) + ' / ' + str(countToWatched) + ' - ' + tvshow['title'], __addonname__ + ', Sync TVShow Watched...')
            i = i + 1
            
            values = {
                'id': id,
                'playcount': tvshow['playcount'],
                'lastplayed': tvshow['lastplayed'],
                'dateadded': tvshow['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'watchedtvshow' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'watchedtvshow' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
    
    # sync unwatched tvshows
    def unwatchedTVshow(self, toUnwatchedID):
    
        countToUnwatched = len(toUnwatchedID)
        i = 0
        
        for id in toUnwatchedID:
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": {"properties": ["title", "dateadded"], "tvshowid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            tvshow = jsonGetDetailsResponse['result']['tvshowdetails']
            
            # progress bar update
            p = int((100 / countToUnwatched) * i)
            self.progBar.update(p, str(i+1) + ' / ' + str(countToUnwatched) + ' - ' + tvshow['title'], __addonname__ + ', Sync TVShow Unwatched...')
            i = i + 1
            
            values = {
                'id': id,
                'dateadded': tvshow['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'unwatchedtvshow' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'unwatchedtvshow' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
            

    def syncTVshowLastPlayed(self):
        # get lastplayed date from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showlastplayedtvshow' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showlastplayedtvshow' + self.tokenURL)
            return False
        movielibLastPlayed = str(response.read())
        
        self.debug('movielibLastPlayedTVshow: ' + movielibLastPlayed)
        
        # get lastplayed tvshow id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["lastplayed"], "filter": {"operator": "greaterthan", "field": "lastplayed", "value": "' + movielibLastPlayed + '"}}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
        
        # set tvshow id to sync date
        xbmcLastPlayedID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'tvshows' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['tvshows']:
                xbmcLastPlayedID.append(str(id['tvshowid']))
                
        self.debug('xbmcLastPlayedTVshowID: ' + str(xbmcLastPlayedID))
        
        # sync lastplayed
        if len(xbmcLastPlayedID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Syncing TVShow Last Played...')
            self.lastPlayedTVshow(xbmcLastPlayedID)
            self.progBar.close()
            
    def lastPlayedTVshow(self, xbmcLastPlayedID):
        
        countLastPlayed = len(xbmcLastPlayedID)
        i = 0
        
        for id in xbmcLastPlayedID:
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": {"properties": ["title", "playcount", "lastplayed"], "tvshowid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
                             
            tvshow = jsonGetDetailsResponse['result']['tvshowdetails']
            
            self.debug(str(jsonGetDetailsResponse))
            
            # progress bar update
            p = int((100 / countLastPlayed) * i)
            self.progBar.update(p, str(i+1) + ' / ' + str(countLastPlayed) + ' - ' + tvshow['title'], __addonname__ + ', Sync TVShow Last Played...')
            i = i + 1
            
            values = {
                'id': id,
                'playcount': tvshow['playcount'],
                'lastplayed': tvshow['lastplayed']
                }
            
            self.debug(str(values))
    
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'lastplayedtvshow' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'lastplayedtvshow' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
            