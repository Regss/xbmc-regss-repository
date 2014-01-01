# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import os
import sys
import re
import urllib
import urllib2 
import cookielib

__addon__           = xbmcaddon.Addon()
__addon_id__        = __addon__.getAddonInfo('id')
__addonname__       = __addon__.getAddonInfo('name')
__icon__            = __addon__.getAddonInfo('icon')
__addonpath__       = xbmc.translatePath(__addon__.getAddonInfo('path'))
__lang__            = __addon__.getLocalizedString
__path__            = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__        = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append(__path__)
sys.path.append (__path_img__)

class Main:

    def start(self, selfGet):
    
        # vars
        self = selfGet
        
        URL = 'http://www.polskastacja.pl'
        
        if self.opt2 == '':
            
            # dane do wysłania przez POST
            post = {'thumb' : ''}

            # zakodowanie danych w URL
            post_encode = urllib.urlencode(post)

            # wysłanie formularza
            opener = urllib2.build_opener()
            pageRadio = opener.open('http://www.polskastacja.pl', post_encode).read()

            matchesRadio = re.compile('class="channelthumb"[^<]+<a href="([^"]+)"><img src="([^"]+)"[^\!]+\![^\!]+"([^"]+.pls)"[^<]+<[^>]+"Radio ([^"]+)" /></a>/').findall(pageRadio)
            string = ''
            for v in matchesRadio:
                urlhtml = URL + v[0]
                thumb = 'http:' + v[1]
                url = v[2]
                title = v[3]
                matchesPls = re.compile('/([^/]+\.pls)').findall(url)
                pls = matchesPls[0]
                
                listitem=xbmcgui.ListItem(label=title, iconImage=thumb, thumbnailImage=thumb)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?plst_' + pls, listitem=listitem, isFolder=True)

            xbmcplugin.setContent(int(sys.argv[1]),'music')
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            opener = urllib2.build_opener()
            pageRadioPLS = opener.open(URL + '/play/' + self.opt2).read()
            
            matchesIP = re.compile('(http://[^\s]+)\s').findall(pageRadioPLS)
            matchesTitle = re.compile('<<<- (.+) - HQ\n').findall(pageRadioPLS)
            if len(matchesTitle) == 0:
                matchesTitle = re.compile('<<<- (.+)\n').findall(pageRadioPLS)
                
            Title = matchesTitle[0]
            Icon = 'http://cdn.polskastacja.pl/data/channel_icons/' + self.opt2[-3:] + 'jpg'
            sURL = matchesIP[0]
            
            import radioPlayer as player
            player.Main().start(Title, Icon, sURL)
    