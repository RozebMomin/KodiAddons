import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
import requests
from bs4 import BeautifulSoup
import re

addon = xbmcaddon.Addon('plugin.video.TV9Gujarat')

# r = requests.get("http://hellotv.in/livetv/play?classid=164217&parentId=1041&name=News")

# soup = BeautifulSoup(r.content)

# need = soup.find_all("script", {'charset':'utf-8'})
# TtoWrite = str(need[1])

# TtoWrite = TtoWrite.replace("	", "")
# TtoWrite = re.search('(delivery.*)', TtoWrite).group()
# TtoWrite = TtoWrite.replace("delivery = ", "")
# TtoWrite = TtoWrite.replace(";", "")
# TtoWrite = TtoWrite.replace("\"", "")
# TtoWrite = TtoWrite.replace("manifest.f4m", "playlist.m3u8")


# videoSource = TtoWrite

# URLStream = videoSource

# URLStream = "rtsp://edge-ind.inapcdn.in:1935/berry/inewsup.stream_aac"

URLStream = "http://d1hya96e2cm7qi.cloudfront.net/Live/_definst_/amlst:sweetbcha1novD206L240P/chunklist_b700000.m3u8"

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)