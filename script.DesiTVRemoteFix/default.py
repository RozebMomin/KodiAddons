import urllib, os,re,urllib2
import xbmc,xbmcgui
 
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("My Script","Downloading File",url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()
 
url ='http://askmaulana.com/desitvmc.com/license.txt'
DownloaderClass(url,"~/Downloads")