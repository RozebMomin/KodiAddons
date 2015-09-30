import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.JaffariCenterATL')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=Sje18clUrqw)')

#util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), URLStream)
