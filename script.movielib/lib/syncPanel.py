# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import urllib2
import hashlib
import json
import base64
import hashlib

__addon__               = xbmcaddon.Addon()
__addonname__           = __addon__.getAddonInfo('name')
__lang__                = __addon__.getLocalizedString

import debug
import sendRequest
import art

def sync(self):
    # get panels list from XBMC
    library = [
        {
            'json': '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["cast", "country", "genre", "studio", "director"]}, "id": 1}',
            'lib': 'movies'
        },
        {
            'json': '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["cast", "genre"]}, "id": 1}',
            'lib': 'tvshows'
        }
    ]
    
    self.panelsLang = {'actor': __lang__(32110), 'genre': __lang__(32111), 'country': __lang__(32112), 'studio': __lang__(32113), 'director': __lang__(32114)}
    
    self.panelsXBMC = {'actor': set(), 'genre': set(), 'country': set(), 'studio': set(), 'director': set()}
    actor_temp = set()
    actorTHUMB = {}
    for l in library:
        jsonGetPanel = xbmc.executeJSONRPC(l['json'])
        print jsonGetPanel
        jsonGetPanel = unicode(jsonGetPanel, 'utf-8', errors='ignore')
        jsonGetPanelResponse = json.loads(jsonGetPanel)

                                
        if 'result' in jsonGetPanelResponse and l['lib'] in jsonGetPanelResponse['result']:
            for video in jsonGetPanelResponse['result'][l['lib']]:
                for panel in self.panelsXBMC.keys():
                    if panel == 'actor':
                        if 'cast' in video:
                            for actor in video['cast']:
                                if actor != '':
                                    self.panelsXBMC['actor'].add(actor['name'].strip())
                                if 'thumbnail' in actor and actor['thumbnail'] != '':
                                    actor_temp.add((actor['name'].strip(), actor['thumbnail']))
                    else:
                        if panel in video:
                            for p in video[panel]:
                                if p != '':
                                    self.panelsXBMC[panel].add(p.strip())
    for a in actor_temp:
        actorTHUMB[a[0]] = a[1]
        
    # prepare hash tables
    hashXBMC = {}
    for pan in self.panelsXBMC.keys():
        hashXBMC[pan] = hashlib.md5(str(self.panelsXBMC[pan])).hexdigest()
        debug.debug('[' + pan + 'XBMC]: ' + str(self.panelsXBMC[pan]))
    debug.debug('[actorTHUMB]: ' + str(actorTHUMB))
    debug.debug('[hashXBMC]: ' + str(hashXBMC))
    
    # check hash and set panels to update
    panelsToUpdate = set()
    for n,h in hashXBMC.items():
        if h != self.hashSITE[n]:
            panelsToUpdate.add(n)
            debug.debug('[' + n.upper() + ' UPDATE NEEDED]')
        else:
            debug.debug('[' + n.upper() + ' UPDATE NOT NEEDED]')
    
    # update panel
    for panel in panelsToUpdate:
        
        debug.debug('=== ' + panel.upper()  + ' SYNC START ===')
        
        # get panel from site
        panelsSite = sendRequest.send(self, 'showpanel&t=' + panel)
        if panelsSite is False:
            return False
        debug.debug('[' + panel + 'SITE]: ' + str(panelsSite))
        
        # prepare panel to add and remove
        toAdd = set(self.panelsXBMC[panel]) - set(panelsSite.keys())
        debug.debug('[' + panel + 'ToAdd]: ' + str(toAdd))
        toRemove = set(panelsSite.keys()) - set(self.panelsXBMC[panel])
        debug.debug('[' + panel + 'ToRemove]: ' + str(toRemove))
        
        # add panels
        if len(toAdd) > 0:
            value = {}
            valueThumb = {}
            countToAdd = len(toAdd)
            step = 500
            addedCount = 0
            next = step
            self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32204) + ' ' + self.panelsLang[panel])
            
            for a in toAdd:
                
                # progress bar update
                p = int((float(100) / float(countToAdd)) * float(addedCount))
                self.progBar.update(p, str(addedCount + 1) + '/' + str(countToAdd) + ' - ' + a)
                
                # push actor thumb
                if self.setSITE['xbmc_actors'] == '1' and 'actor' in panel and a in actorTHUMB and len(actorTHUMB[a]) > 0:
                    t = art.create(urllib2.unquote((actorTHUMB[a]).encode('utf-8')).replace('\\', '/'), 'a', 75, 100, 70)
                    if len(t) > 0:
                        name = hashlib.md5(a.encode('utf-8')).hexdigest()[:10]
                        valueThumb[name] = base64.b64encode(t)

                value[addedCount] = a.encode('utf-8')
                
                addedCount += 1
                if addedCount == next or addedCount == countToAdd:
                
                    if sendRequest.send(self, 'addpanel&t=' + panel, value) is False:
                        self.progBar.close()
                        return False
                    
                    if len(valueThumb) > 0:
                        if sendRequest.send(self, 'addthumb', valueThumb) is False:
                            self.progBar.close()
                            return False
                            
                    next = next + step
                    value = {}
                    valueThumb = {}
                    
            debug.notify(__lang__(32104).encode('utf-8') + ' ' + str(addedCount) + ' ' + self.panelsLang[panel].encode('utf-8'))
            
            self.progBar.close()
            
        # remove panels
        if len(toRemove) > 0:
            value = {}
            removedCount = 0
            for r in toRemove:
                value[removedCount] = r.encode('utf-8')
                removedCount += 1
            if sendRequest.send(self, 'removepanel&t=' + panel, value) is False:
                return False
            
        # update hash
        value = {panel: hashXBMC[panel]}
        if sendRequest.send(self, 'updatehash', value) is False:
            return False