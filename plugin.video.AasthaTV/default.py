import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
import requests
from bs4 import BeautifulSoup
import re

addon = xbmcaddon.Addon('plugin.video.AasthaTV')

r = requests.get("http://vuroll.com/AasthaNetwork")
print "Getting Soup"
soup = BeautifulSoup(r.content)

videoSource = soup.find('source')['src']

URLStream = videoSource

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
