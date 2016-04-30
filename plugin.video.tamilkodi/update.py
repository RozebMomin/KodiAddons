import os
import sys
import xbmcaddon
import urllib
import urllib2
import urlparse
import xbmcplugin, xbmcgui, xbmc, re

programPath     = xbmcaddon.Addon().getAddonInfo('path')
my_addon        = xbmcaddon.Addon('plugin.video.tamilkodi')
addon_dir       = my_addon.getAddonInfo('path')
localNoticeFile = programPath + '/notice.txt'
changeLog       = addon_dir + '/changelog.txt'

icon = xbmcaddon.Addon().getAddonInfo('icon')

defaultFile     = 'http://cyberrule.com/tv/tamilkodi/default.py'
noticeFile      = 'http://cyberrule.com/tv/tamilkodi/get.php?version'



#-------------------------------------------------------------------------------
def GetVersion():
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request(defaultFile)
    r = opener.open(req)
    the_page = r.read()

    regex = '__version__ = "(.*?)"'
    ver = re.compile(regex).findall(the_page)[0]
    print 'version = ', ver

    return float(ver)

#-------------------------------------------------------------------------------
def getNotification():
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request(noticeFile)
    r = opener.open(req)
    the_page = r.read()

    regex = '__notice__ = "(.*?)"'
    ver = re.compile(regex).findall(the_page)[0]
    print 'notice version = ', ver

    return float(ver)

def getNotice():
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request("http://cyberrule.com/tv/tamilkodi/notice.txt")
    r = opener.open(req)
    the_page = r.read()
    return the_page

def getLocalNotification():
    if os.path.isfile(localNoticeFile):
        with open(localNoticeFile, 'r') as f:
            the_page = f.read()
            regex = '__notice__ = "(.*?)"'
            ver = re.compile(regex).findall(the_page)[0]
            print 'local notice ver', ver
            return float(ver)
    else:
        print 'get local notice error'
        copyFile(localNoticeFile, getNotice())
    return 0

def copyFile(localFile, webFile):
    with open(os.path.abspath(localFile), 'w') as f:
        f.write(str(webFile))
    print 'file copied'

#-------------------------------------------------------------------------------
def TextBoxes(heading,anounce):
    class TextBox():
        # constants
        WINDOW = 10147 #10602 for PVR Timer info | window ID
        CONTROL_LABEL = 1
        CONTROL_TEXTBOX = 5

        def __init__( self, *args, **kwargs):
            # activate the text viewer window
            xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
            # get window
            self.win = xbmcgui.Window( self.WINDOW )
            # give window time to initialize
            xbmc.sleep( 500 )
            self.setControls()

        def setControls( self ):
            # set heading
            self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
            try:
                f = open(anounce)
                text = f.read()
            except: text=anounce
            self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
            return
    TextBox()

#-------------------------------------------------------------------------------
def getChangeLog():
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request("http://cyberrule.com/tv/tamilkodi/changelog.txt")
    r = opener.open(req)
    the_page = r.read()
    return the_page
#-------------------------------------------------------------------------------    
def downloadPythonFile(programPath, pyfile):
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)    
    urlStr = "http://cyberrule.com/tv/tamilkodi/" + pyfile
    req = urllib2.Request(urlStr)
    r = opener.open(req)
    the_page = r.read()

    with open(os.path.abspath(programPath + "/" + pyfile), 'w') as f:
        f.write(the_page)

#-------------------------------------------------------------------------------    
def CheckForUpdates():

    #xbmc.executebuiltin('XBMC.RunScript('++',Env)')
    webNotice = getNotification()
    if (webNotice > getLocalNotification()):
        noticetxt = getNotice()
        TextBoxes("[B][COLOR green]Tamil KODI Notice[/B][/COLOR]", noticetxt)
        copyFile(localNoticeFile, noticetxt)

    try:
        data = GetVersion()
        import default
        if (default.getVersion() < data):
            #dialog = xbmcgui.Dialog()
            #dialog.ok(" Updates available ", " New version is available for download \n "
                                             #"will be automatically downloaded in a moment")


            downloadPythonFile(programPath, 'default.py')
            downloadPythonFile(programPath, 'update.py')
            downloadPythonFile(programPath, 'changelog.txt')
            xbmc.executebuiltin("XBMC.Notification(TamilKodi Update,Successful,5000,"+icon+")")
            xbmc.executebuiltin("XBMC.Container.Refresh")

            #TextBoxes("[B][COLOR red]Tamil KODI Changelog[/B][/COLOR]",xbmc.translatePath(changeLog))
            return 1
    except:
        return 1

    return 1

#------------------------------------------------------------------------------- 