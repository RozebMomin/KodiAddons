import ssl
import sys
import urlparse
import urllib,urllib2,re,xbmcplugin,xbmcgui
import os
import requests
from bs4 import BeautifulSoup
import re
import xbmcaddon, util

# urllib2.disable_warnings()

addon = xbmcaddon.Addon('plugin.video.GujaratiNatak')

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'videos')

#YouTube Gujarati Natak Playlist
requestUrl = "https://www.youtube.com/playlist?list=PL7ueRli5dEU8jUZzyucuYQOllebth1x07"
r = requests.get(requestUrl)
data = r.text
soup = BeautifulSoup(data)

#Define Empty Variables
dataTitles = []
dataLinks = []
dataThumbnails = []
i=0

#Define BeautifulSoup Queries
videoTitle = soup.find_all('a', 'pl-video-title-link')
videoLink = soup.find_all('a', 'pl-video-title-link', href=True)
videoThumbnail = soup.find_all('span', 'yt-thumb-clip')

#Fill Empty Queries
for row in videoTitle:
	Title = row.get_text()
	Title = Title.strip()
	dataTitles.append(Title)
	print Title

for link in videoLink:
	properLink = str()
	properLink = link['href']
	properLink = properLink.replace("/watch?v=", "")
	properLink = properLink.split("&")[0]
	dataLinks.append(properLink)

for image in dataLinks:
	videoImage = "http://i.ytimg.com/vi/" + image + "/default.jpg"
	dataThumbnails.append(videoImage)

#Get Length of Directory
maxResults = len(dataLinks)
print "-----------" + str(maxResults)

url = "plugin://plugin.video.youtube/play/?video_id=-fppIc3tjUg"
li = xbmcgui.ListItem('My First Video!', iconImage='http://i.ytimg.com/vi/-fppIc3tjUg/default.jpg')
li.setProperty('IsPlayable', 'true')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = "plugin://plugin.video.youtube/play/?video_id=kqANd2aw8Mc"
li = xbmcgui.ListItem('My Second Video!', iconImage='DefaultVideo.png')
li.setProperty('IsPlayable', 'true')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)