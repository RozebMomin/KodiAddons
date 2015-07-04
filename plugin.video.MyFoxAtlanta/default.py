import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

proc = subprocess.Popen(["curl", "http://livestream.com/api/accounts/4241684/events/2152811/viewing_info"], stdout=subprocess.PIPE)
(out, err) = proc.communicate()

parsed_json = json.loads(out)

addon = xbmcaddon.Addon('plugin.video.MyFoxAtlanta')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), parsed_json["streamInfo"]["rtsp_url"])
