# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import sys
import os
import hashlib
import time

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__lang__                = __addon__.getLocalizedString

import debug
import bar
import sendRequest
import art
import syncVideo

def start(self):
    
    self.setXBMC = {}
    self.setXBMC['URL']      = __addon__.getSetting('url')
    self.setXBMC['Token']    = __addon__.getSetting('token')
    self.setXBMC['Notify']   = __addon__.getSetting('notify')
    self.setXBMC['Debug']    = __addon__.getSetting('debug')
    
    self.versionWebScript = '2.7.2'
    
    self.progBar = bar.Bar()
    
    # debug settings
    for n, s in self.setXBMC.items():
        debug.debug('XBMC: ' + n + ': ' + s)
    
    # notify if debugging is on
    if 'true' in self.setXBMC['Debug']:
        debug.notify(__lang__(32115).encode('utf-8'))
    
    # prepare URL
    if self.setXBMC['URL'][-1:] != '/':
        self.setXBMC['URL'] = self.setXBMC['URL'] + '/'
    if self.setXBMC['URL'][:7] != 'http://':
        self.setXBMC['URL'] = 'http://' + self.setXBMC['URL']
    self.setXBMC['URL'] = self.setXBMC['URL'] + 'sync.php?' + 'token=' + self.setXBMC['Token'] + '&option='
    
    check(self)

# check connection
def check(self):
    
    # get settings
    self.setSITE = sendRequest.send(self, 'checksettings')
    if self.setSITE is False:
        debug.notify(__lang__(32100).encode('utf-8'))
        return False
    if len(self.setSITE) > 0:
        for n, s in self.setSITE.items():
            debug.debug('Server: ' + n + ': ' + s)
    
    # post_max_size in bytes
    post_l = self.setSITE['POST_MAX_SIZE'].strip()[:-1]
    post_r = self.setSITE['POST_MAX_SIZE'].strip().lower()[-1:]
    v = { 'g': 3, 'm': 2, 'k': 1 }
    if post_r in v.keys():
        self.setSITE['POST_MAX_SIZE_B'] = int(post_l) * 1024 ** int(v[post_r])
    else:
        self.setSITE['POST_MAX_SIZE_B'] = int(post_l + post_r)
    debug.debug('Server: POST_MAX_SIZE_B: ' + str(self.setSITE['POST_MAX_SIZE_B']))
    
    # check master mode
    if self.setSITE['xbmc_master'] == '1':
        isMaster = xbmc.getCondVisibility('System.IsMaster')
        if isMaster == 0:
            return False
    
    # check version
    if 'version' not in self.setSITE or self.setSITE['version'] < self.versionWebScript:
        debug.notify(__lang__(32109).encode('utf-8'))
        debug.debug('Wrong Version of web script. Update is needed to version ' + self.versionWebScript + ' or higher')
        return False
    else:
        debug.debug('Version is valid')
    
    # check token
    if hashlib.md5(self.setXBMC['Token']).hexdigest() != self.setSITE['token_md5']:
        debug.notify(__lang__(32101).encode('utf-8'))
        debug.debug('Wrong Token')
        return False
    else:
        debug.debug('Token is valid')
    
    # get hash tables from site
    self.hashSITE = sendRequest.send(self, 'showhash')
    if self.hashSITE is False:
        return False
    debug.debug('[hashSITE]: ' + str(self.hashSITE))
    
    val = [
        {
            'json': '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["cast", "title", "plot", "rating", "year", "thumbnail", "fanart", "runtime", "genre", "director", "originaltitle", "country", "set", "studio", "trailer", "playcount", "lastplayed", "dateadded", "streamdetails", "file"]}, "id": "1"}',
            'id': 'movieid',
            'table': 'movies',
            'lang': 32201,
            'values' : ['id', 'table', 'title', 'originaltitle', 'year', 'rating', 'plot', 'set', 'studio[]', 'genre[]', 'actor[]', 'runtime', 'country[]', 'director[]', 'poster', 'trailer', 'file', 'fanart', 'thumb[]', 'last_played', 'play_count', 'date_added', 'stream[]', 'hash']
        },
        {
            'json': '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["title", "originaltitle", "plot", "genre", "cast", "thumbnail", "fanart", "rating", "premiered", "playcount", "lastplayed", "dateadded"]}, "id": 1}',
            'id': 'tvshowid',
            'table': 'tvshows',
            'lang': 32202,
            'values' : ['id', 'table', 'title', 'originaltitle', 'rating', 'plot', 'genre[]', 'actor[]', 'poster', 'fanart', 'premiered', 'last_played', 'play_count', 'date_added', 'hash']
        },
        {
            'json': '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["title", "plot", "episode", "season", "tvshowid", "thumbnail", "file", "firstaired", "playcount", "lastplayed", "dateadded", "streamdetails"]}, "id": 1}',
            'id': 'episodeid',
            'table': 'episodes',
            'lang': 32203,
            'values' : ['id', 'table', 'title', 'plot', 'episode', 'season', 'tvshow', 'thumbnail', 'firstaired', 'last_played', 'play_count', 'date_added', 'file', 'stream[]', 'hash']
        }
    ]
    
    self.panelUpdated = False
    self.panelsSITE = {}
    
    # sync videos
    debug.debug('=== SYNC VIDEOS ===')
    for v in val:
        if syncVideo.sync(self, v) is False:
            return False

    # start generate banner
    debug.debug('=== GENREATE BANNER ===')
    sendRequest.send(self, 'generatebanner', {'banner': ''})
        