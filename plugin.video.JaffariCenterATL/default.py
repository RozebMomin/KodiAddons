# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/JaffariCenterATL
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon,util
import xbmcgui
from addon.common.addon import Addon
import subprocess
from subprocess import call
import json

addonID = 'plugin.video.JaffariCenterATL'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID = "JaffariCenterATL"

# Entry point
def run():
    plugintools.log("JaffariCenterATL.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("JaffariCenterATL.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Jaffari Center of Atlanta",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        action="playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 'https://www.youtube.com/watch?v=HOVSbS4boIQ')", 
        title="SomethingElse",
        #url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID+"/",
        thumbnail=icon,
        folder=True )
        #util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 'https://www.youtube.com/watch?v=HOVSbS4boIQ')

run()