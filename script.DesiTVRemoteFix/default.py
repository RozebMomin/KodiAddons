import xbmc

tf = '/storage/.kodi/userdata/keymaps/gen.xml'
f2 = open(tf, 'w')
f2.write("""<keymap><global><keyboard><key id="61654">activatewindow(contextmenu)</key><key
id="61654">contextmenu</key></keyboard></global></keymap>""")
f2.close()

xbmc.executebuiltin('Notification(Complete,Please try your remote to ensure it has been fixed!,10000)')