# -*- coding: utf-8 -*-

import urllib
import urllib2
import os
import re
import sys
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import HTMLParser
import datetime

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append (__path__)
sys.path.append (__path_img__)

class main:

    def parseTrailer(self, selfGet, trailerLink):
        
        # vars
        self = selfGet
        
        for link in trailerLink:
            
            opener = urllib2.build_opener()
            trailerPage = opener.open(self.URL + link).read()            
            
            # Trailer URL
            matchesTrailerVideos = re.compile('source src="([^"]+)"').findall(trailerPage)
            if len(matchesTrailerVideos) == 0:
                trailerVideos = ''
            else:
                trailerVideos = matchesTrailerVideos[0]
                
            # pobranie linku do pliku na YouTube
            youtube = re.compile('param name=movie value="http://www.youtube.com/v/([^"]+)"').findall(trailerPage)
            if len(youtube) != 0:
                trailerVideos = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + youtube[0]

            if len(trailerVideos) != 0:
                break
                
        # sprawdzenie czy plik istnieje
        if len(trailerVideos) == 0:
            return False
        
        matchesMovieString = re.compile('(<div id=homeCurrentFilmInfo.*?</div>)').findall(trailerPage)
        movieString = matchesMovieString[0]
        
        # Tytuł
        matchesTitle = re.compile('entityTitle>([^<]+)<').findall(movieString)
        if len(matchesTitle) == 0:
            movieTitle = ''
        else:
            # konwertuje znaki HTML do UTF-8
            movieTitle = self.parseHtml.unescape(unicode(matchesTitle[0],'utf-8'))

        # Okładka
        matchesPoster = re.compile('<img src="([^"]+).0.jpg"').findall(movieString)
        if len(matchesPoster) == 0:
            moviePoster = 'DefaultVideo.png'
        else:
            moviePoster = matchesPoster[0] + '.3.jpg'
        
        # Rok
        matchesMovieYear = re.compile('entityTitle>[^<]+\(([0-9]+)\)<').findall(movieString)
        if len(matchesMovieYear) == 0:
            movieYear = ''
        else:
            movieYear = matchesMovieYear[0]

        # pobranie dodatkowych informacji
        if self.settingsInfo == 'true':
            
            matchesMovieInfoURL = re.compile('href="([^"]+)" class=entityTitle').findall(movieString)
            MovieInfoURL = matchesMovieInfoURL[0]
            
            opener = urllib2.build_opener()
            moviePage = opener.open(self.URL + MovieInfoURL).read()
            
            # Tytuł oryginalny
            matchesOriginalTitle = re.compile('h2 class="text-large caption">([^<]+)<').findall(moviePage)
            if len(matchesOriginalTitle) == 0:
                movieOriginalTitle = ''
            else:
                movieOriginalTitle = self.parseHtml.unescape(unicode(matchesOriginalTitle[0],'utf-8'))
                
            # Rating
            matchesMovieRating = re.compile('v:average"> ([0-9]*),([0-9]*)<').findall(moviePage)
            if len(matchesMovieRating) == 0:
                movieRating = ''
            else:
                movieRating = matchesMovieRating[0][0] + '.' + matchesMovieRating[0][1]
            
            # Votes
            matchesMovieVotes = re.compile('v:votes">([^<]+)<').findall(moviePage)
            if len(matchesMovieVotes) == 0:
                movieVotes = 0
            else:
                movieVotes = matchesMovieVotes[0]
            
            # Plot
            matchesMoviePlot = re.compile('v:summary">(.*?)</').findall(moviePage)
            if len(matchesMoviePlot) == 0:
                moviePlot = ''
            else:
                moviePlot = self.parseHtml.unescape(unicode(matchesMoviePlot[0].replace('<span class="fullText hide">', ''),'utf-8'))

            # Director
            matchesMovieDirector = re.compile('v:directedBy">([^<]+)<').findall(moviePage)
            if len(matchesMovieDirector) == 0:
                movieDirector = ''
            else:
                movieDirector = matchesMovieDirector[0]
                
            # Credits
            matchesMovieCredits = re.compile('scenariusz:[^"]+"[^"]+"[^"]+<a[^>]+>([^<]+)<').findall(moviePage)
            if len(matchesMovieCredits) == 0:
                movieCredits = ''
            else:
                movieCredits = matchesMovieCredits[0]
            
            # Genre
            matchesMovieGenre = re.compile('genreIds=[0-9]+">([^<]+)<').findall(moviePage)
            if len(matchesMovieGenre) == 0:
                movieGenre = ''
            else:
                movieGenre = matchesMovieGenre[0]
                
            # Fanart
            matchesMovieFanart = re.compile('filmPhotos"><div class=col><a href="([^"]+)"').findall(moviePage)
            if len(matchesMovieFanart) == 0:
                movieFanart = ''
            else:
                movieFanart = matchesMovieFanart[0]
        
        else:
            movieOriginalTitle = ''
            movieRating = ''
            movieVotes = ''
            moviePlot = ''
            movieDirector = ''
            movieCredits = ''
            movieGenre = ''
            movieFanart = ''
        
        listitem=xbmcgui.ListItem(label=movieTitle, iconImage=moviePoster, thumbnailImage=moviePoster)
        listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty( 'fanart_image', movieFanart )
        listitem.setProperty('IsPlayable', 'true')
        listitem.setInfo(type='Video', infoLabels={ 'Title': movieTitle})
        listitem.setInfo(type='Video', infoLabels={ 'Originaltitle': movieOriginalTitle})
        listitem.setInfo(type='Video', infoLabels={ 'Year': movieYear})
        listitem.setInfo(type='Video', infoLabels={ 'Rating': movieRating})
        listitem.setInfo(type='Video', infoLabels={ 'Votes': movieVotes})
        listitem.setInfo(type='Video', infoLabels={ 'Plot': moviePlot})
        listitem.setInfo(type='Video', infoLabels={ 'Director': movieDirector})
        listitem.setInfo(type='Video', infoLabels={ 'Credits': movieCredits})
        listitem.setInfo(type='Video', infoLabels={ 'Genre': movieGenre})
        xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
        xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=trailerVideos, listitem=listitem, isFolder=False)
        self.MOVIES.append({'url': trailerVideos, 'title': movieTitle, 'item': listitem, 'poster': moviePoster})
        