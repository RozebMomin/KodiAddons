import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
import requests
from bs4 import BeautifulSoup
import re

addon = xbmcaddon.Addon('plugin.video.AasthaTV')

r = requests.get("http://vuroll.com/play/livetv/Aastha-TV_2038")
# http://vuroll.com/play/livetv/Aastha-TV_2038

soup = BeautifulSoup(r.content)

need = soup.find_all("script", {'charset':'utf-8'})
TtoWrite = str(need[1])

TtoWrite = TtoWrite.replace("	", "")
TtoWrite = re.search('(delivery.*)', TtoWrite).group()
TtoWrite = TtoWrite.replace("delivery = ", "")
TtoWrite = TtoWrite.replace(";", "")
TtoWrite = TtoWrite.replace("\"", "")
TtoWrite = TtoWrite.replace("manifest.f4m", "playlist.m3u8")


videoSource = TtoWrite

URLStream = videoSource

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
