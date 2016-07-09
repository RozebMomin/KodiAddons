import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import urlparse
import HTMLParser
import xbmcaddon
from dirCreator import parseList;
from TurlLib import getURL;

import traceback


REMOTE_DBG=False;
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)  


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                
    return param


__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.BanglaTVLive'
selfAddon = xbmcaddon.Addon(id=addon_id)
  
 
mainurl='http://www.jagobd.com'



def Addtypes():
    parseList(getMainMenu());#caching here
    return

def getMainMenu():
    list=[]
    list.append({'name':'Bangla LIVE Channels','url':'http://askmaulana.com/desitvmc.com/packages/banglatv.php','mode':'IC'})
    # list.append({'name':'Islamic Channels','url':mainurl+'/list/bangla.php','mode':'IC'})
    
    # list.append({'name':'Settings','url':'Settings','mode':'Settings'})
    return list;



def ShowSettings(Fromurl):
    selfAddon.openSettings()


def AddChannels(Fromurl,mode):
    parseList(getChannelsEnteries(Fromurl,PageNumber,mode));#caching here
    
def getChannelsEnteries(Fromurl,PageNumber,mode):
    link=getURL(Fromurl).result;
    #print 'getEnteriesList',link
    if mode=='IC':
        match =re.findall('<a.*?href="(.*?)".*?title="(.*?)".*?src="(.*?)"', link)
    else:
        match =re.findall('<li><a href="(.*?)" rel="bookmark" title="(.*?)"><img.*?src="(.*?)"', link)
    listToReturn=[]
    rmode='PlayC';
    #if mode=='ALLC':
    #    rmode='PlayLive'
    listToReturn.append({'name':"Peacetv Bangla",'url':"http://www.peacetvbangla.com/live_peacetv.html",'mode':rmode,'iconimage':"http://www.peacetvbangla.com/images/top-1.jpg",'isFolder':False})
    for cname in match:
        imageurl=cname[2].replace(' ','%20');
        url=cname[0];
        
        if imageurl.startswith('//'): imageurl="http:"+imageurl
        if not imageurl.startswith('http'): imageurl=mainurl+'/'+imageurl
        if not url.startswith('http'): url=mainurl+url
        #print imageurl    
        listToReturn.append({'name':cname[1],'url':url,'mode':rmode,'iconimage':imageurl,'isFolder':False})
    return listToReturn

def getpeacetvbangla ( url ): 
    link=getURL(url, mobile=False).result;
    reg="file=(.*?)&.*streamer=(.*?)&"
    fl,st=re.findall(reg,link)[0]
    return {'url':'%s playpath=%s'%(st,fl)}
    
def getLiveUrl(url):

    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )
    if 'peacetvbangla' in url:
        u=getpeacetvbangla(url)
        progress.close()
        return u
    #print 'fetching url',url
    link=getURL(url, mobile=False).result;
    #print 'link',link
    progress.update( 30, "", "Finding links..", "" )
    h=HTMLParser.HTMLParser()
    match= re.findall('<iframe name="ifram2" src="(.*?)"', link)
    if len(match)==0:
        match= re.findall('<iframe src="(.*?)" name="ifram2"', link)
    print match    
    if len(match)==0:
        progress.update( 60, "", "Finding links..", "" )


        match= re.findall('fid="(.*?)";', link)
        #print link,match
        zzUrl="http://www.zzcast.com/embed.php?u=%s&vw=600&vh=400&domain=www.jagobd.com"%(match[0])
    else:
        print 'getting zurl',match[0]
        zzUrl=h.unescape(match[0])
    print zzUrl,'zzURL'
    if len(zzUrl)==0:
        return None
    #print zzUrl,'zzURL'
    progress.update( 70, "", "Finding links..", "" )
    if zzUrl.startswith("//"):
        zzUrl='http:'+zzUrl
    link=getURL(zzUrl,referer=url, mobile=False).result;
    #print link,zzUrl
    #link=zzUrl
    progress.update( 90, "", "Finding links..", "" )
    print 'final match is',match,link
    progress.update( 100, "", "Finding links..", "" )   
    if 'file:"' in link:
        match=re.findall('file:"(.*?)"', link)
        return {'url':match[0]+'|Referer='+zzUrl}
    else:
        match= re.findall('SWFObject\(\'(.*?)\',.*file\',\'(.*?)\'.*streamer\',\'(.*?)\'', link, re.DOTALL)
    
    
    #match= re.findall('(http.*?playlist.*?)', link)
    #print match
   
    #link=getURL(match[0][0],referer=url, mobile=True).result;
   # match= re.findall('(http.*?playlist.*?)\\s', link, re.DOTALL)


    if len(match)==0:
        return None
    
    return {'rtmp':match[0][2],'playpath':match[0][1],'swf':match[0][0],'pageUrl':zzUrl}
    
    

#flashvars="src=(.*?)\.f


def PlayLiveLink ( url,name ): 
    urlDic=getLiveUrl(url)
  
    if not urlDic==None:
        line1="Url found, Preparing to play";
        time=2000
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

        if 'url' not in urlDic:
            rtmp=urlDic["rtmp"]
            playPath=urlDic["playpath"]
            swf=urlDic["swf"]
            pageurl=urlDic["pageUrl"]
            playfile= "%s playpath=%s swfUrl=%s token=%s live=1 timeout=15 swfVfy=1 flashVer=WIN\\2015,0,0,167 pageUrl=%s"%(rtmp,playPath,swf,'%pwrter(nKa@#.',pageurl)
    #        playfile= "%s playpath=%s swfUrl=%s live=1 timeout=15 swfVfy=1 flashVer=WIN\\2015,0,0,167 pageUrl=%s"%(rtmp,playPath,swf,pageurl)
        else:
            playfile=urlDic["url"]
        print 'playfile', playfile
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        print "playing stream name: " + str(name) 
        xbmc.Player(  ).play( playfile, listitem)
    else:
          line1="Stream not found";
          time=2000
          xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

    return

VIEW_MODES = {
    'thumbnail': {
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
    },
}

def get_view_mode_id( view_mode):
    view_mode_ids = VIEW_MODES.get(view_mode.lower())
    if view_mode_ids:
        return view_mode_ids.get(xbmc.getSkinDir())
    return None

params=get_params()
url=None
name=None
mode=None
linkType=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=urllib.unquote_plus(params["mode"])
except:
    pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
    linkType=args.get('linkType', '')[0]
except:
    pass


PageNumber=''
try:
    PageNumber=args.get('limitstart', '')[0]
except:
    PageNumber=''

if PageNumber==None: PageNumber=""


print     mode,url,name


try:

    if mode==None or url==None or len(url)<1:
        print "InAddTypes"
        Addtypes()

    elif mode=='BC' or mode=='IC':
        print "AddChannels url is ",name,url
        AddChannels(url,mode) #adds series as well as main VOD section, both are cat.

    elif mode=='PlayC' :
        PlayLiveLink(url,name)
    elif mode=='Settings':
        print "Play url is "+url,mode
        ShowSettings(url)
except:
    print 'something wrong', sys.exc_info()[0]
    traceback.print_exc()

if (not mode==None) and mode>1:
    view_mode_id = get_view_mode_id('thumbnail')
    if view_mode_id is not None:
        #print 'view_mode_id',view_mode_id
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        #print 'Container.SetViewMode(%d)' % view_mode_id
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
   
if not (mode=='PlayC'): 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

