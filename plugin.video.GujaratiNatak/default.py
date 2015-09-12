import urllib,urllib2,re,xbmcplugin,xbmcgui
import os
import requests
from bs4 import BeautifulSoup
import re

#YouTube Gujarati Natak Playlist
url = "https://www.youtube.com/playlist?list=PL7ueRli5dEU8jUZzyucuYQOllebth1x07"
r = requests.get(url)
data = r.text

soup = BeautifulSoup(data)

#Define Empty Variables
dataTitles = []
dataLinks = []
dataThumbnails = []
i=0

#Define BeautifulSoup Queries
videoTitle = soup.find_all("a", {"class","pl-video-title-link"})
videoLink = soup.find_all("a", {"class","pl-video-title-link"}, href=True)
videoThumbnail = soup.find_all("span", {"class","yt-thumb-clip"})

def CATEGORIES():
      addDir("ONE","",1,"")
      addDir( "TWO","",1,"")
      addDir( "THREE","",1,"")
      addDir("FOUR","",1,"")

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(unicode(name), iconImage="DefaultFolder.png",thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name })
    ok=xbmcplugin.addDirectory(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('').findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,2,'')

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
 
elif mode==1:
        print ""+url
        INDEX(url)
 
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)