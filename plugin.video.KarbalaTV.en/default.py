import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

proc = subprocess.Popen(["curl", "http://livestream.com/api/accounts/11436227/events/3998452/viewing_info"], stdout=subprocess.PIPE)
(out, err) = proc.communicate()

parsed_json = json.loads(out)

addon = xbmcaddon.Addon('plugin.video.KarbalaTV.en')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), parsed_json["streamInfo"]["rtsp_url"])
