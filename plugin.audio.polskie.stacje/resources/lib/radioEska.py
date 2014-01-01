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
            ['ESKA Gorąca 20', 'http://poznan5-1.radio.pionier.net.pl:8000/eska-stream19-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855149zzOU.jpg/ru-0-r-244,244-n-855149zzOU.jpg'],
            ['ESKA Love', 'http://gramy01.eska.fm:8000/eska-stream38-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855154IysL.jpg/ru-0-r-244,244-n-855154IysL.jpg'],
            ['ESKA Party', 'http://warszawa1-1.radio.pionier.net.pl:8000/pl/eska-stream5-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855156zAIF.jpg/ru-0-r-244,244-n-855156zAIF.jpg'],
            ['ESKA Impreska z Jankesem', 'http://poznan5-2.radio.pionier.net.pl:8000/eska-stream20-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855153Myti.jpg/ru-0-r-244,244-n-855153Myti.jpg'],
            ['ESKA Hity - Nie Tylko Na Czasie', 'http://poznan5.radio.pionier.net.pl:8000/eska-stream14-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855152y7YF.jpg/ru-0-r-244,244-n-855152y7YF.jpg'],
            ['ESKA Global Lista', 'http://wroclaw.radio.pionier.net.pl:8000/pl/eska-stream16-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855148zGIC.jpg/ru-0-r-244,244-n-855148zGIC.jpg'],
            ['ESKA Dance', 'http://wroclaw.radio.pionier.net.pl:8000/pl/eska-stream12-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855146J4Vb.jpg/ru-0-r-244,244-n-855146J4Vb.jpg'],
            ['ESKA R\'N\'B', 'http://warszawa1-1.radio.pionier.net.pl:8000/pl/eska-stream3-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/8551586STJ.jpg/ru-0-r-244,244-n-8551586STJ.jpg'],
            ['ESKA Ballads', 'http://gdansk1-3.radio.pionier.net.pl:8000/pl/eska-stream11-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855141zvyY.jpg/ru-0-r-244,244-n-855141zvyY.jpg'],
            ['ESKA Rap', 'http://warszawa1-1.radio.pionier.net.pl:8000/pl/eska-stream2-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855157XP0f.jpg/ru-0-r-244,244-n-855157XP0f.jpg'],
            ['ESKA Summer City', 'http://gdansk1-3.radio.pionier.net.pl:8000/pl/eska-stream10-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/85515904Zi.jpg/ru-0-r-244,244-n-85515904Zi.jpg'],
            ['ESKA Cinema', 'http://gramy01.eska.fm:8000/eska-stream24-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855142oc41.jpg/ru-0-r-244,244-n-855142oc41.jpg'],
            ['ESKA Club', 'http://warszawa1-1.radio.pionier.net.pl:8000/pl/eska-stream4-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855143wVBR.jpg/ru-0-r-244,244-n-855143wVBR.jpg'],
            ['ESKA Live RMX Puoteck', 'http://gdansk.radio.pionier.net.pl:8000/pl/eska-stream6-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855190Up99.jpg/ru-0-r-244,244-n-855190Up99.jpg'],
            ['ESKA David Guetta', 'http://gramy01.eska.fm:8000/eska-stream27-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/8551474pdI.jpg/ru-0-r-244,244-n-8551474pdI.jpg'],
            ['Radio TekstyFM', 'http://gramy01.eska.fm:8000/eska-stream26-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855160C6o3.jpg/ru-0-r-244,244-n-855160C6o3.jpg'],
            ['Radio MyMusic', 'http://gramy01.eska.fm:8000/eska-stream25-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855155NlaO.jpg/ru-0-r-244,244-n-855155NlaO.jpg'],
            ['Eska ROCK', 'http://gdansk1-1.radio.pionier.net.pl:8000/pl/eskarock.mp3', 'http://thumbs.eska.pl/common/8/3/s/837695b2f8.jpg/ru-0-r-244,244-n-837695b2f8.jpg'],
            ['Eska ROCK Alternative', 'http://poznan5.radio.pionier.net.pl:8000/eska-stream15-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837629XclT.jpg/ru-0-r-244,244-n-837629XclT.jpg'],
            ['Eska ROCK Xtreme', 'http://gdansk1-3.radio.pionier.net.pl:8000/pl/eska-stream1-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837649BdIz.jpg/ru-0-r-244,244-n-837649BdIz.jpg'],
            ['Eska ROCK Polska', 'http://gdansk1-3.radio.pionier.net.pl:8000/pl/eska-stream8-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837630MdqO.jpg/ru-0-r-244,244-n-837630MdqO.jpg'],
            ['Eska ROCK Classic', 'http://poznan5.radio.pionier.net.pl:8000/eska-stream13-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837628EUsa.jpg/ru-0-r-244,244-n-837628EUsa.jpg'],
            ['Eska ROCK W Ciężkim Stanie', 'http://poznan5-2.radio.pionier.net.pl:8000/eska-stream18-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837631elTP.jpg/ru-0-r-244,244-n-837631elTP.jpg'],
            ['Eska ROCK Ballads', 'http://gramy01.eska.fm:8000/eska-stream30-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837627kmOn.jpg/ru-0-r-244,244-n-837627kmOn.jpg'],
            ['Eska ROCK Zwolnienie z WF', 'http://gramy01.eska.fm:8000/eska-stream32-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837625rkkj.jpg/ru-0-r-244,244-n-837625rkkj.jpg'],
            ['Eska ROCK Reggae', 'http://gramy01.eska.fm:8000/eska-stream21-1.mp3', 'http://thumbs.eska.pl/common/8/3/s/837632BYSQ.jpg/ru-0-r-244,244-n-837632BYSQ.jpg'],
            ['ESKA Club', 'http://poznan5-2.radio.pionier.net.pl:8000/eska-stream4-1.mp3', 'http://thumbs.eska.pl/common/8/5/s/855143wVBR.jpg/ru-0-r-244,244-n-855143wVBR.jpg'],
            ['ESKA Bełchatów', 'http://gramy01.eska.fm:8000/eska_belchatow.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/POL_Be%C5%82chat%C3%B3w_1_COA.svg/256px-POL_Be%C5%82chat%C3%B3w_1_COA.svg.png'],
            ['ESKA Beskidy', 'http://gramy01.eska.fm:8000/eska_beskidy.mp3', ''],
            ['ESKA Białystok', 'http://gramy01.eska.fm:8000/eska_bialystok.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/POL_Białystok_formal_COA.svg/256px-POL_Białystok_formal_COA.svg.png'],
            ['ESKA Bydgoszcz', 'http://gramy01.eska.fm:8000/eska_bydgoszcz.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/POL_Bydgoszcz_COA.svg/256px-POL_Bydgoszcz_COA.svg.png'],
            ['ESKA Elbląg', 'http://gramy01.eska.fm:8000/eska_elblag.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Coast_of_arms_elblag.png/256px-Coast_of_arms_elblag.png'],
            ['ESKA Gorzów Wlkp.', 'http://gramy01.eska.fm:8000/eska_gorzow.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/POL_Gorz%C3%B3w_Wielkopolski_COA_1.svg/256px-POL_Gorz%C3%B3w_Wielkopolski_COA_1.svg.png'],
            ['ESKA Grudziądz', 'http://gramy01.eska.fm:8000/eska_grudziadz.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/1/18/POL_Grudzi%C4%85dz_COA.svg/256px-POL_Grudzi%C4%85dz_COA.svg.png'],
            ['ESKA Iława', 'http://gramy01.eska.fm:8000/eska_ilawa.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/POL_I%C5%82awa_COA.svg/256px-POL_I%C5%82awa_COA.svg.png'],
            ['ESKA Kielce', 'http://gramy01.eska.fm:8000/eska_kielce.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Herb_miasta_Kielce.svg/256px-Herb_miasta_Kielce.svg.png'],
            ['ESKA Koszalin', 'http://gramy01.eska.fm:8000/eska_koszalin.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/POL_Koszalin_COA.svg/256px-POL_Koszalin_COA.svg.png'],
            ['ESKA Kraków', 'http://gramy01.eska.fm:8000/eska_krakow.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/4/41/POL_Krak%C3%B3w_COA.svg/256px-POL_Krak%C3%B3w_COA.svg.png'],
            ['ESKA Leszno', 'http://gramy01.eska.fm:8000/eska_leszno.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/d/de/POL_Leszno_COA.svg/256px-POL_Leszno_COA.svg.png'],
            ['ESKA Lublin', 'http://gramy01.eska.fm:8000/eska_lublin.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/POL_Lublin_COA_1.svg/256px-POL_Lublin_COA_1.svg.png'],
            ['ESKA Łódź', 'http://poznan5-2.radio.pionier.net.pl:8000/eska-lodz.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/POL_%C5%81%C3%B3d%C5%BA_COA.svg/256px-POL_%C5%81%C3%B3d%C5%BA_COA.svg.png'],
            ['ESKA Małopolska', 'http://gramy01.eska.fm:8000/eska_malopolska.mp3', ''],
            ['ESKA Olsztyn', 'http://gramy01.eska.fm:8000/eska_olsztyn.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/9/92/POL_Olsztyn_COA.svg/256px-POL_Olsztyn_COA.svg.png'],
            ['ESKA Opole', 'http://gramy01.eska.fm:8000/eska_opole.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/POL_Opole_COA.svg/256px-POL_Opole_COA.svg.png'],
            ['ESKA Kalisz/Ostrów', 'http://gramy01.eska.fm:8000/eska_ostrow.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/POL_Ostr%C3%B3w_Wielkopolski_COA.svg/256px-POL_Ostr%C3%B3w_Wielkopolski_COA.svg.png'],
            ['ESKA Piła', 'http://gramy01.eska.fm:8000/eska_pila.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/POL_Pi%C5%82a_COA_1.svg/256px-POL_Pi%C5%82a_COA_1.svg.png'],
            ['ESKA Płock', 'http://gramy01.eska.fm:8000/eska_plock.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/POL_P%C5%82ock_COA.svg/256px-POL_P%C5%82ock_COA.svg.png'],
            ['ESKA Poznań', 'http://poznan5.radio.pionier.net.pl:8000/pl/eska-poznan.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/POL_Pozna%C5%84_COA.svg/256px-POL_Pozna%C5%84_COA.svg.png'],
            ['ESKA Przemyśl', 'http://gramy01.eska.fm:8000/eska_przemysl.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/4/47/POL_Przemy%C5%9Bl_COA.svg/256px-POL_Przemy%C5%9Bl_COA.svg.png'],
            ['ESKA Radom', 'http://gramy01.eska.fm:8000/eska_radom.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/POL_Radom_COA.svg/256px-POL_Radom_COA.svg.png'],
            ['ESKA Rzeszów', 'http://gramy01.eska.fm:8000/eska_rzeszow.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/POL_Rzesz%C3%B3w_COA.svg/256px-POL_Rzesz%C3%B3w_COA.svg.png'],
            ['ESKA Siedlce', 'http://gramy01.eska.fm:8000/eska_siedlce.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Herb_Siedlce.svg/256px-Herb_Siedlce.svg.png'],
            ['ESKA Starachowice', 'http://gramy01.eska.fm:8000/eska_starachowice.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Starachowice_herb.svg/256px-Starachowice_herb.svg.png'],
            ['ESKA Szczecin', 'http://lodz.radio.pionier.net.pl:8000/pl/eska-szczecin.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/POL_Szczecin_COA.svg/256px-POL_Szczecin_COA.svg.png'],
            ['ESKA Szczecinek', 'http://gramy01.eska.fm:8000/eska_szczecinek.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/6/62/POL_Szczecinek_COA.svg/256px-POL_Szczecinek_COA.svg.png'],
            ['ESKA Śląsk', 'http://lodz.radio.pionier.net.pl:8000/pl/eska-slask.mp3', ''],
            ['ESKA Tarnów', 'http://gramy01.eska.fm:8000/eska_tarnow.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/2/29/POL_Tarn%C3%B3w_COA.svg/256px-POL_Tarn%C3%B3w_COA.svg.png'],
            ['ESKA Toruń', 'http://gramy01.eska.fm:8000/eska_torun.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/5/52/POL_Toru%C5%84_COA.svg/256px-POL_Toru%C5%84_COA.svg.png'],
            ['ESKA Trójmiasto', 'http://lodz.radio.pionier.net.pl:8000/pl/eska-trojmiasto.mp3', ''],
            ['ESKA Warszawa', 'http://lodz.radio.pionier.net.pl:8000/pl/eska-warszawa.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/POL_Warszawa_COA.svg/256px-POL_Warszawa_COA.svg.png'],
            ['ESKA Wrocław', 'http://lodz.radio.pionier.net.pl:8000/pl/eska-wroclaw.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Herb_wroclaw.svg/256px-Herb_wroclaw.svg.png'],
            ['ESKA Zamość', 'http://gramy01.eska.fm:8000/eska_zamosc.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/a/af/POL_Zamo%C5%9B%C4%87_COA.svg/256px-POL_Zamo%C5%9B%C4%87_COA.svg.png'],
            ['ESKA Zielona Góra', 'http://gramy01.eska.fm:8000/eska_zielona_gora.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/2/21/POL_Zielona_G%C3%B3ra_COA.svg/256px-POL_Zielona_G%C3%B3ra_COA.svg.png'],
            ['ESKA Żary', 'http://gramy01.eska.fm:8000/eska_zary.mp3', 'http://upload.wikimedia.org/wikipedia/commons/thumb/5/56/POL_%C5%BBary_COA.svg/256px-POL_%C5%BBary_COA.svg.png']
            ]

        if self.opt2 == '':
            i = 0
            for key in list:
                listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?eska_' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            Title = list[int(self.opt2)][0]
            Icon = list[int(self.opt2)][2]
            URL = list[int(self.opt2)][1]
        
            import radioPlayer as player
            player.Main().start(Title, Icon, URL)
            