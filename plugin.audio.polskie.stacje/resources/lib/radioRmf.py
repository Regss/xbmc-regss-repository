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
    
        list = [
            ['RMF FM', 'http://rmfon.pl/n/rmffm.pls', ''],
            ['RMF Classic rock', 'http://rmfon.pl/n/rmfclassicrock.pls', ''],
            ['RMF Dance', 'http://rmfon.pl/n/rmfdance.pls', ''],
            ['RMF R&B', 'http://rmfon.pl/n/rmfrnb.pls', ''],
            ['RMF MAXXX', 'http://rmfon.pl/n/rmfmaxxx.pls', ''],
            ['RMF Classic', 'http://rmfon.pl/n/rmfclassic.pls', ''],
            ['RMF Poplista', 'http://rmfon.pl/n/rmfpoplista.pls', ''],
            ['RMF Polskie przeboje', 'http://rmfon.pl/n/rmfpprzeboje.pls', ''],
            ['RMF Słoneczne przeboje', 'http://miastomuzyki.pl/n/rmfsprzeboje.pls', ''],
            ['RMF Chillout', 'http://rmfon.pl/n/rmfchillout.pls', ''],
            ['RMF Bravo', 'http://rmfon.pl/n/rmfbravo.pls', ''],
            ['RMF LOVE', 'http://rmfon.pl/n/rmflove.pls', ''],
            ['RMF Gold', 'http://rmfon.pl/n/rmfgold.pls', ''],
            ['RMF Smooth jazz', 'http://rmfon.pl/n/rmfsmoothjazz.pls', ''],
            ['RMF Święta', 'http://rmfon.pl/n/rmfswieta.pls', ''],
            ['RMF eLO', 'http://rmfon.pl/n/rmfelo.pls', ''],
            ['RMF Przebój roku', 'http://rmfon.pl/n/rmfprzebojroku.pls', ''],
            ['RMF MAXXX Hop bęc', 'http://rmfon.pl/n/rmfhopbec.pls', ''],
            ['RMF Party', 'http://rmfon.pl/n/rmfparty.pls', ''],
            ['RMF 80s', 'http://rmfon.pl/n/rmf80s.pls', ''],
            ['RMF Electro shockwave', 'http://rmfon.pl/n/rmfelectroshockwave.pls', ''],
            ['RMF Hot new', 'http://rmfon.pl/n/rmfhotnew.pls', ''],
            ['RMF Alternatywa', 'http://rmfon.pl/n/rmfalternatywa.pls', ''],
            ['RMF Club', 'http://rmfon.pl/n/rmfclub.pls', ''],
            ['RMF Lady Pank', 'http://rmfon.pl/n/rmfladypank.pls', ''],
            ['RMF Depeche Mode', 'http://rmfon.pl/n/rmfdepechemode.pls', ''],
            ['RMF Hard & heavy', 'http://miastomuzyki.pl/n/rmfhardandheavy.pls', ''],
            ['RMF Muzyka filmowa', 'http://rmfon.pl/n/rmffilmowa.pls', ''],
            ['RMF Polski rock', 'http://rmfon.pl/n/rmfpolskirock.pls', ''],
            ['RMF Hip hop', 'http://rmfon.pl/n/rmfhiphop.pls', ''],
            ['RMF PRL', 'http://rmfon.pl/n/rmfprl.pls', ''],
            ['RMF Blues', 'http://rmfon.pl/n/rmfblues.pls', ''],
            ['RMF Reggae', 'http://rmfon.pl/n/rmfreggae.pls', ''],
            ['RMF Rumor', 'http://rmfon.pl/n/rmfrumor.pls', ''],
            ['RMF Baby', 'http://rmfon.pl/n/rmfbaby.pls', ''],
            ['RMF 60s', 'http://rmfon.pl/n/rmf60s.pls', ''],
            ['RMF 70s', 'http://rmfon.pl/n/rmf70s.pls', ''],
            ['RMF 90s', 'http://rmfon.pl/n/rmf90s.pls', ''],
            ['RMF 50s', 'http://rmfon.pl/n/rmf50s.pls', ''],
            ['RMF Szanty', 'http://rmfon.pl/n/rmfszanty.pls', ''],
            ['RMF Club breaks', 'http://rmfon.pl/n/rmfclubbreaks.pls', ''],
            ['RMF Polski hip hop', 'http://rmfon.pl/n/rmfpolskihiphop.pls', ''],
            ['RMF Cuba', 'http://rmfon.pl/n/rmfcuba.pls', ''],
            ['RMF Francais', 'http://rmfon.pl/n/rmffrancais.pls', ''],
            ['RMF Nippon', 'http://rmfon.pl/n/rmfnippon.pls', ''],
            ['RMF Flamenco', 'http://rmfon.pl/n/rmfflamenco.pls', ''],
            ['RMF Queen', 'http://rmfon.pl/n/rmfqueen.pls', ''],
            ['RMF Groove', 'http://rmfon.pl/n/rmfgroove.pls', ''],
            ['RMF Piosenka literacka', 'http://miastomuzyki.pl/n/rmfpiosenkaliteracka.pls', ''],
            ['RMF Kalinka', 'http://rmfon.pl/n/rmfkalinka.pls', ''],
            ['RMF Celtic', 'http://rmfon.pl/n/rmfceltic.pls', ''],
            ['RMF Grunge', 'http://rmfon.pl/n/rmfgrunge.pls', ''],
            ['RMF FMF', 'http://rmfon.pl/n/rmffmf.pls', ''],
            ['RMF Cover', 'http://rmfon.pl/n/rmfcover.pls', ''],
            ['RMF Michael Jackson', 'http://miastomuzyki.pl/n/rmfmichaeljackson.pls', ''],
            ['RMF Pacuda country', 'http://rmfon.pl/n/rmfcountry.pls', ''],
            ['RMF Beatlemania', 'http://rmfon.pl/n/rmfbeatlemania.pls', ''],
            ['RMF Styl', 'http://rmfon.pl/n/rmfstyl.pls', ''],
            ['RMF 2000', 'http://rmfon.pl/n/rmf2000.pls', ''],
            ['RMF 20 lat RMF FM', 'http://rmfon.pl/n/rmf20lat.pls', ''],
            ['RMF Punk', 'http://rmfon.pl/n/rmfpunk.pls', ''],
            ['RMF Rock progresywny', 'http://miastomuzyki.pl/n/rmfrockprogresywny.pls', ''],
            ['RMF Chopin', 'http://rmfon.pl/n/rmfchopin.pls', ''],
            ['RMF Muzyka klasyczna', 'http://miastomuzyki.pl/n/rmfmuzykaklasyczna.pls', ''],
            ['RMF World music', 'http://rmfon.pl/n/rmfworldmusic.pls', ''],
            ['RMF Football', 'http://rmfon.pl/n/rmffootball.pls', ''],
            ['RMF Nostalgia', 'http://rmfon.pl/n/rmfnostalgia.pls', ''],
            ['RMF 2', 'http://rmfon.pl/n/rmf2.pls', ''],
            ['RMF 3', 'http://rmfon.pl/n/rmf3.pls', ''],
            ['RMF 4', 'http://rmfon.pl/n/rmf4.pls', ''],
            ['RMF 5', 'http://rmfon.pl/n/rmf5.pls', ''],
            ['RMF MAXXX Ibiza', 'http://rmfon.pl/n/rmfibiza.pls', ''],
            ['RMF Poplista 10 lat', 'http://rmfon.pl/n/rmfpoplista10lat.pls', ''],
            ['RMF Hop bęc old school', 'http://rmfon.pl/n/rmfhopbecoldschool.pls', ''],
            ['RMF Sade', 'http://rmfon.pl/n/rmfsade.pls', ''],
            ['RMF 70s disco', 'http://rmfon.pl/n/rmf70sdisco.pls', ''],
            ['RMF 80s disco', 'http://rmfon.pl/n/rmf80sdisco.pls', ''],
            ['RMF Polskie disco', 'http://rmfon.pl/n/rmfpolskiedisco.pls', ''],
            ['RMF Niezapomniane melodie', 'http://rmfon.pl/n/rmfniezapomnianemelodie.pls', ''],
            ['RMF Best of RMFON', 'http://rmfon.pl/n/bestofrmfon.pls', ''],
            ['RMF w pracy', 'http://rmfon.pl/n/rmfwpracy.pls', ''],
            ['RMF Relaks', 'http://rmfon.pl/n/rmfrelaks.pls', ''],
            ['RMF Fitness', 'http://rmfon.pl/n/rmffitness.pls', ''],
            ['RMF Fitness rock', 'http://rmfon.pl/n/rmffitnessrock.pls', ''],
            ['RMF Top 5 dance', 'http://rmfon.pl/n/rmftop5dance.pls', ''],
            ['RMF Top 5 pl', 'http://rmfon.pl/n/rmftop5pl.pls', ''],
            ['RMF Top 5 pop', 'http://rmfon.pl/n/rmftop5pop.pls', ''],
            ['RMF Top 5 R&B', 'http://rmfon.pl/n/rmftop5rnb.pls', ''],
            ['RMF Top 5 rock', 'http://rmfon.pl/n/rmftop5rock.pls', ''],
            ['RMF Dubstep', 'http://rmfon.pl/n/rmfdubstep.pls', ''],
            ['RMF 90s dance', 'http://rmfon.pl/n/rmf90sdance.pls', ''],
            ['RMF Karnawał', 'http://rmfon.pl/n/rmfkarnawal.pls', ''],
            ['RMF Classic karnawał', 'http://rmfon.pl/n/rmfclassickarnawal.pls', ''],
            ['RMF Rio', 'http://rmfon.pl/n/rmfrio.pls', ''],
            ['RMF Top 5 hot new', 'http://rmfon.pl/n/rmftop5hotnew.pls', ''],
            ['RMF Tekściory', 'http://rmfon.pl/n/rmfteksciory.pls', ''],
            ['Radiofonia', 'http://rmfon.pl/n/radiofonia.pls', '']
            ]

        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?rmf_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
                    
            opener = urllib2.build_opener()
            pageRadioPLS = opener.open(list[int(self.opt2)][1]).read()
            
            matchesIP = re.compile('(http://[^\s]+)\s').findall(pageRadioPLS)
                
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = matchesIP[0]
        
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            