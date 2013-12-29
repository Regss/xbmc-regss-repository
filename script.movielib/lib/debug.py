# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import sys
import os

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString

sys.path.append(os.path.join(__addonpath__, "lib"))

class Debuger:

    def debug(self, msg):
        settingsDebug  = __addon__.getSetting('debug')
        if 'true' in settingsDebug:
            xbmc.log('>>>> Movielib <<<< ' + msg.encode('utf-8'))
            
    def notify(self, msg):
        settingsNotify = __addon__.getSetting('notify')
        if 'true' in settingsNotify:
            xbmc.executebuiltin('Notification(Movielib,' + msg.encode('utf-8') + ')')
