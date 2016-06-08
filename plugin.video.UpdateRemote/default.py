import xbmc
import xbmcgui
import xbmcaddon
 
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
 
tf = '/storage/.kodi/userdata/keymaps/gen.xml'
f2 = open(tf, 'w')
f2.write("""<keymap><global><keyboard><key id="61623">mute</key><key id="61573">volumedown</key><key id="61572">volumeup</key><key id="61661">playpause</key><key id="61628">stop</key><key id="61570">left</key><key id="61571">right</key><key id="61568">up</key><key id="61569">down</key><key id="127185">select</key><key id="61576">activatewindow(home)</key><key id="61448">backspace</key><key id="61488">number0</key><key id="61489">number1</key><key id="61490">number2</key><key id="61491">number3</key><key id="61492">number4</key><key id="61493">number5</key><key id="61494">number6</key><key id="61495">number7</key><key id="61496">number8</key><key id="61497">number9</key><key id="61448">previousmenu</key><key id="61656">contextmenu</key></keyboard></global><fullscreenvideo><keyboard><key id="61572">volumeup</key><key id="61573">volumedown</key><key id="61628">stop</key><key id="61623">mute</key><key id="127185">osd</key></keyboard></fullscreenvideo></keymap>""")
f2.close()

xbmc.executebuiltin('Notification(Complete,Please try your remote to ensure it has been fixed!,10000)')