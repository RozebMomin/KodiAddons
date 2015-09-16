import xbmc
import xbmcaddon
 
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
 
line1 = "Checking for updates..."
time = 50000 #in miliseconds
 
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
xbmc.executebuiltin("UpdateAddonRepos", True)
ActivateWindow(Home)