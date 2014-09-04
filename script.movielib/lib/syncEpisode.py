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

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib" ))

import debug
import bar

class syncEpisode:

    def __init__(self):
        self.settingsURL      = __addon__.getSetting('url')
        self.settingsToken    = __addon__.getSetting('token')
        self.settingsActors   = __addon__.getSetting('actors')
        self.settingsPosters  = __addon__.getSetting('posters')
        self.settingsFanarts  = __addon__.getSetting('fanarts')
        self.settingsEpisodes = __addon__.getSetting('episodes')
        self.settingsISO      = __addon__.getSetting('ISO')
        
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
        
        # sync episode
        if self.syncEpisode() is not False:
        
            # sync episode watched status
            if 'true' in self.settingsEpisodes:
                self.syncEpisodeWatched()
            
            # sync episode last played
            if 'true' in self.settingsEpisodes:
                self.syncEpisodeLastPlayed()
        
    def syncEpisode(self):
        # get episode id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showepisodeid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showepisodeid' + self.tokenURL)
            return False
        movielibID = response.read().split()
        self.debug('movielibEpisodeID: ' + str(movielibID))
        
        # get id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": []}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
        
        xbmcID = []
        if 'true' in self.settingsEpisodes:
            if 'result' not in jsonGetIDResponse:
                return False
            if 'episodes' in jsonGetIDResponse['result']:
                for id in jsonGetIDResponse['result']['episodes']:
                    xbmcID.append(str(id['episodeid']))
            self.debug('xbmcEpisodeID: ' + str(xbmcID))
        
        # set id to add
        toAddID = []
        for id in xbmcID:
            if id not in movielibID:
                toAddID.append(id)
        self.debug('toAddEpisodeID: ' + str(toAddID))
        
        # set id do remove
        toRemoveID = []
        for id in movielibID:
            if id not in xbmcID:
                toRemoveID.append(id)
        self.debug('toRemoveEpisodeID: ' + str(toRemoveID))
                    
        # start sync
        if len(toAddID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Adding Episodes...')
            if self.addEpisode(toAddID) is False:
                return False
            self.progBar.close()
            
        if len(toRemoveID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Removeing Episodes...')
            if self.removeEpisode(toRemoveID) is False:
                return False
            self.progBar.close()

    # add episode to database
    def addEpisode(self, toAddID):
        
        addedCount = 0
        skippedCount = 0
        countToAdd = len(toAddID)
        
        for id in toAddID:
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["title", "plot", "episode", "season", "tvshowid", "file", "firstaired", "playcount", "lastplayed", "dateadded"], "episodeid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            episode = jsonGetDetailsResponse['result']['episodedetails']
            
            self.debug(str(jsonGetDetailsResponse))
            
            # progress bar
            p = int((100 / countToAdd) * addedCount)
            self.progBar.update(p, str(addedCount+1) + '/' + str(countToAdd) + ' - ' + episode['title'])
                
            # push episode to script
            values = {
                'id': id,
                'title': episode['title'].encode('utf-8'),
                'plot': episode['plot'].encode('utf-8'),
                'episode': episode['episode'],
                'season': episode['season'],
                'tvshow': episode['tvshowid'],
                'firstaired': episode['firstaired'],
                'file': episode['file'].replace('\\', '/').encode('utf-8'),
                'play_count': episode['playcount'],
                'last_played': episode['lastplayed'],
                'date_added': episode['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'addepisode' + self.tokenURL
            
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'addepisode' + self.tokenURL)
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
            self.notify(__lang__(32104).encode('utf-8') + ' ' + str(addedCount) + ' ' + __lang__(32108).encode('utf-8'))

    # remove episode from database
    def removeEpisode(self, toRemoveID):
        
        removedCount = 0
        countToRemove = len(toRemoveID)
        
        for id in toRemoveID:
        
            # progress bar update
            p = int((100 / countToRemove) * removedCount)
            self.progBar.update(p,'Removeing Episodes...' ,__addonname__ + ' Remove ' + str(removedCount+1) + ' / ' + str(countToRemove))
            
            # remove
            values = { 'id': id }
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'removeepisode' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'removeepisode' + self.tokenURL)
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
            self.notify(__lang__(32105).encode('utf-8') + ' ' + str(removedCount) + ' ' + __lang__(32108).encode('utf-8'))

    def syncEpisodeWatched(self):
        # get watched id from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showwatchedepisodeid' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showwatchedepisodeid' + self.tokenURL)
            return False
        movielibWatchedID = response.read().split()
        
        self.debug('movielibWatchedEpisodeID: ' + str(movielibWatchedID))
        
        # get watched id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["playcount"], "filter": {"operator": "greaterthan", "field": "playcount", "value": "0"}}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
    
        xbmcWatchedID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'episodes' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['episodes']:
                xbmcWatchedID.append(str(id['episodeid']))
        self.debug('xbmcWatchedEpisodeID: ' + str(xbmcWatchedID))
        
        # set id to watched
        toWatchedID = []
        for id in xbmcWatchedID:
            if id not in movielibWatchedID:
                toWatchedID.append(id)
        self.debug('toWatchedEpisodeID: ' + str(toWatchedID))
        
        # set id to unwatched
        toUnwatchedID = []
        for id in movielibWatchedID:
            if id not in xbmcWatchedID:
                toUnwatchedID.append(id)
        self.debug('toUnwatchedEpisodeID: ' + str(toUnwatchedID))
                    
        # start sync
        if len(toWatchedID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Syncing Episodes Watched...')
            self.watchedEpisode(toWatchedID)
            self.progBar.close()
            
        if len(toUnwatchedID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Syncing Episodes Unwatched...')
            self.unwatchedEpisode(toUnwatchedID)
            self.progBar.close()
            
    # sync watched episodes
    def watchedEpisode(self, toWatchedID):
    
        countToWatched = len(toWatchedID)
        i = 0
        
        for id in toWatchedID:
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["title", "playcount", "lastplayed", "dateadded"], "episodeid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            episode = jsonGetDetailsResponse['result']['episodedetails']
            
            # progress bar update
            p = int((float(100) / float(countToWatched)) * float(i))
            self.progBar.update(p, str(i+1) + ' / ' + str(countToWatched) + ' - ' + episode['title'], __addonname__ + ', Sync Episodes Watched...')
            i = i + 1
            
            values = {
                'id': id,
                'playcount': episode['playcount'],
                'lastplayed': episode['lastplayed'],
                'dateadded': episode['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'watchedepisode' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'watchedepisode' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # GET ERRORS
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
    
    # sync unwatched episodes
    def unwatchedEpisode(self, toUnwatchedID):
    
        countToUnwatched = len(toUnwatchedID)
        i = 0
        
        for id in toUnwatchedID:
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["title", "dateadded"], "episodeid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
            
            self.debug(str(jsonGetDetailsResponse))
            
            episode = jsonGetDetailsResponse['result']['episodedetails']
            
            # progress bar update
            p = int((100 / countToUnwatched) * i)
            self.progBar.update(p, str(i+1) + ' / ' + str(countToUnwatched) + ' - ' + episode['title'], __addonname__ + ', Sync Episodes Unwatched...')
            i = i + 1
            
            values = {
                'id': id,
                'dateadded': episode['dateadded']
                }
            
            self.debug(str(values))
            
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'unwatchedepisode' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'unwatchedepisode' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)
            

    def syncEpisodeLastPlayed(self):
        # get lastplayed date from movielib database
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'showlastplayedepisode' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showlastplayedepisode' + self.tokenURL)
            return False
        movielibLastPlayed = str(response.read())
        
        self.debug('movielibLastPlayedEpisode: ' + movielibLastPlayed)
        
        # get lastplayed episode id from xbmc
        jsonGetID = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["lastplayed"], "filter": {"operator": "greaterthan", "field": "lastplayed", "value": "' + movielibLastPlayed + '"}}, "id": 1}')
        jsonGetID = unicode(jsonGetID, 'utf-8', errors='ignore')
        jsonGetIDResponse = json.loads(jsonGetID)
        
        self.debug(str(jsonGetIDResponse))
        
        # set episode id to sync date
        xbmcLastPlayedID = []
        if 'result' not in jsonGetIDResponse:
            return False
        if 'episodes' in jsonGetIDResponse['result']:
            for id in jsonGetIDResponse['result']['episodes']:
                xbmcLastPlayedID.append(str(id['episodeid']))
                
        self.debug('xbmcLastPlayedEpisodeID: ' + str(xbmcLastPlayedID))
        
        # sync lastplayed
        if len(xbmcLastPlayedID) > 0:
            self.progBar.create('Start...', __addonname__ + ', Syncing Episodes Last Played...')
            self.lastPlayedEpisode(xbmcLastPlayedID)
            self.progBar.close()
            
    def lastPlayedEpisode(self, xbmcLastPlayedID):
        for id in xbmcLastPlayedID:
        
            countLastPlayed = len(xbmcLastPlayedID)
            i = 0
        
            jsonGetDetails = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["title", "playcount", "lastplayed"], "episodeid": ' + id + '}, "id": "1"}')
            jsonGetDetails = unicode(jsonGetDetails, 'utf-8', errors='ignore')
            jsonGetDetailsResponse = json.loads(jsonGetDetails)
                        
            self.debug(str(jsonGetDetailsResponse))
                        
            episode = jsonGetDetailsResponse['result']['episodedetails']
            
            # progress bar update
            p = int((100 / countLastPlayed) * i)
            self.progBar.update(p, str(i+1) + ' / ' + str(countLastPlayed) + ' - ' + episode['title'], __addonname__ + ', Sync Episodes Last Played...')
            i = i + 1
            
            values = {
                'id': id,
                'playcount': episode['playcount'],
                'lastplayed': episode['lastplayed']
                }
            
            self.debug(str(values))
    
            data = urllib.urlencode(values)
            opener = urllib2.build_opener()
            URL = self.settingsURL + self.optionURL + 'lastplayedepisode' + self.tokenURL
            try:
                response = opener.open(URL, data)
            except:
                self.notify(__lang__(32100).encode('utf-8') + ': ' + self.settingsURL)
                self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'lastplayedepisode' + self.tokenURL)
                return False
            output = response.read()
            
            self.debug(URL)
            
            # get errors
            if len(output) > 0:
                if 'ERROR:' in output:
                    self.notify(__lang__(32102).encode('utf-8'))
            
            self.debug(output)