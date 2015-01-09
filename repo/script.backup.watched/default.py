# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import json
import os
import ntpath
import time
import re

__addon__ = xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__datapath__ = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/') + '/'
__path_img__ = __addonpath__ + '/images/'
__lang__ = __addon__.getLocalizedString

ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_STEP_BACK = 21
ACTION_NAV_BACK = 92
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_MOUSE_MOVE = 107
ACTION_BACKSPACE = 110
KEY_BUTTON_BACK = 275

# GUI
class GUI(xbmcgui.WindowDialog):

    def __init__(self):

        self.button = {}
        bgResW = 520
        bgResH = 150
        bgPosX = (1280 - bgResW) / 2
        bgPosY = (720 - bgResH) / 2
        self.start = 1
        
        # add controls
        self.bg = xbmcgui.ControlImage(bgPosX, bgPosY, bgResW, bgResH, __path_img__ + 'bg.png')
        self.addControl(self.bg)
        
        self.strActionInfo = xbmcgui.ControlLabel(bgPosX, bgPosY+20, 520, 200, '', 'font14', '0xFFFFFFFF', alignment=2)
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel(__lang__(32100))
        
        self.button[1] = xbmcgui.ControlButton(bgPosX+30, bgPosY+80, 220, 50, __lang__(32101), alignment=6, font='font13')
        self.addControl(self.button[1])
        self.setFocus(self.button[1])
        
        self.button[2] = xbmcgui.ControlButton(bgPosX+270, bgPosY+80, 220, 50, __lang__(32102), alignment=6, font='font13')
        self.addControl(self.button[2])
        
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_STEP_BACK or action == ACTION_BACKSPACE or action == ACTION_NAV_BACK or action == KEY_BUTTON_BACK or action == ACTION_MOUSE_RIGHT_CLICK:
            self.close()
        if action == ACTION_MOVE_LEFT:
            if self.start > 1:
                self.start = self.start - 1
            self.setFocus(self.button[self.start])
        if action == ACTION_MOVE_RIGHT:
            if self.start < 2:
                self.start = self.start + 1
            self.setFocus(self.button[self.start])
            
    def onControl(self, control):
        if control == self.button[1]:
            self.close()
            Backup()
            
        if control == self.button[2]:
            self.close()
            
            # get avalible files
            fi = []
            dir = os.listdir(__datapath__)
            # append to list
            for file in dir:
                find = re.findall('w_([0-9]{14}).json', file)
                if len(find) > 0:
                    fi.append(find[0])
                    
            if len(fi) > 0:
                restore = Restore(fi)
                restore.doModal(fi)
                del restore
            else:
                xbmcgui.Dialog().ok(__addonname__, __lang__(32104))
                
class Backup:
    # backup all watched status and save to file
    def __init__(self):
        jsonGetWatchedM = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter": {"field": "playcount", "operator": "greaterthan", "value": "0"}, "properties": ["playcount", "lastplayed", "dateadded", "file"]}, "id": 1}')
        jsonGetWatchedM = unicode(jsonGetWatchedM, 'utf-8')
        jsonGetWatchedM = json.loads(jsonGetWatchedM)
        
        jsonGetWatchedE = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter": {"field": "playcount", "operator": "greaterthan", "value": "0"}, "properties": ["playcount", "lastplayed", "dateadded", "file"]}, "id": 1}')
        jsonGetWatchedE = unicode(jsonGetWatchedE, 'utf-8')
        jsonGetWatchedE = json.loads(jsonGetWatchedE)
        
        movies = []
        if 'result' in jsonGetWatchedM:
            movies = movies + jsonGetWatchedM['result']['movies']
        
        if 'result' in jsonGetWatchedE:
            movies = movies + jsonGetWatchedE['result']['episodes']
            
        # create dir in addon data if not exist
        if not xbmcvfs.exists(__datapath__):
            xbmcvfs.mkdir(__datapath__)
        
        # remove old files
        b_files = os.listdir(__datapath__)
        r_files = []
        for file in b_files:
            if re.search('w_([0-9]{14}).json', file):
                r_files.append(file)
        
        for r in r_files[:-4]:
            os.remove(__datapath__ + r)
        
        # create new file with data
        a_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        f = xbmcvfs.File(__datapath__ + 'w_' + a_time + '.json', 'w') 
        f.write(json.dumps(movies))
        f.close()
        xbmcgui.Dialog().ok(__addonname__, __lang__(32103))

class Restore(xbmcgui.WindowDialog):
    def __init__(self, fi):
        
        btW = 400
        btH = 50
        btPosX = (1280 - btW) / 2
        btPosY = 160
        self.start = 1
             
        # sort and transform to to dict
        fi.reverse()
        self.files = {}
        cFiles = 0
        for  f in fi:
            cFiles = cFiles + 1
            self.files[cFiles] = f
        self.start = 1
        self.end = cFiles
        
        # background
        bgW = btW + 40
        bgH = (cFiles * btH) + (cFiles * 20) + 20
        bgPosX = btPosX - 20
        bgPosY = btPosY + btH
        
        self.bg = xbmcgui.ControlImage(bgPosX, bgPosY, bgW, bgH, __path_img__ + 'bg.png')
        self.addControl(self.bg)
        
        # buttons
        start = 0
        self.button = {}
        for file in self.files:
            start += 1
            l_date = self.files[file][6:8] + '.' + self.files[file][4:6] + '.' + self.files[file][0:4] + ' ' + self.files[file][8:10] + ':' + self.files[file][10:12] + ':' + self.files[file][12:14]
            self.button[start] = xbmcgui.ControlButton(btPosX, btPosY + (btH * start) + (start * 20), btW, btH, l_date, alignment=6, font='font13')
            self.addControl(self.button[start])
        self.setFocus(self.button[1])
        
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_STEP_BACK or action == ACTION_BACKSPACE or action == ACTION_NAV_BACK or action == KEY_BUTTON_BACK or action == ACTION_MOUSE_RIGHT_CLICK:
            self.close()
        if action == ACTION_MOVE_UP:
            if self.start > 1:
                self.start = self.start - 1
            self.setFocus(self.button[self.start])
        if action == ACTION_MOVE_DOWN:
            if self.start < self.end:
                self.start = self.start + 1
            self.setFocus(self.button[self.start])
            
    def onControl(self, control):
        for file in self.files:
            if control == self.button[file]:
                self.close()
                self.restore(file)
            
    def restore(self, file):
        
        # get settings
        self.setMethod      = __addon__.getSetting('method')
        
        # read watched status from file
        f = xbmcvfs.File(__datapath__ + 'w_' + self.files[file] + '.json', 'r')
        result = f.read()
        f.close()
        
        prog = Bar()
        prog.create(__lang__(32201), __addonname__ + ', ' + __lang__(32200))
        
        jsonRead = json.loads(result)
        
        if len(jsonRead) > 0:
            
            # get file names from XBMC
            jsonGetWatchedM = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "file"]}, "id": 1}')
            jsonGetWatchedM = unicode(jsonGetWatchedM, 'utf-8')
            jsonGetWatchedM = json.loads(jsonGetWatchedM)
            
            jsonGetWatchedE = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["title", "file"]}, "id": 1}')
            jsonGetWatchedE = unicode(jsonGetWatchedE, 'utf-8')
            jsonGetWatchedE = json.loads(jsonGetWatchedE)
            
            jsonGetWatchedR = []
            
            if 'result' in jsonGetWatchedM:
                jsonGetWatchedR = jsonGetWatchedR + jsonGetWatchedM['result']['movies']
                
            if 'result' in jsonGetWatchedE:
                jsonGetWatchedR = jsonGetWatchedR + jsonGetWatchedE['result']['episodes']
            
            leng = len(jsonRead)
            start = 0
            
            for r in jsonRead:
            
                if 'movieid' in r.keys():
                    method = 'VideoLibrary.SetMovieDetails'
                    video = 'movieid'
                
                if 'episodeid' in r.keys():
                    method = 'VideoLibrary.SetEpisodeDetails'
                    video = 'episodeid'
                    
                start += 1
                p = int((float(100) / float(leng)) * float(start))
                for m in jsonGetWatchedR:

                    # by path
                    if '0' in self.setMethod:
                        if r['file'] == m['file']:
                            prog.update(p, m['title'])
                            jsonSetWatched = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "' + method + '", "params": {"playcount": ' + str(r['playcount']) + ', "dateadded": "' + r['dateadded'] + '", "lastplayed": "' + r['lastplayed'] + '", "' + video + '": ' + str(m[video]) + '}, "id": 1}')
                    
                    # by filename
                    if '1' in self.setMethod:
                        if ntpath.basename(r['file']) == ntpath.basename(m['file']):
                            prog.update(p, m['title'])
                            jsonSetWatched = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "' + method + '", "params": {"playcount": ' + str(r['playcount']) + ', "dateadded": "' + r['dateadded'] + '", "lastplayed": "' + r['lastplayed'] + '", "' + video + '": ' + str(m[video]) + '}, "id": 1}')
        prog.close()
                    
class Bar:
    def __init__(self):
        self.b = xbmcgui.DialogProgressBG()
    
    def create(self, message, heading):
        self.b.create(heading, message)
    
    def update(self, percent, message, heading=0):
        if heading == 0:
            self.b.update(percent, message=message)
        else:
            self.b.update(percent, heading, message)
        
    def close(self):
        self.b.close()

        
gui = GUI()
gui.doModal()
del gui