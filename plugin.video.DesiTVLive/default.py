import re, os, sys
import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from addon.common.addon import Addon
import time
import base64, json
import pyaes
import sqlite3
import socket


addon_id = 'plugin.video.DesiTVLive'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
debug = Addon.getSetting('debug')

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addonDir = xbmc.translatePath(Addon.getAddonInfo('path'))
profile = xbmc.translatePath(Addon.getAddonInfo('profile'))
local_db = os.path.join(profile, 'local_db.db')
pluginDir = sys.argv[0]
dialog = xbmcgui.Dialog()

language = (Addon.getSetting('langType')).lower()
tvsort = (Addon.getSetting('tvsortType')).lower()
moviessort = (Addon.getSetting('moviessortType')).lower()
ipaddress = (Addon.getSetting('ipaddress'))

base_url = 'http://origin.dittotv.com'
base2_url = '/tvshows/all/0/'+language+'/'
listitem=''

# Create addon folder in user_data, necessary for the sqlite db
if Addon.getSetting("firstrun") != 'false':
	Addon.setSetting("firstrun", 'false')

def addon_log(string):
    if debug == 'true':
        xbmc.log("[plugin.video.DesiTVLive-%s]: %s" %(addon_version, string))

def make_request(url):
    try:
        if ipaddress != "0.0.0.0":
		    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 'Accept' : 'text/html,application/xhtml+xml,application/xml', 'X-Forwarded-For': ipaddress}
        else:
		    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 'Accept' : 'text/html,application/xhtml+xml,application/xml'}
        if url == None:
        	url = base2_url
        request = urllib2.Request(url,None,headers)
        response = urllib2.urlopen(request)
        data = response.read()
        response.close()
        return data
    except urllib2.URLError, e:    # This is the correct syntax
        print e
        ##sys.exit(1)
        
def get_menu():

	addDir(2, '[COLOR orange][B]TV Shows[/B][/COLOR]', '', '')
	addDir(3, '[COLOR white][B]Movies[/B][/COLOR]', '', '')        
	addDir(4, '[COLOR green][B]Live TV[/B][/COLOR]', '', '')
	addDir(5, 'Search', '', '')
	addDir(12, 'My Favorites', '', '')

def get_favorites():
	print 'Display Favorite Shows'
	conn = sqlite3.connect(local_db)
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS ditto_fav_list (fav_name TEXT PRIMARY KEY, fav_url TEXT, fav_icon TEXT)')
	c.execute('SELECT fav_name, fav_url, fav_icon FROM ditto_fav_list')
	shows = c.fetchall()
	conn.close()
	if len(shows):
		print shows # DEBUG
		xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
		for fav_name, fav_url, fav_icon in shows:
			addDir(1, fav_name, fav_url, fav_icon, dirmode='favorites')
	else:
		dialog.notification('Info', 'No shows were added to the addon favorites.', xbmcgui.NOTIFICATION_INFO, 2000)

	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def edit_favorites(fav_arg):
    print 'Favorites function activated'
    print 'Parameter: ' + str(fav_arg)
    data = fav_arg.split(';')
    fav_mode = data[0].replace('MODE:', '')
    fav_name = data[1].replace('NAME:', '')
    fav_url = data[2].replace('URL:', '')
    print 'Mode:',fav_mode
    print 'Url:',fav_url
    print 'Show name:',fav_name

    # Connect to DB
    conn = sqlite3.connect(local_db)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS ditto_fav_list (fav_name TEXT PRIMARY KEY, fav_url TEXT, fav_icon TEXT)')

    if fav_mode == 'ADD':
        progress = xbmcgui.DialogProgress()
        progress.create('Adding to favorites', 'Added "{0}" to favorites'.format(fav_name))
        progress.update( 50, "", 'Getting show icon...', "" )
        print 'Adding Favorite'
        content = make_request(fav_url)
        show_icon = ''
        c.execute('INSERT OR REPLACE INTO ditto_fav_list VALUES ("{0}", "{1}", "{2}")'.format(fav_name, fav_url, show_icon))
        progress.close()
        header = 'Show Added'
        text = '"{0}" added to favorites.'.format(fav_name)

    else:
        print 'Removing Favorite'
        c.execute('DELETE FROM ditto_fav_list WHERE fav_name="{0}"'.format(fav_name))
        header = 'Show Removed'
        text = '"{0}" removed from favorites.'.format(fav_name)
    conn.commit()
    conn.close()
    dialog.notification(header, text, xbmcgui.NOTIFICATION_INFO, 3000)
    xbmc.executebuiltin("Container.Refresh")
	
def get_search():
	if url:
		search_url = base_url+url
	else:
		keyb = xbmc.Keyboard('', 'Search for Movies/TV Shows/Trailers/Videos in all languages')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_term = urllib.quote_plus(keyb.getText())
			if not search_term:
				addon.show_ok_dialog(['empty search not allowed'.title()], addon.get_name())
				sys.exit()				
		else:
			get_menu()

			
		search_url = 'http://origin.dittotv.com/search/all/0/'+search_term

	r=make_request(search_url)
	match = re.compile('<a href="(.+?)">\s+<h1 title="(.+?)">[^"]+<img  src="(.+?)".*\n.*>(.+?)</span>').findall(r)
	for link, name, img, movie in match:
		if (movie != 'Live TV'):
			if '&amp;' in name:
				name = name.replace('&amp;', '&')
			if '&#39;' in name:
				name = name.replace('&#39;', '\'')
			if '&amp;' in img:
				img = img.replace('&amp;', '&')
			if (movie!= 'TV Show'):
				addDir(8, name, link, img, isplayable=True)
			else:
				addDir(1, name, base_url+link, img, dirmode='allshows', isplayable=False)
			
	match2 = re.compile('class="next-epg next-disabled"').findall(r)
	
	if match2:
		print "no more next page"		
	else:
		match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		addDir(4, '>>> Next Page >>>', match3[0], '')
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_livetv():
	if url:
		base4_url = base_url+url
	else:
		base4_url = 'http://origin.dittotv.com/livetv/all/0/'+language
	r = make_request(base4_url)

	match = re.compile('<div class="subpattern2 movies-all-indi channels-all alltvchannel">\s+<a href="(.+?)" title="(.+?)">.+?<img src="(http.+?)"', re.DOTALL).findall(r)
	
	for link, name, img in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(8, name, link, img, isplayable=True)
		
	match2 = re.compile('class="next-epg next-disabled"').findall(r)
	
	if match2:
		print "no more next page"		
	else:
		match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		addDir(4, '>>> Next Page >>>', match3[0], '')
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def get_movies():
	base3_url = '/movies/all/0/'+language

	if url:
		r=make_request(base_url+url)
	else:
		r = make_request(base_url+base3_url)

	match = re.compile('<a href="(.+?)" title="(.+?)" >\n.*<img src="(.+?)"').findall(r)

	for link, name, img in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(8, name, link, img, isplayable=True)  

	match2 = re.compile('class="next-epg next-disabled"').findall(r)

	if match2:
		print "no more next page"		
	else:
		match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		addDir(3, '>>> Next Page >>>', match3[0], '')
		
	if (moviessort == "name"):
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )

	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
	setView('movies', 'movie-view')
        
def get_shows():
	if url:
		r=make_request(base_url+url)
	else:
		r = make_request(base_url+base2_url)

	match = re.compile('<a href="(.+?)" title="(.+?)">\s+<img  src="(.+?)"').findall(r)

	for link, name, img in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(1, name, base_url+link, img, dirmode='allshows', isplayable=False) 

	match2 = re.compile('class="next-epg next-disabled"').findall(r)

	if match2:
		print "no more next page"		
	else:
		match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		addDir(2, '>>> Next Page >>>', match3[0], '')
		
	if (tvsort == "name"):
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )

	xbmcplugin.endOfDirectory(int(sys.argv[1]))

	# setView('tvshows', 'default-view')

def get_episodes():
	r = make_request(url+'/episodes')

	match = re.compile('<a href="(.+?)" title="(.+?)">\s+<img src="(.+?)"').findall(r)
	for link, name, img in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(8, name, link, img, isplayable=True) 
    
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def get_livetv_url(url, name):
    addon_log('get_video_url: begin...')
    videos = []
    ptclass=name
    # ptclass=ptclass.rsplit('/')[-1:][0]
    html = make_request(base_url+url)
    encurl = re.findall(r'\"file\":\"(.+?)\"', html)[0]
    if 'livetv' in url:
        key = re.findall(r'value=\"(.*?)\" class=\"livetv-url-val\"', html)[0]
    else:
        key = re.findall(r'value=\"(.*?)\" class=\"e-url-val\"', html)[0]
    decrypted = GetLSProData(key=key, iv='00000000000000000000000000000000', data=encurl)
    # params = re.compile("(http://[^']*\/)").findall(decrypted)
    # if params:
        # params = params[0]
    # else:
        # params = ''
	
    # html2 = make_request(decrypted)
    # if html2:
		# matchlist2 = re.compile("BANDWIDTH=([0-9]+)[^\n]*\n([^\n]*)\n").findall(str(html2))
		# if matchlist2:
			# for (size, video) in matchlist2:
				# if size:
					# size = int(size)
				# else:
					# size = 0
				# if 'http://' in video:
					# video = video
				# else:
					# video=params+video
				# videos.append( [size, video] )
    # else:
        # videos.append( [-2, match] )

    # videos.sort(key=lambda L : L and L[0], reverse=True)

    # addon_log('get_video_url: end...')
    # final_video = videos[0][1]
    listitem =xbmcgui.ListItem(ptclass)
    listitem.setProperty('IsPlayable', 'true')
    listitem.setPath(decrypted)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)		
		
    # xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def setView(content, viewType):
        
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

	#Thanks Shani(LSP)
def GetLSProData(key,iv,data):
    import binascii
    key=base64.b64decode(key)
    iv=binascii.unhexlify(iv)
    data=base64.b64decode(data)
    decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
    val1= decryptor.decrypt(data)
    val2= repr(val1).partition('\\')
    retval= val2[0].replace('\'', '')
    return retval
	
def addDir(mode,name,url,image, dirmode=None, isplayable=False):
	# name = name.encode('utf-8', 'ignore')
	# url = url.encode('utf-8', 'ignore')
	# image = image.encode('utf-8', 'ignore')

	if 0==mode:
		link = url
	else:
		link = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&image="+urllib.quote_plus(image)

	ok=True
	item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
	item.setInfo( type="Video", infoLabels={ "Title": name } )

	if dirmode == 'allshows': 
		add_fav_cmd = 'MODE:ADD;NAME:{0};URL:{1}'.format(urllib.quote_plus(name), urllib.quote_plus(url))
		RunPlugin2 = 'RunPlugin({0}?mode=13&fav_arg={1})'.format(sys.argv[0], add_fav_cmd)
		item.addContextMenuItems([('Add Ditto Favorites', RunPlugin2,)])
	if dirmode == 'favorites':
		rem_fav_cmd = 'MODE:REMOVE;NAME:{0};URL:{1}'.format(urllib.quote_plus(name), urllib.quote_plus(url))
		RunPlugin = 'RunPlugin({0}?mode=13&fav_arg={1})'.format(sys.argv[0], rem_fav_cmd)
		item.addContextMenuItems([('Remove from Ditto Favorites', RunPlugin,)])

	isfolder=True
	if isplayable:
		item.setProperty('IsPlayable', 'true')
		isfolder=False
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=link,listitem=item,isFolder=isfolder)
	return ok

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

params=get_params()
mode=None
name=None
url=None
image=None
fav_arg = None

try:
    mode=int(params["mode"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    image=urllib.unquote_plus(params["image"])
except:
    pass
try:
    fav_arg = urllib.unquote_plus(params["fav_arg"])
except:
    pass

addon_log("Mode: "+str(mode))
addon_log("Name: "+str(name))
addon_log("URL: "+str(url))
addon_log("Image: "+str(image))

if mode==None:
	get_menu()
    
if mode==2:
    get_shows()

if mode==3:
    get_movies()
    
if mode==4:
    get_livetv()

if mode==5:
	get_search()
	
if mode==1:
    get_episodes()

if mode==8:
    get_livetv_url(url, name)
    
if mode==11:
    get_video_url()

if mode==12:
	get_favorites()

if mode==13:
	edit_favorites(fav_arg)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
