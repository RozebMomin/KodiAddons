import xbmcaddon, util
import xbmcgui
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.JaffariCenter.en')
addonname = addon.getAddonInfo('name')

errorLine1 = "Jaffari Center of Atlanta is not currently LIVE!"
errorLine2 = "Please try again later."

proc = subprocess.Popen(["curl", "http://xjaffari2x.api.channel.livestream.com/2.0/livestatus.json"], stdout=subprocess.PIPE)
(out, err) = proc.communicate()
parsed_json_data = json.loads(out)
LiveStatus = parsed_json_data["channel"]["isLive"]


if LiveStatus = 'false' :
	xbmcgui.Dialog().ok(addonname, errorLine1, errorLine2)
else:
	proc = subprocess.Popen(["curl", "http://xjaffari2x.api.channel.livestream.com/2.0/info.json"], stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	parsed_json = json.loads(out)
	util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), parsed_json["channel"]["iphoneUrl"])
