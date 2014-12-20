# -*- coding: utf-8 -*-

import os
import xbmcvfs

import art
import urllib2
import base64
import hashlib
import debug

def prep(self, m, v):
    #panels values
    panelsValue = {}
    for panel in self.panels:
        if panel == 'actor':
            val = [];
            if 'cast' in m:
                for cast in m['cast']:
                    if len(cast['name']) > 0 and cast['name'].strip() in self.panelsSITE['actor']:
                        val.append(self.panelsSITE['actor'][cast['name'].strip()])
            panelsValue[panel] = val
        else:
            val = []
            if panel in m:
                for l in m[panel]:
                    if len(l) > 0 and l.strip() in self.panelsSITE[panel]:
                        val.append(self.panelsSITE[panel][l.strip()])
            panelsValue[panel] = val
    
    
    # thumbnail for episodes
    if v['table'] == 'episodes' and 'thumbnail' in m:
        thumbnail = art.create(urllib2.unquote((m['thumbnail']).encode('utf-8')).replace('\\', '/'), 'p', 200, 113, 70)
    else:
        thumbnail = ''
    
    # poster
    if self.setSITE['xbmc_posters'] == '1' and v['table'] != 'episodes' and 'thumbnail' in m:
        poster = art.create(urllib2.unquote((m['thumbnail']).encode('utf-8')).replace('\\', '/'), 'p', 200, 294, 70)
    else:
        poster = ''
    
    # fanart
    if self.setSITE['xbmc_fanarts'] == '1' and 'fanart' in m:
        fanart = art.create(urllib2.unquote((m['fanart']).encode('utf-8')).replace('\\', '/'), 'f', 1280, 720, 70)
    else:
        fanart = ''
    
    # extra thumbs
    ex_thumb = []
    ex_size = self.setSITE['xbmc_thumbs_q'].split('x')
    if self.setSITE['xbmc_thumbs'] == '1' and 'file' in m:
        extrathumbs_path = os.path.dirname(m['file'].replace('\\', '/')) + '/extrathumbs/'
        if xbmcvfs.exists(extrathumbs_path) and 'file' in m:
            ex_dir = xbmcvfs.listdir(extrathumbs_path)
            for thumb in ex_dir[1]:
                if len(thumb) > 0 and thumb[:5] == 'thumb' and thumb[-3:] == 'jpg':
                    t = art.create(urllib2.unquote('image://' + extrathumbs_path + thumb).encode('utf-8') + '/', 'e', int(ex_size[0]), int(ex_size[1]), 70)
                    ex_thumb.append(base64.b64encode(t))
        
    # trailer
    if 'trailer' in m and m['trailer'][:4] == 'http':
        trailer = m['trailer']
    elif 'trailer' in m and m['trailer'][:29] == 'plugin://plugin.video.youtube':
        ytid = m['trailer'].split('=')
        trailer = 'http://www.youtube.com/embed/' + ytid[2][0:11]
    else:
        trailer = ''
    
    val = {
        'table': v['table'],
        'id': m[v['id']],
        'title': m['title'].encode('utf-8'),
        'plot': m['plot'].encode('utf-8'),
        'rating': str(round(float(m['rating']), 1)) if 'rating' in m else '',
        'year': m['year'] if 'year' in m else '',
        'runtime': m['runtime'] / 60 if 'runtime' in m else '',
        'genre[]': panelsValue['genre'] if 'genre' in m else '',
        'director[]': panelsValue['director'] if 'director' in m else '',
        'originaltitle': m['originaltitle'].encode('utf-8') if 'originaltitle' in m else '',
        'country[]': panelsValue['country'] if 'country' in m else '',
        'set': m['set'].encode('utf-8') if 'set' in m else '',
        'actor[]': panelsValue['actor'] if 'cast' in m else '',
        'studio[]': panelsValue['studio'] if 'studio' in m else '',
        'premiered': m['premiered'] if 'premiered' in m else '',
        'episode': m['episode'] if 'episode' in m else '',
        'season': m['season'] if 'season' in m else '',
        'tvshow': m['tvshowid'] if 'tvshowid' in m else '',
        'firstaired': m['firstaired'] if 'firstaired' in m else '',
        'file': m['file'].replace('\\', '/').encode('utf-8') if 'file' in m else '',
        'play_count': m['playcount'],
        'last_played': m['lastplayed'],
        'date_added': m['dateadded'],
        'poster': base64.b64encode(poster),
        'fanart': base64.b64encode(fanart),
        'thumbnail': base64.b64encode(thumbnail),
        'thumb[]': ex_thumb,
        'trailer': trailer,
        'hash': hashlib.md5(str(m)).hexdigest()
    }
    if 'streamdetails' in m:
        stream = []
        if len(m['streamdetails']['video']) > 0:
            for s in m['streamdetails']['video']:
                stream.append(';'.join(['v',s['codec'], str(s['aspect']), str(s['width']), str(s['height']), str(s['duration'] / 60), '', '', '', '']))
        
        if len(m['streamdetails']['audio']) > 0:
            for s in m['streamdetails']['audio']:
                stream.append(';'.join(['a', '', '', '', '', '', s['codec'], str(s['channels']), s['language'], '']))
        
        if len(m['streamdetails']['subtitle']) > 0:
            for s in m['streamdetails']['subtitle']:
                stream.append(';'.join(['s', '', '', '', '', '', '', '', '', s['language']]))
        
        val.update({
            'stream[]': stream
        })
    
    # add only values support for this video type
    values = {}
    for q in v['values']:
        if q in val:
            values[q] = val[q]
        
    debug.debug(str(values))
    return values