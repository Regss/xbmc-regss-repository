# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__icon__                = __addon__.getAddonInfo('icon')

def debug(msg):
    if 'true' in __addon__.getSetting('debug'):
        xbmc.log('>>>> Movielib <<<< ' + msg)
        
def notify(msg):
    if 'true' in __addon__.getSetting('notify'):
        xbmc.executebuiltin('Notification(Movielib, ' + msg + ', 4000, ' + __icon__ + ')')
        