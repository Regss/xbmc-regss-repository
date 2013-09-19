# -*- coding: utf-8 -*-
import urllib2
import re
import sys
import xbmcaddon
import xbmcplugin
import xbmcgui
import HTMLParser

class Premieres:

    def __init__(self):
        __settings__ = xbmcaddon.Addon("plugin.video.filmweb.pl.premiery")
        self.settingsAutoPlay = __settings__.getSetting("autoPlay")
        self.URL = 'http://www.filmweb.pl'
        self.COOKIE = 'welcomeScreen=welcome_screen'
        self.MOVIES = []
        self.parseHtml = HTMLParser.HTMLParser()

    # TRAILERS KINO
    def getTrailersK(self):
        
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
                # konwertuje znaki HTML do UTF-8
                self.movieTitle = self.parseHtml.unescape(unicode(matchesTitle[0],'utf-8'))

            # Tytuł oryginalny
            matchesOriginalTitle = re.compile('class=filmSubtitle> ([^<]+) <').findall(pageMovie)
            if len(matchesOriginalTitle) == 0:
                self.movieOriginalTitle = ''
            else:
                self.movieOriginalTitle = self.parseHtml.unescape(unicode(matchesOriginalTitle[0],'utf-8'))
            
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
                self.moviePlot = self.parseHtml.unescape(unicode(matchesMoviePlot[0],'utf-8'))

            # Director
            matchesMovieDirector = re.compile('reżyser:</dt><dd><[^>]+>([^<]+)<').findall(pageMovie)
            if len(matchesMovieDirector) == 0:
                self.movieDirector = ''
            else:
                self.movieDirector = matchesMovieDirector[0]
                
            # Trailer URL
            matchesMovieTrailer = re.compile('href="(/video/trailer/[^"]+)"').findall(pageMovie)
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink)

    # TRAILERS DVD
    def getTrailersD(self):
    
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
                # konwertuje znaki HTML do UTF-8
                self.movieTitle = self.parseHtml.unescape(unicode(matchesTitle[0],'utf-8'))
                
            # Tytuł oryginalny
            matchesOriginalTitle = re.compile('<h2 class="text-large[^>]+>([^<]+)<').findall(pageMovie)
            if len(matchesOriginalTitle) == 0:
                self.movieOriginalTitle = ''
            else:
                self.movieOriginalTitle = self.parseHtml.unescape(unicode(matchesOriginalTitle[0],'utf-8'))
            
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
            
            # Plot
            self.moviePlot = ''

            # Director
            self.movieDirector = ''
            
            # Trailer URL
            matchesMovieTrailer = re.compile('filmSubpageContent.*?href="(/video/trailer/[^"]+)".*?filmSubpageMenu').findall(pageMovie)
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink)
            

    # PARSE TRAILER LINK
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
    
    # PLAYLIST
    def playList(self):
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        # utworzenie Playlisty
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        for playListItem in self.MOVIES:
            playList.add(playListItem["url"], playListItem["item"])
        xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")
        
        # autoodtwarzanie playlisty
        if self.settingsAutoPlay == 'true':
            xbmc.Player().play(playList)
    
    # MENU
    def menu(self):
        listItemKino = xbmcgui.ListItem(label="Premiery Kino", iconImage="special://home/addons/plugin.video.filmweb.pl.premiery/img/kino.png")
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?kino", listitem=listItemKino, isFolder=True)
        listItemDVD = xbmcgui.ListItem(label="Premiery DVD", iconImage="special://home/addons/plugin.video.filmweb.pl.premiery/img/dvd.png")
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?dvd", listitem=listItemDVD, isFolder=True)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
run = Premieres()

if sys.argv[2] == '?kino':
    run.getTrailersK()
    run.playList()
elif sys.argv[2] == '?dvd':
    run.getTrailersD()
    run.playList()
else:
    run.menu()
    