import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.AajTak')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=92BvhFGRLi4)')
#watch?v=92BvhFGRLi4
#util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
