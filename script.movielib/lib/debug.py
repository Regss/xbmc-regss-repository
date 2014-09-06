# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import sys
import os

__addon__               = xbmcaddon.Addon()
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib"))

class Debuger:

    def debug(self, msg):
        settingsDebug  = __addon__.getSetting('debug')
        if 'true' in settingsDebug:
            xbmc.log('>>>> Movielib <<<< ' + msg)
            
    def notify(self, msg):
        settingsNotify = __addon__.getSetting('notify')
        if 'true' in settingsNotify:
            xbmc.executebuiltin('Notification(Movielib, ' + msg + ', 4000, ' + __addonpath__.encode('utf-8') + '/icon.png)')
            