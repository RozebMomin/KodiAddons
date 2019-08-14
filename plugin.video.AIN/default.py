import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2,urllib,cgi, re
import HTMLParser
import traceback,cookielib
import base64, os
from datetime import date

langSelectMode=1
listingMode=2
playingMode=3
overridemode=None  
try:
    from lxmlERRRORRRR import etree
    print("running with lxml.etree")
except ImportError:
    try:
        import xml.etree.ElementTree as etree
        print("running with ElementTree on Python 2.5+")
    except ImportError:
        try:
        # normal cElementTree install
            import cElementTree as etree
            print("running with cElementTree")
        except ImportError:
            try:
            # normal ElementTree install
                import elementtree.ElementTree as etree
                print("running with ElementTree")
            except ImportError:
                print("Failed to import ElementTree from any known place")
          
try:
    import json
except:
    import simplejson as json
    
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id        = 'plugin.video.AIN'
selfAddon       = xbmcaddon.Addon(id=addon_id)
profile_path    =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonPath       = xbmcaddon.Addon().getAddonInfo("path")
addonversion    = xbmcaddon.Addon().getAddonInfo("version")
home            = xbmc.translatePath(selfAddon.getAddonInfo('path').decode('utf-8'))
DONOTCACHE      = selfAddon.getSetting( "donotcache" ) =="true"

if not selfAddon.getSetting( "dummy" )=="true":
    selfAddon.setSetting( "dummy" ,"true")

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

def addDir(name, url, mode, iconimage, isfolder):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
    return ok


def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):
    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;

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

def ChooseLanguage():
    addDir ('Hindi Movies',    'emovies:{"lang":"hindi","type":"main"}',     langSelectMode, os.path.join(home,'icons', 'hindi.png'), True)
    addDir ('Tamil Movies',    'emovies:{"lang":"tamil","type":"main"}',     langSelectMode, os.path.join(home,'icons', 'tamil.png'), True)
    addDir ('Telugu Movies',   'emovies:{"lang":"telugu","type":"main"}',    langSelectMode, os.path.join(home,'icons', 'telugu.png'), True)
    addDir ('Malayalam Movie', 'emovies:{"lang":"malayalam","type":"main"}', langSelectMode, os.path.join(home,'icons', 'malayalam.png'), True)
    addDir ('Kannada Movies',  'emovies:{"lang":"kannada","type":"main"}',   langSelectMode, os.path.join(home,'icons', 'kannada.png'), True)
    addDir ('Bengali Movies',  'emovies:{"lang":"bengali","type":"main"}',   langSelectMode, os.path.join(home,'icons', 'bengali.png'), True)
    addDir ('Marathi Movies',  'emovies:{"lang":"marathi","type":"main"}',   langSelectMode, os.path.join(home,'icons', 'marathi.png'), True)
    addDir ('Punjabi Movies',  'emovies:{"lang":"punjabi","type":"main"}',   langSelectMode, os.path.join(home,'icons', 'punjabi.png'), True)

def  AddEmoviesMain(url):
    dummy,url=url.split('emovies:')
    urldata=json.loads(url)
    print urldata
    print urldata["type"]
    if urldata["type"]=="decade":
        addEmoviesFromSearch(urldata)
    elif urldata["type"]=="year":
        addEmoviesFromSearch(urldata)
    elif urldata["type"]=="decades":
        for s in ['2010','2000','1990','1980','1970','1960','1950','1940']:
            addDir ('Movies from %s'%s ,'emovies:{"lang":"%s","type":"decade","decadenum":"%s"}'%(urldata["lang"],s),listingMode,'', True)
    elif urldata["type"]=="years":
        for s in range(date.today().year, 1948, -1):
            addDir ('Movies from %s'%s ,'emovies:{"lang":"%s","type":"year","yearnum":"%s"}'%(urldata["lang"],s),listingMode,'', True)
    elif urldata["type"]=="search":
        if 'searchdata' not in urldata:
            userinput=xbmcgui.Dialog().input('Enter Search', type=xbmcgui.INPUT_ALPHANUM)
            if len(userinput)==0: return
            urldata["searchdata"]=userinput        
            searchurl='emovies:'+json.dumps(urldata)
            searchurl = '%s?mode=%d&url=%s' % (sys.argv[0], listingMode, urllib.quote_plus(searchurl))
            xbmc.executebuiltin('Container.Update(%s)' % searchurl)
            return
        addEmoviesFromSearch(urldata)
    elif urldata["type"]=="alpha":
        if 'searchdata' not in urldata:
            dialog = xbmcgui.Dialog()
            import string
            alphas=list(string.ascii_uppercase)
            index = dialog.select('Choose Starts with', alphas)
            userinput=""
            if index > -1:
                userinput=alphas[index]
            if len(userinput)==0: return
            urldata["searchdata"]=userinput
            searchurl='emovies:'+json.dumps(urldata)
            searchurl = '%s?mode=%d&url=%s' % (sys.argv[0], listingMode, urllib.quote_plus(searchurl))
            xbmc.executebuiltin('Container.Update(%s)' % searchurl)
            return
        addEmoviesFromSearch(urldata)
    elif urldata["type"]=="recent":
        addEmoviesFromSearch(urldata)
    else:
        print "Showing movie menu"    
        addDir ('Search Movie' ,'emovies:{"lang":"%s","type":"search"}'%(urldata["lang"]),listingMode,'', False)
        addDir ('Alphabetically List' ,'emovies:{"lang":"%s","type":"alpha"}'%(urldata["lang"]),listingMode,'', False)
        addDir ('Years' ,'emovies:{"lang":"%s","type":"years"}'%(urldata["lang"]),listingMode,'', True)
        addDir ('Decades' ,'emovies:{"lang":"%s","type":"decades"}'%(urldata["lang"]),listingMode,'', True)
        addDir ('Recently Added' ,'emovies:{"lang":"%s","type":"recent"}'%(urldata["lang"]),listingMode,'', True)


def addEmoviesFromSearch(urldata):
    url=""
    print 'addEmoviesFromSearch',urldata
    page="1"
    lang=urldata["lang"]
    url1=""
    url2=""
    if 'page' in urldata:
        page=urldata["page"]
    urlpage=int(page)*2
    if urldata["type"]=="decade":
        decadenumber=urldata["decadenum"]
        url1="https://einthusan.ca/movie/results/?decade=%s&find=Decade&lang=%s&page=%s"%(decadenumber,lang,str(urlpage-1))
        url2="https://einthusan.ca/movie/results/?decade=%s&find=Decade&lang=%s&page=%s"%(decadenumber,lang,str(urlpage))
    elif urldata["type"]=="year":
        yearnumber=urldata["yearnum"]
        url1="https://einthusan.ca/movie/results/?year=%s&find=Year&lang=%s&page=%s"%(yearnumber,lang,str(urlpage-1))
        url2="https://einthusan.ca/movie/results/?year=%s&find=Year&lang=%s&page=%s"%(yearnumber,lang,str(urlpage))
    elif urldata["type"]=="recent":
        url1="https://einthusan.ca/movie/results/?find=Recent&lang=%s&page=%s"%(lang,str(urlpage-1))
        url2="https://einthusan.ca/movie/results/?find=Recent&lang=%s&page=%s"%(lang,str(urlpage))
    elif urldata["type"]=="search":
        searchdata=urldata["searchdata"]
        url1="https://einthusan.ca/movie/results/?query=%s&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage-1))
        url2="https://einthusan.ca/movie/results/?query=%s&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage))
    elif urldata["type"]=="alpha":
        searchdata=urldata["searchdata"]
        url1="https://einthusan.ca/movie/results/?alpha=%s&find=Alphabets&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage-1))
        url2="https://einthusan.ca/movie/results/?alpha=%s&find=Alphabets&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage))
                
    newpage=str(int(page)+1)
    newpagedata=urldata
    newpagedata["page"]=newpage
    moviecode=""
    html1=""
    try:
        html1=getUrl(url1)
        if len(url2)>0:
            html1+=getUrl(url2)
    except: pass
    added=False
    for mov in re.findall( "<div class=\"block1\">.*?href=['\"].*?watch\/(.*?)\/\?lang=(.*?)['\"].*?src=['\"](.*?)['\"].*?<h3>(.*?)<",html1):
        try:
            added=True
            moviecode=mov[0]
            imageurl=mov[2]
            if imageurl.startswith('//'): imageurl='http:'+imageurl
            mname=mov[3]
            addDir (mname,base64.b64encode('emovies:%s,%s'%(moviecode,lang)),playingMode,imageurl, False)
        except: pass
    if added:
        addDir ('Next Page %s'%newpage ,'emovies:'+json.dumps(newpagedata),listingMode,'', True)

def PlayGen(url,checkUrl=False, followredirect=False):
    url = base64.b64decode(url)
    print 'gen is '+url

    if url.startswith('plugin://'):
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
        return
    
    if checkUrl and url.startswith('http') and '.m3u' in url:
        headers=[('User-Agent','AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)')]
        urldata=getUrl(url.split('|')[0],timeout=5,headers=headers)
        if followredirect:
            if not urldata.startswith('#EXTM3U'):
                url=urldata+'|'+url.split('|')[1]
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 
        

def decodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
	
def encodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
    
def PlayEinthusanLink(url,progress=None):
    url,lang=url.split(',')
    cookieJar = cookielib.LWPCookieJar()
    headers=[('Origin','https://einthusan.ca'),('Referer','https://einthusan.ca/movie/browse/?lang=hindi'),('User-Agent',base64.b64decode('TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzU1LjAuMjg4My44NyBTYWZhcmkvNTM3LjM2'))]
    mainurl='https://einthusan.ca/movie/watch/%s/?lang=%s'%(url,lang)
    mainurlajax='https://einthusan.ca/ajax/movie/watch/%s/?lang=%s'%(url,lang)
    
    htm=getUrl(mainurl,headers=headers,cookieJar=cookieJar)
    lnk=re.findall('data-ejpingables=["\'](.*?)["\']',htm)[0]#.replace('&amp;','&')

    jdata='{"EJOutcomes":"%s","NativeHLS":false}'%lnk
    
    h = HTMLParser.HTMLParser()
    gid=re.findall('data-pageid=["\'](.*?)["\']',htm)[0]
    gid=h.unescape(gid).encode("utf-8")
    
    postdata={'xEvent':'UIVideoPlayer.PingOutcome','xJson':jdata,'arcVersion':'3','appVersion':'59','gorilla.csrf.Token':gid}
    postdata = urllib.urlencode(postdata)
    rdata=getUrl(mainurlajax,headers=headers,post=postdata,cookieJar=cookieJar)
    r=json.loads(rdata)["Data"]["EJLinks"]
    print r
    lnk=json.loads(decodeEInth(r).decode("base64"))["HLSLink"]
      
    urlnew=lnk+('|https://einthusan.ca&Referer=%s&User-Agent=%s'%(mainurl,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'))
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    PlayGen(base64.b64encode(urlnew))
        

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
    mode=int(params["mode"])
except:
    pass

print params
args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
    linkType=args.get('linkType', '')[0]
except:
    pass

print 	mode,url,linkType

try:
    if mode==None or url==None or len(url)<1:
        singleLanguage=selfAddon.getSetting( "singleLanguage" )
        print "language setting is:"
        print singleLanguage
        if singleLanguage=="0" or singleLanguage=="":
            ChooseLanguage()
        else:
            languages=["hindi","hindi","tamil","telugu","malayalam","kannada","bengali","marathi","punjabi"]
            AddEmoviesMain('emovies:{"lang":"%s","type":"main"}'%languages[int(singleLanguage)])
    elif mode==langSelectMode:
        print("Language selected...URL is %s" %url) 
        AddEmoviesMain(url)
#        AddEmoviesMain('emovies:{"lang":"%s","type":"main"}'%urldata["lang"])
    elif mode==playingMode:
        url=base64.b64decode(url)
        print "Play url is "+url
        PlayEinthusanLink(url.split('emovies:')[1])
    elif mode in [listingMode] :
        print "List url is "+url
        AddEmoviesMain(url)
except:
    print 'somethingwrong'
    traceback.print_exc(file=sys.stdout)

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
        'skin.amber': 53
    },
}

def get_view_mode_id( view_mode):
    default_view_mode=selfAddon.getSetting( "usethisviewmode" )
    if default_view_mode=="":
        view_mode_ids = VIEW_MODES.get(view_mode.lower())
        if view_mode_ids:
            return view_mode_ids.get(xbmc.getSkinDir())
    else:
        return int(default_view_mode)
    return None

playmode=[playingMode]
try:
    if (not mode==None) and mode>1 and mode not in playmode:
        view_mode_id = get_view_mode_id('thumbnail')
        if overridemode: view_mode_id=overridemode
        if view_mode_id is not None:
            print 'view_mode_id',view_mode_id
            xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
except: traceback.print_exc(file=sys.stdout)

if not  (mode in  playmode ):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
        
