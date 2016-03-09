import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.MakkahTVLive')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=ArVmnth5jB4)')
#plugin://plugin.video.youtube/?action=play_video&videoid=ArVmnth5jB4)')

#util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
