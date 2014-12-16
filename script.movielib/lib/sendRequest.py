# -*- coding: utf-8 -*-

import xbmcaddon
import urllib
import urllib2
import json
import time

__addon__               = xbmcaddon.Addon()
__lang__                = __addon__.getLocalizedString

import debug

def send(self, option, values=''):
    
    debug.debug('[REQUEST]: ' + self.setXBMC['URL'] + option)
    debug.debug('[REQUEST]: ' + str(values))
    
    # try send data
    data = urllib.urlencode(values, True)
    data_len = len(data)
    
    debug.debug('[REQUEST DATA SIZE]: ' + str(data_len) + ' bytes')
    
    if option != 'checksettings' and data_len > self.setSITE['POST_MAX_SIZE_B']:
        debug.notify(__lang__(32116).encode('utf-8'))
        debug.debug('[REQUEST ERROR]: Data too large to send, server can takes only ' + str(self.setSITE['POST_MAX_SIZE_B']) + ' bytes')
        return False

    for l in range(1, 4):
        try:
            opener = urllib2.build_opener()
            response = opener.open(self.setXBMC['URL'] + option, data)
        except Exception as Error:
            conn = False
            debug.debug('Can\'t connect to: ' + self.setXBMC['URL'] + option)
            debug.debug('[REQUEST ERROR]: ' + str(Error))
            if l < 3:
                debug.debug('[REQUEST]: Wait 5 secs and retring ' + str(l))
            time.sleep(15)
        else:
            conn = True
            break;
        
    if conn != True:
        debug.notify(__lang__(32100).encode('utf-8'))
        return False
        
    output = response.read()
    debug.debug('[RESPONSE]: ' + str(output))
    
    # if no values return json
    if values == '':
        try:
            output = unicode(output, 'utf-8', errors='ignore')
            output = json.loads(output)
        except Exception as Error:
            debug.debug('[GET JSON ERROR]: ' + str(Error))
            return False
    else:
        #get errors
        if len(output) > 0 and 'ERROR:' in output:
            debug.notify(__lang__(32102).encode('utf-8'))
            return False
    
    return output
        