# -*- coding: utf-8 -*-
import urllib2, re, sys
import xbmcaddon, xbmcplugin, xbmcgui

class Premieres:

    # definicja zmiennych globalnych
    def __init__(self):
        __settings__ = xbmcaddon.Addon("plugin.video.filmweb.pl.premiery")
        self.autoPlay = __settings__.getSetting("autoPlay")
        self.URL = 'http://www.filmweb.pl'
        self.COOKIE = 'welcomeScreen=welcome_screen'
        self.MOVIES = []
        self.chars = {
        "&oacute;": "ó",
        "&quot;": "\""
        }
        
    def getTrailers(self):
        #xbmcgui.Dialog().ok('d', self.autoPlay)
        
        # połączenie z adresem URL, ustawienie ciasteczek, pobranie zawartości strony z premierami
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', self.COOKIE))
        pagePremieres = opener.open(self.URL + "/premiere").read()
        
        # pobranie linków do poszczególnych filmów
        matchesPremiereMovie = list(set(re.compile('(div class="filmPreview.*?id=filmId>)').findall(pagePremieres)))
        
        # pobranie zawartości strony z trailerami
        for pageMovie in matchesPremiereMovie:

            # Tytuł
            matchesTitle = re.compile('class="filmTitle[^>]+>([^<]+)<').findall(pageMovie)
            if len(matchesTitle) == 0:
                self.movieTitle = ''
            else:
                self.movieTitle = matchesTitle[0]

            # Tytuł oryginalny
            matchesOriginalTitle = re.compile('class=filmSubtitle> ([^<]+) <').findall(pageMovie)
            if len(matchesOriginalTitle) == 0:
                self.movieOriginalTitle = ''
            else:
                self.movieOriginalTitle = matchesOriginalTitle[0]
            
            # Okładka
            matchesPoster = re.compile('img src="([^"]+).2.jpg"').findall(pageMovie)
            if len(matchesPoster) == 0:
                self.moviePoster = 'DefaultVideo.png'
            else:
                self.moviePoster = matchesPoster[0] + ".3.jpg"
            
            # Rok
            matchesMovieYear = re.compile('titleYear>\(([0-9]+)\)').findall(pageMovie)
            if len(matchesMovieYear) == 0:
                self.movieYear = ''
            else:
                self.movieYear = matchesMovieYear[0]
            
            # Rating
            matchesMovieRating = re.compile('([0-9]),([0-9])/10').findall(pageMovie)
            if len(matchesMovieRating) == 0:
                self.movieRating = ''
            else:
                self.movieRating = matchesMovieRating[0][0] + "." + matchesMovieRating[0][1]
            
            # Votes
            matchesMovieVotes = re.compile(' ([^<]+) głos').findall(pageMovie)
            if len(matchesMovieVotes) == 0:
                self.movieVotes = 0
            else:
                self.movieVotes = matchesMovieVotes[0]
            
            # Plot
            matchesMoviePlot = re.compile('filmPlot><p>([^<]+)<').findall(pageMovie)
            if len(matchesMoviePlot) == 0:
                self.moviePlot = ''
            else:
                self.moviePlot = matchesMoviePlot[0]

            # Director
            matchesMovieDirector = re.compile('reżyser:</dt><dd><[^>]+>([^<]+)<').findall(pageMovie)
            if len(matchesMovieDirector) == 0:
                self.movieDirecotr = ''
            else:
                self.movieDirector = matchesMovieDirector[0]
                
            # Trailer URL
            matchesMovieTrailer = re.compile('href="(/video/trailer/[^"]+)"').findall(pageMovie)
            
            # HTML to UTF-8
            for val in self.chars:
                self.movieTitle = self.movieTitle.replace(val, self.chars[val])
                self.moviePlot = self.moviePlot.replace(val, self.chars[val])
                
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink)

    # pobranie informacji o trailerze
    def parseTrailerPage(self, trailerLink):

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
            listitem.setInfo(type='Video', infoLabels={ "Plot": self.moviePlot})
            listitem.setInfo(type='Video', infoLabels={ "Director": self.movieDirector})
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=trailerVideos[0], listitem=listitem, isFolder=False)
            self.MOVIES.append({"url": trailerVideos[0], "title": self.movieTitle, "item": listitem, "poster": self.moviePoster})
        
    def play(self):
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        # tworzy playlistę
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
       
        for item in self.MOVIES:
            playList.add(item["url"])
        
        # automatyczne odtwarzanie playlisty
        
        if self.autoPlay == 'true':
            xbmc.executebuiltin('playlist.playoffset(video , 0)')

runPremiere = Premieres()
runPremiere.getTrailers()
runPremiere.play()