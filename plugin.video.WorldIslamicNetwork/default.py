import xbmcaddon, util

addon = xbmcaddon.Addon('plugin.video.WorldIslamicNetwork')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 'rtsp://live.wmncdn.net/winislam/d042e6f2b8e7e4c40b35b857a0d4102b.sdp')
