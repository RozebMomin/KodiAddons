import xbmc
import xbmcgui
import xbmcaddon
 
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

xbmc.executebuiltin("RunAddon(plugin.video.SportsDevil)")