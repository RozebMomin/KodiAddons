import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
import requests
from bs4 import BeautifulSoup
import re

addon = xbmcaddon.Addon('plugin.video.AasthaTV')

r = requests.get("http://hellotv.in/livetv/play?classid=2038")

soup = BeautifulSoup(r.content)

need = soup.find_all("script", {'charset':'utf-8'})
TtoWrite = str(need[1])

TtoWrite = TtoWrite.replace("	", "")
TtoWrite = re.search('(delivery.*)', TtoWrite).group()
TtoWrite = TtoWrite.replace("delivery = ", "")
TtoWrite = TtoWrite.replace(";", "")
TtoWrite = TtoWrite.replace("\"", "")

videoSource = TtoWrite

URLStream = videoSource

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
