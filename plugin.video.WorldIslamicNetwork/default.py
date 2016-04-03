import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.WorldIslamicNetwork')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=acWnaZnoGkU)')

# URLStream = "rtsp://live.wmncdn.net/winislam/d042e6f2b8e7e4c40b35b857a0d4102b.sdp"
#acWnaZnoGkU

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
