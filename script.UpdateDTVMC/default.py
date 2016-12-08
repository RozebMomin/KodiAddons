import os
import os.path
import urllib
import zipfile
import xbmc
import xbmcgui


fileNameOne = "/storage/.kodi/addons/repository.shani"

getFile = urllib.URLopener()
sourcePathFileOne = "http://askmaulana.com/streams/repository.shani-2.9.zip"
targetPathFileOne = "/tmp/repository.shani-2.9.zip"
extractionDirectory = "/storage/.kodi/addons/"

if os.path.exists(fileNameOne):
    print "Path already exists."
    xbmcgui.Dialog().notification('DesiTV Media Center', 'Shani Repository Already Exists!')
else:
    xbmcgui.Dialog().notification('DesiTV Media Center', 'Downloading Shani Repository')
    getFile.retrieve(sourcePathFileOne, targetPathFileOne)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileOne, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    xbmcgui.Dialog().notification('DesiTV Media Center', 'Successfully Installed Shani Repository.')
    print "Successfully unzipped file to target directory."