import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

#proc = subprocess.Popen(["curl", "http://livestream.com/api/accounts/11436227/events/3998452/viewing_info"], stdout=subprocess.PIPE)
#(out, err) = proc.communicate()

#parsed_json = json.loads(out)

addon = xbmcaddon.Addon('plugin.video.WorldIslamicNetwork')

URLStream = "rtsp://live.wmncdn.net/winislam/d042e6f2b8e7e4c40b35b857a0d4102b.sdp"
#http://live.wmncdn.net/winislam/d042e6f2b8e7e4c40b35b857a0d4102b.sdp/playlist.m3u8
#rtsp://live.wmncdn.net/winislam/d042e6f2b8e7e4c40b35b857a0d4102b.sdp

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
