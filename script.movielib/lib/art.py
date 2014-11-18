# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcvfs
import os
from PIL import Image
import cStringIO
import urllib

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')

import debug

def create(source, i, width, height, q):
    if (source[:5] == 'image'):
        file = source
        temp = __datapath__ + '/temp_' + str(i)
        # if file is stored in smb or nfs copy it to addon_data
        if (source[8:11].lower() == 'smb') or (source[8:11].lower() == 'nfs'):
            copyRes = xbmcvfs.copy(source[8:][:-1], temp)
            if copyRes == True:
                source = temp
            else:
                source = ''
        # if it is a URL
        elif source[8:12] == 'http':
            try:
                source = cStringIO.StringIO(urllib.urlopen(source[8:][:-1]).read())
            except:
                source = ''
        else:
            source = source[8:][:-1]
        # resize image
        try:
            image = Image.open(source)
            h = image.size[1]
            if h > 10:
                if (h > height):
                    image.load()
                    image = image.resize((width, height), Image.ANTIALIAS)
                image.save(temp, 'JPEG', quality=int(q))
                poster_bin = xbmcvfs.File(temp)
                output = poster_bin.read()
                poster_bin.close()
            else:
                output = ''
        except Exception as Error:
            output = ''
            debug.debug(str(file))
            debug.debug(str(Error))
    else:
        output = ''
    return output
        