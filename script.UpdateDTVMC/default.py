import os
import os.path
import urllib
import zipfile
import xbmc
import xbmcgui

getFile = urllib.URLopener()
extractionDirectory = "/storage/.kodi/addons/"
titleString = "DesiTV Media Center"

## Einthusan Addon Installation
fileNameEinthusan = "/storage/.kodi/addons/plugin.video.einthusan"
sourcePathFileEinthusan = "http://desitvmc.com/packages/plugin.video.einthusan-1.3.3.zip"
targetPathFileEinthusan = "/tmp/plugin.video.einthusan-1.3.3.zip"

if os.path.exists(fileNameEinthusan):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'Einthusan Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading Einthusan')
    getFile.retrieve(sourcePathFileEinthusan, targetPathFileEinthusan)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileEinthusan, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed Einthusan.')
    print "Successfully unzipped file to target directory."

## ZEM TV Addon Installation
fileNameZemTV = "/storage/.kodi/addons/plugin.video.ZemTV-shani"
sourcePathFileZemTV = "http://desitvmc.com/packages/plugin.video.ZemTV-shani-5.0.0.zip"
targetPathFileZemTV = "/tmp/plugin.video.ZemTV-shani-5.0.0.zip"

if os.path.exists(fileNameZemTV):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'ZemTV Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading ZemTV')
    getFile.retrieve(sourcePathFileZemTV, targetPathFileZemTV)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileZemTV, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed ZemTV.')
    print "Successfully unzipped file to target directory."


## Shani Repository Installation
fileNameShaniRepository = "/storage/.kodi/addons/repository.shani"
sourcePathFileShaniRepository = "http://desitvmc.com/packages/repository.shani-2.9.zip"
targetPathFileShaniRepository = "/tmp/repository.shani-2.9.zip"


if os.path.exists(fileNameShaniRepository):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'Shani Repository Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading Shani Repository')
    getFile.retrieve(sourcePathFileShaniRepository, targetPathFileShaniRepository)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileShaniRepository, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed Shani Repository.')
    print "Successfully unzipped file to target directory."


## F4MTester Installation
fileNameF4MTester = "/storage/.kodi/addons/plugin.video.f4mTester"
sourcePathFileF4MTester = "http://desitvmc.com/packages/plugin.video.f4mTester-2.6.6.zip"
targetPathFileF4MTester = "/tmp/plugin.video.f4mTester-2.6.6.zip"


if os.path.exists(fileNameF4MTester):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'F4MTester Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading F4MTester')
    getFile.retrieve(sourcePathFileF4MTester, targetPathFileF4MTester)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileF4MTester, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed F4MTester.')
    print "Successfully unzipped file to target directory."

