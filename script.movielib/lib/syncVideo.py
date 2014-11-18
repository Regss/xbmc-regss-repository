# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import hashlib
import json
import time

__addon__               = xbmcaddon.Addon()
__addonname__           = __addon__.getAddonInfo('name')
__lang__                = __addon__.getLocalizedString

import debug
import prepareValues
import sendRequest
import syncPanel

def sync(self, v):
    # define panels
    self.panels = ['actor', 'genre', 'country', 'studio', 'director']

    # get videos from XBMC
    jsonGetVideos = xbmc.executeJSONRPC(v['json'])
    jsonGetVideos = unicode(jsonGetVideos, 'utf-8', errors='ignore')
    jsonGetVideosResponse = json.loads(jsonGetVideos)
    
    # prepare xbmc videos array
    self.videosXBMC = {}
    if 'result' in jsonGetVideosResponse and v['table'] in jsonGetVideosResponse['result']:
        for video in jsonGetVideosResponse['result'][v['table']]:
            self.videosXBMC[str(video[v['id']])] = video
    debug.debug('[' + v['table'] + 'XBMC]: ' + str(self.videosXBMC))
    
    # check hash video library
    if hashlib.md5(str(self.videosXBMC)).hexdigest() == self.hashSITE[v['table']]:
        debug.debug('[' + v['table'].upper() + ' UPDATE NOT NEEDED]')
    else:
        debug.debug('[' + v['table'].upper() + ' UPDATE NEEDED]')
    
        # check if panels update is needed
        if self.panelUpdated == False:
            # sync panels
            debug.debug('=== SYNC PANELS ===')
            if syncPanel.sync(self) is False:
                return False
            self.panelUpdated = True
    
        # get id and hash from site
        videosSite = sendRequest.send(self, 'showvideo&table=' + v['table'], '')
        debug.debug('[' + v['table'] + 'SITE]: ' + str(videosSite))

        # prepare videos to add and remove
        videoToAdd = set(self.videosXBMC.keys()) - set(videosSite.keys())
        debug.debug('[' + v['table'] + 'ToAdd]: ' + str(videoToAdd))
        videoToRemove = set(videosSite.keys()) - set(self.videosXBMC.keys())
        debug.debug('[' + v['table'] + 'ToRemove]: ' + str(videoToRemove))
        
        # prepare videos to update
        videoToUpdate = {}
        for m in self.videosXBMC.keys():
            if m in videosSite:
                
                # if hashes not match update video
                if hashlib.md5(str(self.videosXBMC[m])).hexdigest() != videosSite[m]:
                    
                    # add hash to video array
                    videoToUpdate[m] = self.videosXBMC[m]
        debug.debug('[' + v['table'] + 'ToUpdate]: ' + str(videoToUpdate.keys()))
        
        # add videos
        if len(videoToAdd) > 0:
            debug.debug('=== ADDING VIDEOS ===')
            if add(self, videoToAdd, v, 'add') is False:
                self.progBar.close()
                return False
            self.progBar.close()
            
        # remove videos
        if len(videoToRemove) > 0:
            debug.debug('=== REMOVING VIDEOS ===')
            if remove(self, videoToRemove, v) is False:
                return False
            
        # update videos
        if len(videoToUpdate) > 0:
            debug.debug('=== UPDATING VIDEOS ===')
            if add(self, videoToUpdate, v, 'update') is False:
                self.progBar.close()
                return False
            self.progBar.close()
            
        # update hash
        value = {v['table']: hashlib.md5(str(self.videosXBMC)).hexdigest()}
        sendRequest.send(self, 'updatehash', value)
        
def add(self, videoToAdd, v, opt):
    
    # get new list panels from site
    if len(self.panelsSITE) == 0:
        for a in self.panels:
            # get new list actors from site
            self.panelsSITE[a] = sendRequest.send(self, 'showpanel&t=' + a, '')
            debug.debug('[' + a + 'SITE]: ' + str(self.panelsSITE[a]))
        
    # init progres bar
    addedCount = 0
    countToAdd = len(videoToAdd)
    self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32204 if opt == 'add' else 32209) + ' ' + __lang__(v['lang']))
    
    for video in videoToAdd:
        start_time = time.time()
        
        # progress bar update
        p = int((float(100) / float(countToAdd)) * float(addedCount))
        progYear = ' (' + str(self.videosXBMC[video]['year']) + ')' if 'year' in self.videosXBMC[video] else ''
        self.progBar.update(p, str(addedCount + 1) + '/' + str(countToAdd) + ' - ' + self.videosXBMC[video]['title'] + progYear)
        
        # get values
        values = prepareValues.prep(self, self.videosXBMC[video], v)
        
        # send requst
        if sendRequest.send(self, opt + 'video&t=' + v['table'], values) is False:
            return False
        else:
            addedCount += 1
        debug.debug('[TIME]: ' + str(time.time() - start_time)[0:5])
        
    if addedCount > 0:
        debug.notify(__lang__(32104 if opt == 'add' else 32103).encode('utf-8') + ' ' + str(addedCount) + ' ' + __lang__(v['lang']).encode('utf-8'))

def remove(self, videoToRemove, v):
    
    removedCount = 0
    
    # get values
    values = {}
    for video in videoToRemove:
        removedCount += 1
        values[removedCount] = video
    
    # send requst
    if sendRequest.send(self, 'removevideo&t=' + v['table'], values) is False:
        return False
        
    if removedCount > 0:
        debug.notify(__lang__(32105).encode('utf-8') + ' ' + str(removedCount) + ' ' + __lang__(v['lang']).encode('utf-8'))
