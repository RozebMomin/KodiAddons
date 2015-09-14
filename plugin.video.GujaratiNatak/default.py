# import urllib,urllib2,re,xbmcplugin,xbmcgui
# import os
# import requests
# from bs4 import BeautifulSoup
# import re

# #YouTube Gujarati Natak Playlist
# url = "https://www.youtube.com/playlist?list=PL7ueRli5dEU8jUZzyucuYQOllebth1x07"
# r = requests.get(url)
# data = r.text

# soup = BeautifulSoup(data)

# #Define Empty Variables
# dataTitles = []
# dataLinks = []
# dataThumbnails = []
# i=0

# #Define BeautifulSoup Queries
# videoTitle = soup.find_all("a", {"class","pl-video-title-link"})
# videoLink = soup.find_all("a", {"class","pl-video-title-link"}, href=True)
# videoThumbnail = soup.find_all("span", {"class","yt-thumb-clip"})
#------------------------------------------------------------
# import sys
# import urlparse
# import urllib,urllib2,re,xbmcplugin,xbmcgui
# import os
# import requests
# from bs4 import BeautifulSoup
# import re

# #YouTube Gujarati Natak Playlist
# url = "https://www.youtube.com/playlist?list=PL7ueRli5dEU8jUZzyucuYQOllebth1x07"
# r = requests.get(url)
# data = r.text

# soup = BeautifulSoup(data)

# #Define Empty Variables
# dataTitles = []
# dataLinks = []
# dataThumbnails = []
# i=0

# #Define BeautifulSoup Queries
# # videoTitle = soup.findAll("a",{"class","pl-video-title-link"})
# # videoLink = soup.find_all("a",{"class","pl-video-title-link"},href=True)
# # videoThumbnail = soup.find_all("span",{"class","yt-thumb-clip"})


#########################################
import xbmcaddon, util
import sys
import xbmcgui
import xbmcplugin

addon = xbmcaddon.Addon('plugin.video.GujaratiNatak')

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

#url = 'https://www.youtube.com/watch?v=-fppIc3tjUg'
url = "plugin://plugin.video.youtube/play/?video_id=-fppIc3tjUg"
li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

url = "plugin://plugin.video.youtube/play/?video_id=kqANd2aw8Mc"
li = xbmcgui.ListItem('My Second Video!', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)