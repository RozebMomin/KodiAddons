import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

from bs4 import BeautifulSoup
import urllib
import re

addon = xbmcaddon.Addon('plugin.video.MakkahTVLive')

url = "https://www.youtube.com/channel/UClIIopOeuwL8KEK0wnFcodw/live"

page3 = urllib.urlopen(url).read()
soup3 = BeautifulSoup(page3)

desc = soup3.findAll(attrs={"itemprop":"videoId"}) 
liveVideoId = desc[0]['content'].encode('utf-8')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+liveVideoId+')')

# util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)