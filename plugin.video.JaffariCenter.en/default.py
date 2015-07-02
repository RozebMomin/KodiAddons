import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

proc = subprocess.Popen(["curl", "http://xjaffari2x.api.channel.livestream.com/2.0/info.json"], stdout=subprocess.PIPE)
(out, err) = proc.communicate()

parsed_json = json.loads(out)

addon = xbmcaddon.Addon('plugin.video.JaffariCenter.en')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), parsed_json["channel"]["iphoneUrl"])
