#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmcaddon,base64

pluginhandle = int(sys.argv[1])
xbox = xbmc.getCondVisibility("System.Platform.xbox")
settings = xbmcaddon.Addon(id='plugin.video.mpora_com')
translation = settings.getLocalizedString

def index():
        addDir(translation(30002),"http://mpora.com/videos",'sortDirection',"")
        addDir(translation(30003),"http://mpora.com/snowboarding/videos",'sortDirection',"")
        addDir(translation(30004),"http://mpora.com/surfing/videos",'sortDirection',"")
        addDir(translation(30005),"http://mpora.com/skateboarding/videos",'sortDirection',"")
        addDir(translation(30006),"http://mpora.com/bmx/videos",'sortDirection',"")
        addDir(translation(30007),"http://mpora.com/bmxracing/videos",'sortDirection',"")
        addDir(translation(30008),"http://mpora.com/mountainbiking/videos",'sortDirection',"")
        addDir(translation(30009),"http://mpora.com/motocross/videos",'sortDirection',"")
        addDir(translation(30010),"http://mpora.com/skiing/videos",'sortDirection',"")
        addDir(translation(30011),"http://mpora.com/wakeboarding/videos",'sortDirection',"")
        addDir(translation(30012),"http://mpora.com/windsurfing/videos",'sortDirection',"")
        addDir(translation(30013),"http://mpora.com/kitesurfing/videos",'sortDirection',"")
        addDir(translation(30014),"http://mpora.com/road-cycling/videos",'sortDirection',"")
        addDir(translation(30015),"http://mpora.com/outdoor/videos",'sortDirection',"")
        addDir(translation(30020),"",'search',"")
        xbmcplugin.endOfDirectory(pluginhandle)

def sortDirection(url):
        urlRecent=url+"/recent"
        urlBrands=url+"/brands"
        urlHD=url+"/hd"
        addDir(translation(30017),urlRecent,'listVideos',"")
        addDir(translation(30016),url,'listVideos',"")
        addDir(translation(30019),urlHD,'listVideos',"")
        addDir(translation(30018),urlBrands,'listVideos',"")
        xbmcplugin.endOfDirectory(pluginhandle)

def listVideos(url):
        content = getUrl(url)
        matchPage=re.compile('<a class="next_page" rel="next" href="(.+?)">', re.DOTALL).findall(content)
        content = content[content.find('<ul class="video-list">'):]
        content = content[:content.find('</ul>')]
        spl=content.split('<li')
        for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile('<h6>(.+?)</h6>', re.DOTALL).findall(entry)
            title=match[0]
            title=cleanTitle(title)
            match=re.compile('href="(.+?)"', re.DOTALL).findall(entry)
            url="http://mpora.com"+match[0]
            match=re.compile('src="(.+?)"', re.DOTALL).findall(entry)
            thumb=match[0].replace("_200x112_","_640x360_").replace("_tn_","_")
            addLink(title,url,'playVideo',thumb)
        if len(matchPage)>0:
          urlNext="http://mpora.com"+matchPage[0]
          addDir(translation(30001),urlNext,'listVideos',"")
        xbmcplugin.endOfDirectory(pluginhandle)

def search():
        keyboard = xbmc.Keyboard('', translation(30020))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
          search_string = keyboard.getText().replace(" ","+")
          listVideos('http://mpora.com/search?q='+search_string+'&submit=search')

def playVideo(url):
        content = getUrl(url)
        match=re.compile('<video controls="controls" height="(.+?)" id="(.+?)" preload="(.+?)" src="(.+?)" width="(.+?)"></video>', re.DOTALL).findall(content)
        url=match[0][3]
        if url.find("_640"):
          req = urllib2.Request(url.replace("_640","_1280"))
          try:
            urllib2.urlopen(req)
            url=url.replace("_640","_1280")
          except:
            pass
        listitem = xbmcgui.ListItem(path=url)
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def cleanTitle(title):
        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","\\").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
        title=title.replace("&Auml;","Ä").replace("&Uuml;","Ü").replace("&Ouml;","Ö").replace("&auml;","ä").replace("&uuml;","ü").replace("&ouml;","ö")
        title=title.strip()
        return title

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/13.0')
        if xbox==True:
          response = urllib2.urlopen(req)
        else:
          response = urllib2.urlopen(req,timeout=30)
        link=response.read()
        response.close()
        return link

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
         
params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode == 'listVideos':
    listVideos(url)
elif mode == 'sortDirection':
    sortDirection(url)
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'search':
    search()
else:
    index()
