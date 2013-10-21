# -*- coding: utf-8 -*-

import json
import xbmc
import xbmcgui
import re
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')

#name of script for this service work
serviceForScript = 'script.tag.star.rating'

class MyPlayer(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__(self)
        
    def onPlayBackEnded(self):
        try:
            self.mediaType
        except:
            pass
        else:
            if self.mediaType == 'movie' or self.mediaType == 'tvshow':
                if self.movieID != '':
                    xbmc.executebuiltin('XBMC.RunScript(' + serviceForScript + ', ' + self.movieID + ', ' + self.mediaType + ')')
                    self.movieID = ''
            
    def onPlayBackStarted(self):
    
        # get player ID
        jsonGetPlayerID = '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'
        jsonGetPlayerIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetPlayerID))
        try:
            self.playerID = str(jsonGetPlayerIDResponse['result']['playerid'])
        except:
            self.playerID = '1'
        
        # get movie played ID
        jsonGetMovieID = '{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "playerid": ' + self.playerID + ' }, "id": 1}'
        jsonGetMovieIDResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieID))
        
        try:
            self.mediaType = jsonGetMovieIDResponse['result']['item']['type']
        except:
            self.mediaType = ''
        
        try:
            self.movieID = str(jsonGetMovieIDResponse['result']['item']['id'])
        except:
            self.movieID = ''
        
    def onPlayBackStopped(self):
        try:
            self.mediaType
        except:
            pass
        else:
            if self.mediaType == 'movie' or self.mediaType == 'tvshow':
                if self.movieID != '':
                    xbmc.executebuiltin('XBMC.RunScript(' + serviceForScript + ', ' + self.movieID + ', ' + self.mediaType + ')')
                    self.movieID = ''
        
player = MyPlayer()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
