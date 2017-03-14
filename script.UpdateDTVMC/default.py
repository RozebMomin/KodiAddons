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

## Aftershock Repo Installation
fileNameAFRepo = "/storage/.kodi/addons/repository.aftershock"
sourcePathFileAFRepo = "http://desitvmc.com/packages/repository.aftershock-2.0.1.zip"
targetPathFileAFRepo = "/tmp/repository.aftershock-2.0.1.zip"


if os.path.exists(fileNameAFRepo):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'AFRepo Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading AFRepo')
    getFile.retrieve(sourcePathFileAFRepo, targetPathFileAFRepo)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileAFRepo, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed AFRepo.')
    print "Successfully unzipped file to target directory."

## Aftershock Artwork Installation
fileNameAFArtwork = "/storage/.kodi/addons/script.aftershock.artwork"
sourcePathFileAFArtwork = "http://desitvmc.com/packages/script.aftershock.artwork-1.1.0.zip"
targetPathFileAFArtwork = "/tmp/script.aftershock.artwork-1.1.0.zip"


if os.path.exists(fileNameAFArtwork):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'AFArtwork Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading AFArtwork')
    getFile.retrieve(sourcePathFileAFArtwork, targetPathFileAFArtwork)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileAFArtwork, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed AFArtwork.')
    print "Successfully unzipped file to target directory."

## Aftershock Guide Installation
fileNameAFGuide = "/storage/.kodi/addons/script.aftershocknow.guide"
sourcePathFileAFGuide = "http://desitvmc.com/packages/script.aftershocknow.guide-1.1.5.zip"
targetPathFileAFGuide = "/tmp/script.aftershocknow.guide-1.1.5.zip"


if os.path.exists(fileNameAFGuide):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'AFGuide Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading AFGuide')
    getFile.retrieve(sourcePathFileAFGuide, targetPathFileAFGuide)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileAFGuide, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed AFGuide.')
    print "Successfully unzipped file to target directory."

## Aftershock Main Addon Installation
fileNameAFMainAddon = "/storage/.kodi/addons/plugin.video.aftershock"
sourcePathFileAFMainAddon = "http://desitvmc.com/packages/plugin.video.aftershock-4.3.5.zip"
targetPathFileAFMainAddon = "/tmp/plugin.video.aftershock-4.3.5.zip"


if os.path.exists(fileNameAFMainAddon):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'AFMainAddon Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading AFMainAddon')
    getFile.retrieve(sourcePathFileAFMainAddon, targetPathFileAFMainAddon)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileAFMainAddon, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed AFMainAddon.')
    print "Successfully unzipped file to target directory."

## SpeedTest Addon Installation
fileNameSpeedTestAddon = "/storage/.kodi/addons/script.speedtestnet"
sourcePathFileSpeedTestAddon = "http://arnuboxota.com/repo/addons/script.speedtestnet/script.speedtestnet-1.0.0.zip"
targetPathFileSpeedTestAddon = "/tmp/script.speedtestnet-1.0.0.zip"


if os.path.exists(fileNameSpeedTestAddon):
    print "Path already exists."
    xbmcgui.Dialog().notification(titleString, 'SpeedTest Already Installed!')
else:
    xbmcgui.Dialog().notification(titleString, 'Downloading SpeedTest')
    getFile.retrieve(sourcePathFileSpeedTestAddon, targetPathFileSpeedTestAddon)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileSpeedTestAddon, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification(titleString, 'Successfully Installed SpeedTest.')
    print "Successfully unzipped file to target directory."

## Successful Update Dialog
xbmc.executebuiltin("UpdateLocalAddons")
xbmc.executebuiltin("UpdateAddonRepos")

if os.path.exists(fileNameEinthusan) and os.path.exists(fileNameZemTV) and os.path.exists(fileNameShaniRepository) and os.path.exists(fileNameF4MTester) and os.path.exists(fileNameSpeedTestAddon):
    xbmcgui.Dialog().ok(titleString, "Congratulations!", "Your DesiTV Media Center has been updated successfully!")

else:
    xbmcgui.Dialog().ok(titleString, "Looks like something went wrong!", "Looks like your DesiTV has not been updated fully!", "Please run this program again!")

# xbmcgui.Dialog().ok(titleString, "Congratulations!", "Your DesiTV Media Center has been updated successfully!")