import xbmcaddon, util

addon = xbmcaddon.Addon('plugin.video.SaudiQuranTV.en')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 'rtsp://livestreaming2.itworkscdn.net/squranlive/squran_360p')
