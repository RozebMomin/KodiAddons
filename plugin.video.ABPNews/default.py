import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
import requests
from bs4 import BeautifulSoup
import re

addon = xbmcaddon.Addon('plugin.video.ABPNews')

r = requests.get("https://vuroll.com/livetv/play?classid=1890&parentId=0&name=MOST%20VISITED")

soup = BeautifulSoup(r.content)

need = soup.findAll('script')
TtoWrite = str(need[9])

TtoWrite = TtoWrite.replace("	", "")
TtoWrite = re.search('(delivery.*)', TtoWrite).group()
TtoWrite = TtoWrite.replace("delivery = ", "")
TtoWrite = TtoWrite.replace(";", "")
TtoWrite = TtoWrite.replace("\"", "")
TtoWrite = TtoWrite.replace("manifest.f4m", "playlist.m3u8")


videoSource = TtoWrite

URLStream = videoSource

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
