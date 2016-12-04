import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
# from bs4 import BeautifulSoup
# import urllib


# url = "https://www.youtube.com/user/JaffariCenterATL/live"

# page3 = urllib.urlopen(url).read()
# soup3 = BeautifulSoup(page3)

# desc = soup3.findAll(attrs={"itemprop":"videoId"}) 
# url2 = desc[0]['content'].encode('utf-8')

addon = xbmcaddon.Addon('plugin.video.JaffariCenterATL')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=NuDx31eNMyM)')

#util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)


