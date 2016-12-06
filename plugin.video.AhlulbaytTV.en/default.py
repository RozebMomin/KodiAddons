import xbmcaddon, util

addon = xbmcaddon.Addon('plugin.video.AhlulbaytTV.en')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 'rtmp://109.123.126.10:1935/live/livestream1.sdp')
