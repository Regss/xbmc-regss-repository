# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')

#name of script for this service work
serviceForScript = 'script.movielib'

class Run:

    def __init__(self):
        xbmc.executebuiltin('XBMC.RunScript(' + serviceForScript + ')')

class Monitor(xbmc.Monitor):

    def __init__(self):
        xbmc.Monitor.__init__(self)
        
    def onDatabaseUpdated(self, video):
        xbmc.executebuiltin('XBMC.RunScript(' + serviceForScript + ')')
            
class Player(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__(self) 
        
    def onPlayBackStopped(self):
        xbmc.executebuiltin('XBMC.RunScript(' + serviceForScript + ')')

Run()
monitor = Monitor()
player = Player()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
    