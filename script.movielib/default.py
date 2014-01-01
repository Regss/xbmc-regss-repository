# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import sys
import os
import urllib
import urllib2

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib"))

import debug
import syncMovie
import syncWatched
import syncLastPlayed

class Movielib:

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

        self.checkConn()
    
    # check connection
    def checkConn(self):
        try:
            urllib2.urlopen(self.settingsURL + self.optionURL + 'showid' + self.tokenURL,timeout=2)
        except:
            self.notify(__lang__(32100) + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'showid' + self.tokenURL)
            return False
        else:
            self.debug('Connected to: ' + self.settingsURL + self.optionURL + 'showid' + self.tokenURL)
            self.checkToken()
    
    # check token
    def checkToken(self):
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'checktoken' + self.tokenURL
        try:
            response = opener.open(URL)
        except:
            self.notify(__lang__(32100) + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + 'checktoken' + self.tokenURL)
            return False
        checkToken = response.read()
        self.debug(URL)
        self.debug('Check Token')
        self.debug(checkToken)
        
        if checkToken != 'true':
            self.debug('Wrong Token')
            self.notify(__lang__(32101))
            return False
        
        # start sync movies
        self.debug('Run Sync Movies')
        syncMovie.syncMovie()
        
        # start sync watched
        self.debug('Run Sync Watched')
        syncWatched.syncWatched()
        
        # start sync played
        self.debug('Run Sync LastPlayed')
        syncLastPlayed.syncLastPlayed()

Movielib()
