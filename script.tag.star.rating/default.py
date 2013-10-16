# -*- coding: utf-8 -*-

import json
import xbmcgui
import xbmc
import re
import sys
import os
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, "resources" )
__path_img__            = __addonpath__ + '/images'

ACTION_PREVIOUS_MENU        = 10
ACTION_MOVE_LEFT            = 1
ACTION_MOVE_RIGHT           = 2
ACTION_MOVE_UP              = 3
ACTION_MOVE_DOWN            = 4
ACTION_STEP_BACK            = 21
ACTION_NAV_BACK             = 92
ACTION_MOUSE_RIGHT_CLICK    = 101
ACTION_MOUSE_MOVE           = 107
ACTION_BACKSPACE            = 110
KEY_BUTTON_BACK             = 275

class StarRating():
    def __init__(self):
        
        # set vars
        self.tagPrefix = __addon__.getSetting('tagPrefix')
        self.otherTags = []
        self.rating = 0
        self.otherTags = ''
        self.main()
        
    def main(self):

        # check if arg exist
        try:
            arg = sys.argv[1]
        except:
            return False
        
        if re.search('INFO', arg):
            self.movieID = xbmc.getInfoLabel(arg)
        else:
            self.movieID = arg
        
        # check prefix lenght
        if len(self.tagPrefix) <= 4:
            msg = __lang__(32100)
            self.msg(msg)
            return False
        
        # check empty ID
        if self.movieID == '':
            return False
        
        self.getTags()
        
    def getTags(self):
        
        # get tags and mediatype
        jsonGetMovieDetails = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["tag", "title"], "movieid": '+self.movieID+'}, "id": "1"}'
        jsonGetMovieDetailsResponse = json.loads(xbmc.executeJSONRPC(jsonGetMovieDetails))
        
        jsonGetTVShowDetails = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": {"properties": ["tag", "title"], "tvshowid": '+self.movieID+'}, "id": "1"}'
        jsonGetTVShowDetailsResponse = json.loads(xbmc.executeJSONRPC(jsonGetTVShowDetails))
        
        try:
            mediaType = sys.argv[2]
        except:
            try:
                titleMovie = jsonGetMovieDetailsResponse['result']['moviedetails']['title'].encode("utf-8")
            except:
                titleMovie = False
            if titleMovie == xbmc.getInfoLabel("ListItem.Title"):
                mediaType = 'movie'
            try:
                titleTV = jsonGetTVShowDetailsResponse['result']['tvshowdetails']['title'].encode("utf-8")
            except:
                titleTV = False
            if titleTV == xbmc.getInfoLabel("ListItem.Title"):
                mediaType = 'tvshow'
        
        try:
            mediaType
        except:
            return False
        
        if mediaType == 'movie':
            tagList = jsonGetMovieDetailsResponse['result']['moviedetails']['tag']
            title = jsonGetMovieDetailsResponse['result']['moviedetails']['title'].encode("utf-8")
        elif mediaType == 'tvshow':
            tagList = jsonGetTVShowDetailsResponse['result']['tvshowdetails']['tag']
            title = jsonGetTVShowDetailsResponse['result']['tvshowdetails']['title'].encode("utf-8")
        else:
            return False

        # check tags
        if len(tagList) != 0:

            # if rating tag exsist get rating, append other tag to list
            for tag in tagList:
                if re.search(self.tagPrefix + '\s[0-9]+', tag):
                    self.rating = int(re.compile('[0-9]+').search(tag).group(0))
                else:
                    self.otherTags = self.otherTags + '"' + (tag.encode("utf-8")) + '", '

            self.otherTags = self.otherTags[:-2]
        
        # display window rating
        display = WindowRating(self.tagPrefix, title, self.rating, self.otherTags, self.movieID, mediaType)
        display.doModal()
        del display

    def msg(self, msg):        
        xbmcgui.Dialog().ok(__addonname__, msg)

class WindowRating(xbmcgui.WindowDialog):
    
    def __init__(self, tagPrefix, title, rating, otherTags, movieID, mediaType):
        
        # set window property to true
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.window.setProperty('StarRating', 'true')
        
        # set vars
        self.tagPrefix = tagPrefix
        self.title = title
        self.rating = rating
        self.otherTags = otherTags
        self.movieID = movieID
        self.button = []
        
        if mediaType == 'movie':
            self.mediaDatabase = 'SetMovieDetails'
            self.typeID = 'movieid'
        elif mediaType == 'tvshow':
            self.mediaDatabase = 'SetTVShowDetails'
            self.typeID = 'tvshowid'
        
        # create window
        bgResW = 520
        bgResH = 170
        bgPosX = (1280 - bgResW) / 2
        bgPosY = (720 - bgResH) / 2
        self.bg = xbmcgui.ControlImage(bgPosX, bgPosY, bgResW, bgResH, __path_img__+'//bg.png')
        self.addControl(self.bg)
        self.labelTitle = xbmcgui.ControlLabel(bgPosX+20, bgPosY+26, bgResW-40, bgResH-40, '[B]'+self.title+'[/B]', 'font14', '0xFF0084ff',  alignment=2)
        self.addControl(self.labelTitle)
        self.label = xbmcgui.ControlLabel(bgPosX+20, bgPosY+64, bgResW-40, bgResH-40, __lang__(32101)+':', 'font13', '0xFFFFFFFF',  alignment=2)
        self.addControl(self.label)
        
        # create button list
        self.starLeft = bgPosX+40
        self.starTop = bgPosY+106
        for i in range(11):
            if i == 0:
                self.button.append(xbmcgui.ControlButton(self.starLeft, self.starTop, 30, 30, "", focusTexture=__path_img__ + '//star0f.png', noFocusTexture=__path_img__ + '//star0.png'))
            else:
                if i <= self.rating:
                    self.button.append(xbmcgui.ControlButton(self.starLeft+(i*40), self.starTop, 30, 30, "", focusTexture=__path_img__ + '//star2f.png', noFocusTexture=__path_img__ + '//star2.png'))
                else:
                    self.button.append(xbmcgui.ControlButton(self.starLeft+(i*40), self.starTop, 30, 30, "", focusTexture=__path_img__ + '//star2f.png', noFocusTexture=__path_img__ + '//star1.png'))
                
            self.addControl(self.button[i])
        self.setFocus(self.button[self.rating])
        
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_STEP_BACK or action == ACTION_BACKSPACE or action == ACTION_NAV_BACK or action == KEY_BUTTON_BACK or action == ACTION_MOUSE_RIGHT_CLICK:
            self.close()
        if action == ACTION_MOVE_RIGHT or action == ACTION_MOVE_UP:
            if self.rating < 10:
                self.rating = self.rating + 1
            self.setFocus(self.button[self.rating])
        if action == ACTION_MOVE_LEFT or action == ACTION_MOVE_DOWN:
            if self.rating > 0:
                self.rating = self.rating - 1
            self.setFocus(self.button[self.rating])
        
    def onControl(self, control):
        # save tag using JSON
        for i in range(11):
            if control == self.button[i]:
                if i == 0:
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.' + self.mediaDatabase + '", "params": {"'+self.typeID+'" : ' + self.movieID + ', "tag":[' + self.otherTags + ']}}')
                else:
                    if len(self.otherTags) > 0:
                        self.otherTags = self.otherTags + ', '
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.' + self.mediaDatabase + '", "params": {"'+self.typeID+'" : ' + self.movieID + ', "tag":[' + self.otherTags + '"' + self.tagPrefix + ' ' + str(i) + '"]}}')
                self.close()

# check window property if not exist run script
window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
if window.getProperty('StarRating') != 'true':
    StarRating()
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    window.setProperty('StarRating', 'false')


