# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import sys
import os
import urllib2

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib"))

import debug
import syncMovie
import syncTVshow
import syncEpisode

class Movielib:

    def __init__(self):
        self.settingsURL      = __addon__.getSetting('url')
        self.settingsToken    = __addon__.getSetting('token')
        self.settingsActors   = __addon__.getSetting('actors')
        self.settingsPosters  = __addon__.getSetting('posters')
        self.settingsFanarts  = __addon__.getSetting('fanarts')
        self.settingsEpisodes = __addon__.getSetting('episodes')
        self.settingsISO      = __addon__.getSetting('ISO')
        self.settingsMaster   = __addon__.getSetting('master')
        
        self.versionWebScript = '2.4.0'
        
        self.notify = debug.Debuger().notify
        self.debug = debug.Debuger().debug
        
        # debug settings
        self.debug('settingsURL: ' + self.settingsURL)
        self.debug('settingsToken: ' + self.settingsToken)
        self.debug('settingsActors: ' + self.settingsActors)
        self.debug('settingsPosters: ' + self.settingsPosters)
        self.debug('settingsFanarts: ' + self.settingsFanarts)
        self.debug('settingsEpisodes: ' + self.settingsEpisodes)
        self.debug('settingsISO: ' + self.settingsISO)
        self.debug('settingsMaster: ' + self.settingsMaster)
        
        # prepare URL
        if self.settingsURL[-1:] != '/':
            self.settingsURL = self.settingsURL + '/'
        if self.settingsURL[:7] != 'http://':
            self.settingsURL = 'http://' + self.settingsURL
        
        self.optionURL = 'sync.php?option='
        
        # add token var
        self.tokenURL = '&token=' + self.settingsToken
        
        # check master mode
        if 'true' in self.settingsMaster:
            isMaster = xbmc.getCondVisibility('System.IsMaster')
            if isMaster == 1:
                self.checkToken()
        else:
            self.checkToken()
    
    # check connection
    def checkToken(self):
        
        # check version
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'checkversion'
        try:
            response = opener.open(URL)
        except Exception as Error:
            self.notify(__lang__(32100) + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'checkversion')
            self.debug(str(Error))
            return False
        
        checkVersion = response.read()
        checkVersion = checkVersion.replace(' ', '').replace('\n', '').strip()
        self.debug(URL)
        self.debug('Check version')
        self.debug(checkVersion)
        
        if checkVersion < self.versionWebScript:
            self.notify(__lang__(32109))
            self.debug('Wrong Version of web script. Update is needed to version ' + self.versionWebScript + ' or higher')
            return False
        else:
            self.debug('Version is valid')
        
        # check token
        opener = urllib2.build_opener()
        URL = self.settingsURL + self.optionURL + 'checktoken' + self.tokenURL
        try:
            response = opener.open(URL)
        except Exception as Error:
            self.notify(__lang__(32100) + ': ' + self.settingsURL)
            self.debug('Can\'t connect to: ' + self.settingsURL + self.optionURL + 'checktoken' + self.tokenURL)
            self.debug(str(Error))
            return False
        
        checkToken = response.read()
        checkToken = checkToken.replace(' ', '').replace('\n', '').strip()
        self.debug(URL)
        self.debug('Check Token')
        self.debug(checkToken)
        
        if checkToken != 'true':
            self.notify(__lang__(32101))
            self.debug('Wrong Token')
            return False
        else:
            self.debug('Valid Token')
            
        # start sync movies
        self.debug('Run Sync Movies')
        syncMovie.syncMovie()
        
        # start sync TVshows
        self.debug('Run Sync TVshows')
        syncTVshow.syncTVshow()
        
        # start sync Episodes
        self.debug('Run Sync Episodes')
        syncEpisode.syncEpisode()
    
# check if script is running
if(xbmcgui.Window(10000).getProperty(__addon_id__ + '_running') != 'True'):
    
    # create a lock prevent to run script duble time
    xbmcgui.Window(10000).setProperty(__addon_id__ + '_running', 'True')
    
    Movielib()
    
    # remove lock
    xbmcgui.Window(10000).clearProperty(__addon_id__ + '_running')
    