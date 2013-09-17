# -*- coding: utf-8 -*-
import urllib2, re, sys
import xbmcaddon, xbmcplugin, xbmcgui

class PremieresDVD:

    # definicja zmiennych globalnych
    def __init__(self):
        self.URL = 'http://www.filmweb.pl'
        self.COOKIE = 'welcomeScreen=welcome_screen'
        self.MOVIES = []
    
    def getTrailers(self):
    
        # połączenie z adresem URL, ustawienie ciasteczek, pobranie zawartości strony z premierami
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', self.COOKIE))
        pagePremieres = opener.open(self.URL + "/dvd/premieres").read()
        
        # pobranie linków do poszczególnych filmów
        matchesPremiereMovie = list(set(re.compile('href="([^"]+)/editions"').findall(pagePremieres)))
        
        # pobranie zawartości strony z trailerami
        for movieLink in matchesPremiereMovie:
            
            opener.addheaders.append(('Cookie', self.COOKIE))
            pageMovie = opener.open(self.URL + movieLink + "/video").read()
            
            # Tytuł
            matchesTitle = re.compile('v:name[^>]+>([^<]+)<').findall(pageMovie)
            if len(matchesTitle) == 0:
                self.movieTitle = ''
            else:
                self.movieTitle = matchesTitle[0]
            
            # Tytuł oryginalny
            matchesOriginalTitle = re.compile('<h2 class="text-large[^>]+>([^<]+)<').findall(pageMovie)
            if len(matchesOriginalTitle) == 0:
                self.movieOriginalTitle = ''
            else:
                self.movieOriginalTitle = matchesOriginalTitle[0]
            
            # Okładka
            matchesPoster = re.compile('v:image" href="([^"]+\.jpg)').findall(pageMovie)
            if len(matchesPoster) == 0:
                self.moviePoster = 'DefaultVideo.png'
            else:
                self.moviePoster = matchesPoster[0]
            
            # Rok
            matchesMovieYear = re.compile('id=filmYear[^>]+>\(([0-9]+)\)').findall(pageMovie)
            if len(matchesMovieYear) == 0:
                self.movieYear = ''
            else:
                self.movieYear = matchesMovieYear[0]
            
            # Rating
            matchesMovieRating = re.compile('v:average"> ([0-9]),([0-9])<').findall(pageMovie)
            if len(matchesMovieRating) == 0:
                self.movieRating = ''
            else:
                self.movieRating = matchesMovieRating[0][0] + "." + matchesMovieRating[0][1]
            
            # Votes
            matchesMovieVotes = re.compile('v:votes">([^<]+)<').findall(pageMovie)
            if len(matchesMovieVotes) == 0:
                self.movieVotes = 0
            else:
                self.movieVotes = matchesMovieVotes[0]
            
            # Trailer URL
            matchesMovieTrailer = re.compile('filmSubpageContent.*?href="(/video/trailer/[^"]+)".*?filmSubpageMenu').findall(pageMovie)
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink, movieLink)
                
    # pobranie informacji o trailerze
    def parseTrailerPage(self, trailerLink, movieLink):

        # połaczenie z adresem, pobranie zawartości strony z trailerem
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', self.COOKIE))
        trailerPage = opener.open(self.URL + trailerLink).read()

        # pobranie bezpośredniego URL do pliku wideo
        trailerVideos = re.compile('source src="([^"]+)"').findall(trailerPage)
        
        # pobranie linku do pliku na YouTube
        youtube = re.compile('param name=movie value="http://www.youtube.com/v/([^"]+)"').findall(trailerPage)
        if len(youtube) != 0:
            youtubeURL = "plugin://plugin.video.youtube/?action=play_video&videoid=" + youtube[0]
            trailerVideos.append(youtubeURL)
        
        # sprawdzenie czy plik istnieje, przygotowanie listy odtwarzania
        if len(trailerVideos) == 0:
            return False
        else:
            listitem=xbmcgui.ListItem(label=self.movieTitle, iconImage=self.moviePoster, thumbnailImage=self.moviePoster)
            listitem.setProperty('IsPlayable', 'true')
            listitem.setProperty( "Video", "true" )
            listitem.setInfo(type='Video', infoLabels={ "Title": self.movieTitle})
            listitem.setInfo(type='Video', infoLabels={ "Originaltitle": self.movieOriginalTitle})
            listitem.setInfo(type='Video', infoLabels={ "Year": self.movieYear})
            listitem.setInfo(type='Video', infoLabels={ "Rating": self.movieRating})
            listitem.setInfo(type='Video', infoLabels={ "Votes": self.movieVotes})
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=trailerVideos[0], listitem=listitem, isFolder=False)
            self.MOVIES.append({"url": trailerVideos[0], "title": self.movieTitle, "item": listitem, "poster": self.moviePoster})
        
    def play(self):
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        xbmc.executebuiltin('playlist.playoffset(video , 0)')

runPremiereDVD = PremieresDVD()
runPremiereDVD.getTrailers()
runPremiereDVD.play()