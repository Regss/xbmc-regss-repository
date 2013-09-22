# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import sys
import xbmcaddon
import xbmcplugin
import xbmcgui
import HTMLParser

opt = sys.argv[2]

class Premieres:

    def __init__(self):
        __settings__ = xbmcaddon.Addon("plugin.video.filmweb.pl.premiery")
        self.settingsAutoPlay = __settings__.getSetting("autoPlay")
        self.settingsLogin = __settings__.getSetting("login")
        self.settingsCity = __settings__.getSetting("city")
        self.settingsInfo = __settings__.getSetting("info")
        self.URL = 'http://www.filmweb.pl'
        self.MOVIES = []
        self.parseHtml = HTMLParser.HTMLParser()

    # TRAILERS KINO
    def getTrailersKino(self):
        
        # połączenie z adresem URL, ustawienie ciasteczek, pobranie zawartości strony z premierami
        opener = urllib2.build_opener()
        pagePremieres = opener.open(self.URL + "/premiere").read()
        
        # pobranie linków do poszczególnych filmów
        matchesPremiereMovie = list(set(re.compile('(div class="filmPreview.*?id=filmId>)').findall(pagePremieres)))
        
        # pobranie zawartości strony z trailerami
        for pageMovie in matchesPremiereMovie:

            # Trailer URL
            matchesMovieTrailer = re.compile('href="(/video/trailer/[^"]+)"').findall(pageMovie)
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink)

    # TRAILERS DVD
    def getTrailersDVD(self):
    
        # połączenie z adresem URL, ustawienie ciasteczek, pobranie zawartości strony z premierami
        opener = urllib2.build_opener()
        pagePremieres = opener.open(self.URL + "/dvd/premieres").read()
        
        # pobranie linków do poszczególnych filmów
        matchesPremiereMovie = list(set(re.compile('href="([^"]+)/editions"').findall(pagePremieres)))
        
        # pobranie zawartości strony z trailerami
        for movieLink in matchesPremiereMovie:
            
            pageMovie = opener.open(self.URL + movieLink + "/video").read()
            
            # Trailer URL
            matchesMovieTrailer = re.compile('filmSubpageContent.*?href="(/video/trailer/[^"]+)".*?filmSubpageMenu').findall(pageMovie)
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink)
    
    # TRAILERS WANNA SEE
    def getTrailersSee(self):
    
        # połączenie z adresem URL, ustawienie ciasteczek, pobranie zawartości strony z premierami
        opener = urllib2.build_opener()
        pageWannaSee = opener.open(self.URL + "/user/" + self.settingsLogin + "/films/wanna-see").read()
        
        # pobranie linków do poszczególnych filmów
        matchesWannaSeeMovie = list(set(re.compile('overflow[^<]+<a href="([^"]+)"').findall(pageWannaSee)))
        
        # sprawdzenie czy istnieje użytkownik
        if len(matchesWannaSeeMovie) == 0:
            return False

        # pobranie zawartości strony z trailerami
        for movieLink in matchesWannaSeeMovie:
            pageMovie = opener.open(self.URL + movieLink + "/video").read()
            
            # Trailer URL
            matchesMovieTrailer = re.compile('filmSubpageContent.*?href="(/video/trailer/[^"]+)".*?filmSubpageMenu').findall(pageMovie)
            
            # jeśli istnieje trailer pobiera informacje
            if len(matchesMovieTrailer) != 0:
                trailerLink = matchesMovieTrailer[0]
                self.parseTrailerPage(trailerLink)
    
    # TRAILERS LOCATION
    def getTrailersCity(self):
        if opt == '?city':
            listItemKino = xbmcgui.ListItem(label="Poniedziałek")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?poniedzialek", listitem=listItemKino, isFolder=True)
            listItemDVD = xbmcgui.ListItem(label="Wtorek")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?wtorek", listitem=listItemDVD, isFolder=True)
            listItemWannaSee = xbmcgui.ListItem(label="Środa")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?sroda", listitem=listItemWannaSee, isFolder=True)
            listItemCity = xbmcgui.ListItem(label="Czwartek")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?czwartek", listitem=listItemCity, isFolder=True)
            listItemCity = xbmcgui.ListItem(label="Piątek")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?piatek", listitem=listItemCity, isFolder=True)
            listItemCity = xbmcgui.ListItem(label="Sobota")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?sobota", listitem=listItemCity, isFolder=True)
            listItemCity = xbmcgui.ListItem(label="Niedziela")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?niedziela", listitem=listItemCity, isFolder=True)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        else:
            # połączenie z adresem URL, ustawienie ciasteczek, pobranie zawartości strony z premierami
            encodeCity = urllib.quote(self.settingsCity)
            opener = urllib2.build_opener()
            pagePremieres = opener.open(self.URL + "/city/" + encodeCity + "/day/" + opt[1:]).read()
            
            # pobranie linków do poszczególnych filmów
            matchesPremiereMovie = list(set(re.compile('(div class="dropdownTarget.*?trailerLink[^>]+>)').findall(pagePremieres)))
            
            # pobranie zawartości strony z trailerami
            for pageMovie in matchesPremiereMovie:
                
                # Trailer URL
                matchesMovieTrailer = re.compile('trailerLink" href="([^"]+)"').findall(pageMovie)
                
                # jeśli istnieje trailer pobiera informacje
                if len(matchesMovieTrailer) != 0:
                    trailerLink = matchesMovieTrailer[0]
                    self.parseTrailerPage(trailerLink)
    
    # PARSE TRAILER LINK
    def parseTrailerPage(self, trailerLink):

        # połaczenie z adresem, pobranie zawartości strony z trailerem
        opener = urllib2.build_opener()
        trailerPage = opener.open(self.URL + trailerLink).read()
        
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

        # Trailer URL
        trailerVideos = re.compile('source src="([^"]+)"').findall(trailerPage)
        
        # pobranie linku do pliku na YouTube
        youtube = re.compile('param name=movie value="http://www.youtube.com/v/([^"]+)"').findall(trailerPage)
        if len(youtube) != 0:
            youtubeURL = "plugin://plugin.video.youtube/?action=play_video&videoid=" + youtube[0]
            trailerVideos.append(youtubeURL)
        
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
                movieRating = matchesMovieRating[0][0] + "." + matchesMovieRating[0][1]
            
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
        
        
        # sprawdzenie czy plik istnieje, przygotowanie listy odtwarzania
        if len(trailerVideos) == 0:
            return False
        else:
            listitem=xbmcgui.ListItem(label=movieTitle, iconImage=moviePoster, thumbnailImage=moviePoster)
            listitem.setProperty('IsPlayable', 'true')
            listitem.setProperty( "fanart_image", movieFanart )
            listitem.setProperty('IsPlayable', 'true')
            listitem.setInfo(type='Video', infoLabels={ "Title": movieTitle})
            listitem.setInfo(type='Video', infoLabels={ "Originaltitle": movieOriginalTitle})
            listitem.setInfo(type='Video', infoLabels={ "Year": movieYear})
            listitem.setInfo(type='Video', infoLabels={ "Rating": movieRating})
            listitem.setInfo(type='Video', infoLabels={ "Votes": movieVotes})
            listitem.setInfo(type='Video', infoLabels={ "Plot": moviePlot})
            listitem.setInfo(type='Video', infoLabels={ "Director": movieDirector})
            listitem.setInfo(type='Video', infoLabels={ "Credits": movieCredits})
            listitem.setInfo(type='Video', infoLabels={ "Genre": movieGenre})
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
            xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=trailerVideos[0], listitem=listitem, isFolder=False)
            self.MOVIES.append({"url": trailerVideos[0], "title": movieTitle, "item": listitem, "poster": moviePoster})
    
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
        listItemWannaSee = xbmcgui.ListItem(label="Chcę zobaczyć", iconImage="special://home/addons/plugin.video.filmweb.pl.premiery/img/see.png")
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?wannasee", listitem=listItemWannaSee, isFolder=True)
        listItemCity = xbmcgui.ListItem(label="W moim mieście", iconImage="special://home/addons/plugin.video.filmweb.pl.premiery/img/city.png")
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + "?city", listitem=listItemCity, isFolder=True)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
run = Premieres()

if opt == '?kino':
    run.getTrailersKino()
    run.playList()
elif opt == '?dvd':
    run.getTrailersDVD()
    run.playList()
elif opt == '?wannasee':
    run.getTrailersSee()
    run.playList()
elif opt == '?city' or opt == '?poniedzialek' or opt == '?wtorek' or opt == '?sroda' or opt == '?czwartek' or opt == '?piatek' or opt == '?sobota' or opt == '?niedziela':
    run.getTrailersCity()
    run.playList()
else:
    run.menu()
    