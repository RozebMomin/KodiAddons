# import xbmcaddon, util
# import subprocess
# from subprocess import call
# import json
# import os
# import requests
# from bs4 import BeautifulSoup
# import re

# addon = xbmcaddon.Addon('plugin.video.TV9Gujarat')

# # r = requests.get("http://hellotv.in/livetv/play?classid=164217&parentId=1041&name=News")

# # soup = BeautifulSoup(r.content)

# # need = soup.find_all("script", {'charset':'utf-8'})
# # TtoWrite = str(need[1])

# # TtoWrite = TtoWrite.replace("	", "")
# # TtoWrite = re.search('(delivery.*)', TtoWrite).group()
# # TtoWrite = TtoWrite.replace("delivery = ", "")
# # TtoWrite = TtoWrite.replace(";", "")
# # TtoWrite = TtoWrite.replace("\"", "")
# # TtoWrite = TtoWrite.replace("manifest.f4m", "playlist.m3u8")


# # videoSource = TtoWrite

# # URLStream = videoSource

# # URLStream = "rtsp://edge-ind.inapcdn.in:1935/berry/inewsup.stream_aac"

# liveVideoId = "DNmHwhi21vk"

# xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+liveVideoId+')')

# # URLStream = "http://d1hya96e2cm7qi.cloudfront.net/Live/_definst_/amlst:sweetbcha1novD206L240P/chunklist_b500000.m3u8"

# # util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)

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

addon = xbmcaddon.Addon('plugin.video.TV9Gujarat')

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'videos')

# #YouTube TV9 Gujarat Uploads
# requestUrl = "https://www.youtube.com/user/JaffariCenterATL/videos?live_view=500&sort=dd&view=0&flow=list"
# r = requests.get(requestUrl)
# data = r.text
# soup = BeautifulSoup(data)

#YouTube Jaffari Center LIVE Stream
liveGetURL = "https://www.youtube.com/user/tv9gujaratlive/live"

page3 = urllib.urlopen(liveGetURL).read()
soup3 = BeautifulSoup(page3)

desc = soup3.findAll(attrs={"itemprop":"videoId"}) 
liveStreamVideoId = desc[0]['content'].encode('utf-8')

# #Define Empty Variables
# dataTitles = []
# dataLinks = []
# dataThumbnails = []
# i=0

# #Define BeautifulSoup Queries
# videoTitle = soup.find_all('h3', 'yt-lockup-title ')
# videoLink = soup.find_all('div',{"data-context-item-id":True})
# videoThumbnail = soup.find('span', 'yt-thumb-clip')

# # Fill Empty Queries
# for row in videoTitle:
#         Title = row.get_text()
#         Title = Title.strip()
#         Title = Title.encode('utf-8')
#         Title = Title.split("-")[0]
#         dataTitles.append(Title)

# for link in videoLink:
#         properLink = str()
#         properLink = link['data-context-item-id']
#         dataLinks.append(properLink)

#Get Length of Directory

liveURL = "plugin://plugin.video.youtube/play/?video_id=" + liveStreamVideoId
li2 = xbmcgui.ListItem(' LIVE ', iconImage='http://i.ytimg.com/vi/'+liveStreamVideoId+'/maxresdefault.jpg')
li2.setProperty('IsPlayable', 'true')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=liveURL, listitem=li2)

# maxResults = len(dataLinks)
# for i in range(0, maxResults):
#         url = "plugin://plugin.video.youtube/play/?video_id=" + str(dataLinks[i])
#         li = xbmcgui.ListItem(' '+str(dataTitles[i])+' ', iconImage='http://i.ytimg.com/vi/'+str(dataLinks[i])+'/maxresdefault.jpg')
#         li.setProperty('IsPlayable', 'true')
#         xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
#         i+=1

# print "-----------" + str(maxResults)

xbmcplugin.endOfDirectory(addon_handle)