import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

#proc = subprocess.Popen(["curl", "http://livestream.com/api/accounts/11436227/events/3998452/viewing_info"], stdout=subprocess.PIPE)
#(out, err) = proc.communicate()

#parsed_json = json.loads(out)

addon = xbmcaddon.Addon('plugin.video.VelayatTV')

URLStream = "http://216.75.232.210:1935/live/mp4:myStream/playlist.m3u8"
# http://216.75.232.210:1935/live/mp4:myStream/playlist.m3u8

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
