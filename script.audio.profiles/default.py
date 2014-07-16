# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import json
import os

__addon__ = xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__datapath__ = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/') + '/'
__path_img__ = __addonpath__ + '/images/'
__lang__ = __addon__.getLocalizedString

ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_STEP_BACK = 21
ACTION_NAV_BACK = 92
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_MOUSE_MOVE = 107
ACTION_BACKSPACE = 110
KEY_BUTTON_BACK = 275

class Start:

    def __init__(self):
        # detect mode, check args
        try:
            mode = str(sys.argv[1])
        except:
            mode = False
        
        # start GUI or switch audio
        if mode == False:
            gui = GUI()
            gui.doModal()
            del gui
        else:
            switch = Switch()
            switch.check(mode)

# GUI to configure audio profiles
class GUI(xbmcgui.WindowDialog):

    def __init__(self):
        # set vars
        self.sName1         = __addon__.getSetting('name1')
        self.sName2         = __addon__.getSetting('name2')
        self.button = [0]
        bgResW = 520
        bgResH = 170
        bgPosX = (1280 - bgResW) / 2
        bgPosY = (720 - bgResH) / 2
        self.start = 1
        
        # add controls
        self.bg = xbmcgui.ControlImage(bgPosX, bgPosY, bgResW, bgResH, __path_img__ + 'bg.png')
        self.addControl(self.bg)
        self.strActionInfo = xbmcgui.ControlLabel(bgPosX, bgPosY+20, 520, 200, '', 'font14', '0xFFFFFFFF', alignment=2)
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel(__lang__(32010))
        self.button.append(xbmcgui.ControlButton(bgPosX+30, bgPosY+80, 220, 50, self.sName1, alignment=6, font='font13'))
        self.addControl(self.button[1])
        self.setFocus(self.button[1])
        self.button.append(xbmcgui.ControlButton(bgPosX+270, bgPosY+80, 220, 50, self.sName2, alignment=6, font='font13'))
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
            self.save(1)
            self.close()
        if control == self.button[2]:
            self.save(2)
            self.close()
    
    # get audio config and save to file
    def save(self, button):
        jsonGetSysSettings = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"level": "expert", "filter":{"section":"system","category":"audiooutput"}},"id":1}')
        jsonGetSysSettings = unicode(jsonGetSysSettings, 'utf-8')
        jsonGetSysSettings = json.loads(jsonGetSysSettings)

        jsonToWrite = ''
        if 'result' in jsonGetSysSettings:
            for set in jsonGetSysSettings['result']['settings']:
                jsonToWrite = jsonToWrite + '"' + str(set['id']) + '": "' + str(set['value']) + '", '
        jsonToWrite = '{' + jsonToWrite[:-2] + '}'

        if not xbmcvfs.exists(__datapath__):
            xbmcvfs.mkdir(__datapath__)
        f = xbmcvfs.File(__datapath__ + 'profile' + str(button) + '.json', 'w')
        result = f.write(jsonToWrite)
        f.close()

# switching profiles
class Switch:

    def check(self, mode):
        # check profile config
        if not xbmcvfs.exists(__datapath__ + 'profile1.json'):
            Message().msg(__lang__(32011))
            return False
        if not xbmcvfs.exists(__datapath__ + 'profile2.json'):
            Message().msg(__lang__(32011))
            return False
        # check mode
        if mode == '0':
            self.toggle(mode)
        else:
            self.profile(mode)
        
    def toggle(self, mode):
        # create profile file
        if not xbmcvfs.exists(__datapath__):
            xbmcvfs.mkdir(__datapath__)
        try:
            f = xbmcvfs.File(__datapath__ + 'profile')
            profile = f.read()
            f.close()
            if profile == '1':
                profile = '2'
            else:
                profile = '1'
        except:
            profile = '1'
        
        self.profile(profile)
        
    def profile(self, profile):
        self.sName = [0, __addon__.getSetting('name1'), __addon__.getSetting('name2')]
        
        # read settings from profile
        f = xbmcvfs.File(__datapath__ + 'profile'+profile+'.json', 'r')
        result = f.read()
        jsonResult = json.loads(result)
        f.close()
        
        for req in jsonResult:
            if req == 'audiooutput.audiodevice' or req == 'audiooutput.passthroughdevice':
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting": "' + req + '", "value": "' + jsonResult[req] + '"}, "id": 1}')
            else:
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting": "' + req + '", "value": ' + jsonResult[req] + '}, "id": 1}')
        
        Message().msg(self.sName[int(profile)])
        
        # write curent profile
        f = xbmcvfs.File(__datapath__ + 'profile', 'w')
        f.write(profile)
        f.close()

class Message:
    def msg(self, msg):
        xbmc.executebuiltin('Notification(Switch Audio,'+msg+', 4000, ' + __addonpath__ + '/icon.png)')
        
Start()