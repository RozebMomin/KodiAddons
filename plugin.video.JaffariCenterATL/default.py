# import xbmcaddon, util
# import subprocess
# from subprocess import call
# import json
# import os
# # from bs4 import BeautifulSoup
# # import urllib


# # url = "https://www.youtube.com/user/JaffariCenterATL/live"

# # page3 = urllib.urlopen(url).read()
# # soup3 = BeautifulSoup(page3)

# # desc = soup3.findAll(attrs={"itemprop":"videoId"}) 
# # url2 = desc[0]['content'].encode('utf-8')

# addon = xbmcaddon.Addon('plugin.video.JaffariCenterATL')

# xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=NuDx31eNMyM)')

# #util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)

## ^^ OLD CODE

## VV NEW CODE

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

addon = xbmcaddon.Addon('plugin.video.JaffariCenterATL')

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'videos')

#YouTube Jaffari Center Uploads
requestUrl = "https://www.youtube.com/user/JaffariCenterATL/videos?live_view=500&sort=dd&view=0&flow=list"
r = requests.get(requestUrl)
data = r.text
soup = BeautifulSoup(data)

#YouTube Jaffari Center LIVE Stream
liveGetURL = "https://www.youtube.com/user/JaffariCenterATL/live"

page3 = urllib.urlopen(liveGetURL).read()
soup3 = BeautifulSoup(page3)

desc = soup3.findAll(attrs={"itemprop":"videoId"}) 
liveStreamVideoId = desc[0]['content'].encode('utf-8')

#Define Empty Variables
dataTitles = []
dataLinks = []
dataThumbnails = []
i=0

#Define BeautifulSoup Queries
videoTitle = soup.find_all('h3', 'yt-lockup-title ')
videoLink = soup.find_all('div',{"data-context-item-id":True})
videoThumbnail = soup.find('span', 'yt-thumb-clip')

# Fill Empty Queries
for row in videoTitle:
        Title = row.get_text()
        Title = Title.strip()
        Title = Title.encode('utf-8')
        Title = Title.split("-")[0]
        dataTitles.append(Title)

for link in videoLink:
        properLink = str()
        properLink = link['data-context-item-id']
        dataLinks.append(properLink)

#Get Length of Directory

liveURL = "plugin://plugin.video.youtube/play/?video_id=" + liveStreamVideoId
li2 = xbmcgui.ListItem(' LIVE ', iconImage='http://i.ytimg.com/vi/'+liveStreamVideoId+'/maxresdefault.jpg')
li2.setProperty('IsPlayable', 'true')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=liveURL, listitem=li2)

maxResults = len(dataLinks)
for i in range(0, maxResults):
        url = "plugin://plugin.video.youtube/play/?video_id=" + str(dataLinks[i])
        li = xbmcgui.ListItem(' '+str(dataTitles[i])+' ', iconImage='http://i.ytimg.com/vi/'+str(dataLinks[i])+'/maxresdefault.jpg')
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        i+=1

# print "-----------" + str(maxResults)

xbmcplugin.endOfDirectory(addon_handle)