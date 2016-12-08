import os
import os.path
import urllib
import zipfile


fname = "/storage/.kodi/addons/repository.shani"

getFile = urllib.URLopener()
sourcePathFileOne = "http://askmaulana.com/streams/repository.shani-2.9.zip"
targetPathFileOne = "/tmp/repository.shani-2.9.zip"
extractionDirectory = "/storage/.kodi/addons/"

if os.path.exists(fname):
    print "Path already exists."
else:
    print "Path does not exist. Retrieving ZIP file."
    getFile.retrieve(sourcePathFileOne, targetPathFileOne)
    print "Successfully retrieved file."
    print "Unzipping ZIP file to target directory."
    zip_ref = zipfile.ZipFile(targetPathFileOne, 'r')
    zip_ref.extractall(extractionDirectory)
    zip_ref.close()
    print "Successfully unzipped file to target directory."