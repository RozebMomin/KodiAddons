import re, os, sys
import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from addon.common.addon import Addon
import sqlite3
import socket
import requests
import random
import json

addon_id = 'plugin.video.ditto-rain'
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

language = (Addon.getSetting('langType'))
livelanguage = (Addon.getSetting('livelangType'))
tvsort = (Addon.getSetting('tvsortType'))
moviessort = (Addon.getSetting('moviessortType'))
quality = (Addon.getSetting('qualityType')).lower()

base_url = 'http://www.dittotv.com'
# base2_url = '/tvshows/all/0/'+language+'/'
listitem=''

if 'Latest' in moviessort:
	moviessort = 'created%2Cdesc'
elif 'A-Z' in moviessort:
	moviessort = 'name%2Casc'
else:
	moviessort = 'name%2Cdesc'
	
if 'Latest' in tvsort:
	tvsort = 'created%2Cdesc'
elif 'A-Z' in tvsort:
	tvsort = 'name%2Casc'
else:
	tvsort = 'name%2Cdesc'	
	

s = requests.Session()

def addon_log(string):
    if debug == 'true':
        xbmc.log("[plugin.video.ditto2-rain-%s]: %s" %(addon_version, string))

def make_request(url):
    try:		
		headers = {'Accept':'text/html,application/xhtml+xml,q=0.9,image/jxr,*/*', 'Accept-Language':'en-US,en;q=0.5', 'Accept-Encoding':'gzip, deflate', 'Connection':'keep-alive', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
		response = s.get(url, headers=headers, cookies=s.cookies)
		return response.text
    except urllib2.URLError, e:    # This is the correct syntax
        print e
        
def get_menu():
	addDir(2, '[COLOR orange][B]TV Shows[/B][/COLOR]', '', '')
	addDir(3, '[COLOR white][B]Movies[/B][/COLOR]', '', '')        
	addDir(24, '[COLOR green][B]Live TV[/B][/COLOR]', '', '')
	addDir(5, 'Search', '', '')
	addDir(12, 'My Favorites Shows/Movies', '', '')
	addDir(14, 'My Favorite Live TV Channels', '', '')

def new_live_tv():
	r = make_request('http://www.dittotv.com/livetv')
	match = re.compile('Select Channel</option>(.+?)</select>', re.DOTALL).findall(r)[0]
	match2 = re.compile('<option value="(\d+)">(.+?)</option>').findall(match)
	for link, title in match2:
		if '&amp;' in title:
			title = title.replace('&amp;', '&')
		if '&#39;' in title:
			title = title.replace('&#39;', '\'')
		addDir(28,title,'http://www.dittotv.com/livetv/link?name='+urllib.quote_plus(title).replace('+','%20'),'http://dittotv2.streamark.netdna-cdn.com/vod_images/optimized/livetv/'+str(link)+'.jpg',dirmode='allshows', isplayable=True)
		
	setView('default','default-view')
		
def new_live_tv_url(name, url):
	s.headers['Referer']='http://www.dittotv.com/livetv'
	r = make_request(url)
	rjson = json.loads(r)
	url2 = urllib.unquote_plus(url)
	if '&' in name:
		name2 = name.replace('&', '%26')
	else:
		name2 = name
	if '&' in url2:
		url2 = url2.replace('&','and-')
	if ' ' in url2:
		url2 = url2.replace(' ', '-')
	m3 = rjson['link']+'|Referer=http://www.dittotv.com/livetv/'+url2.lower()
	listitem =xbmcgui.ListItem(name)
	listitem.setProperty('IsPlayable', 'true')
	listitem.setPath(m3)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
def new_movies_url(name, url):
	print 'inside ditto name', name
	print 'inside ditto', url
	r = make_request(url)
	# csrf = re.compile('<meta name="csrf-token" content="(.+?)">').findall(r)[0]
	movie_src = re.compile('<video.+?src="(.+?)".+?</video>', re.DOTALL).findall(r)[0]
	m3 = movie_src#+'|Referer='+url
	listitem = xbmcgui.ListItem(name)
	listitem.setProperty('IsPlayable', 'true')
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setPath(m3)
	print 'm3 is', m3
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def new_episodes_url(name, url):
	# print url
	r = make_request(url)
	# csrf = re.compile('<meta name="csrf-token" content="(.+?)">').findall(r)[0]
	movie_src = re.compile('<video.+?src="(.+?)".+?</video>', re.DOTALL).findall(r)[0]
	m3 = movie_src
	# print 'm3 is', m3
	listitem = xbmcgui.ListItem(name)
	listitem.setProperty('isPlayable', 'true')
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setPath(m3)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	# listitem.setProperty('IsPlayable', 'true')
	# # listitem.setProperty('mimetype', 'video/x-msvideo')
	# listitem.setPath(m3)
	# xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def get_favorites():
	print 'Display Favorite Shows'
	conn = sqlite3.connect(local_db)
	c = conn.cursor()
	# c.execute('DROP TABLE IF EXISTS ditto_fav_list')
	c.execute('CREATE TABLE IF NOT EXISTS ditto_fav_list (fav_name TEXT PRIMARY KEY, fav_url TEXT, fav_icon TEXT)')
	c.execute('SELECT fav_name, fav_url, fav_icon FROM ditto_fav_list')
	shows = c.fetchall()
	conn.close()
	if len(shows):
		# print shows # DEBUG
		xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
		for fav_name, fav_url, fav_icon in shows:
			if 'livetv' not in fav_url:
				# addDir(28, fav_name, fav_url, fav_icon, dirmode='favorites',isplayable=True)
			# else:
				addDir(1, fav_name, fav_url, fav_icon, dirmode='favorites')
	else:
		dialog.notification('Info', 'No shows were added to the addon favorites.', xbmcgui.NOTIFICATION_INFO, 3000)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
	setView('episodes', 'episode-view')
	
def get_live_favorites():
	# print 'Display Favorite Live channels'
	conn = sqlite3.connect(local_db)
	c = conn.cursor()
	# c.execute('DROP TABLE IF EXISTS ditto_fav_list')
	c.execute('CREATE TABLE IF NOT EXISTS ditto_fav_list (fav_name TEXT PRIMARY KEY, fav_url TEXT, fav_icon TEXT)')
	c.execute('SELECT fav_name, fav_url, fav_icon FROM ditto_fav_list')
	shows = c.fetchall()
	conn.close()
	if len(shows):
		print shows # DEBUG
		xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
		for fav_name, fav_url, fav_icon in shows:
			if 'livetv' in fav_url:
				addDir(28, fav_name, fav_url, fav_icon, dirmode='favorites',isplayable=True)
			# else:
				# addDir(1, fav_name, fav_url, fav_icon, dirmode='favorites')
	else:
		dialog.notification('Info', 'No Live TV channels were added.', xbmcgui.NOTIFICATION_INFO, 3000)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
	setView('episodes', 'episode-view')
	
def edit_favorites(fav_arg):
    # print 'Favorites function activated'
    # print 'Parameter: ' + str(fav_arg)
    data = fav_arg.split('\;')
    fav_mode = data[0].replace('MODE:', '')
    fav_name = data[1].replace('NAME:', '')
    fav_url = data[2].replace('URL:', '')
    fav_icon = data[3].replace('IMG:','')
    # print 'Mode:',fav_mode
    # print 'Url:',fav_url
    # print 'Show name:',fav_name

    # Connect to DB
    conn = sqlite3.connect(local_db)
    c = conn.cursor()
    # c.execute('DROP TABLE IF EXISTS ditto_fav_list')
    c.execute('CREATE TABLE IF NOT EXISTS ditto_fav_list (fav_name TEXT PRIMARY KEY, fav_url TEXT, fav_icon TEXT)')

    if fav_mode == 'ADD':
        progress = xbmcgui.DialogProgress()
        progress.create('Adding to favorites', 'Added "{0}" to favorites'.format(fav_name))
        progress.update( 50, "", 'Getting show icon...', "" )
        print 'Adding Favorite'
        content = make_request(fav_url)
        # show_icon = ''
        c.execute('INSERT OR REPLACE INTO ditto_fav_list VALUES ("{0}", "{1}", "{2}")'.format(fav_name, fav_url, fav_icon))
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
		search_url = url
	else:
		keyb = xbmc.Keyboard('', 'Search for Movies/TV Shows/Trailers/Videos in all languages')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_term = urllib.quote_plus(keyb.getText())
			
		search_url = 'http://www.dittotv.com/search?q='+search_term

	r=make_request(search_url)
	match = re.compile('<div class="result clearfix">\s+<a href="(.+?)" class="poster">\s+<img src="(.+?)".+?<a.+?>\s+(.+?)\s+<', re.DOTALL).findall(r)
	for link, img, name in match:
		print link, img, name
		if 'livetv' not in link:
			if '&amp;' in name:
				name = name.replace('&amp;', '&')
			if '&#039;' in name:
				name = name.replace('&#039;', '\'')
			if '&amp;' in img:
				img = img.replace('&amp;', '&')
			if 'tvshow' not in link:
				addDir(29, name, base_url+link, img, isplayable=True)
			else:
				addDir(1, name, base_url+link, img, dirmode='allshows', isplayable=False)
			
	match2 = re.compile('<li class="next"><a href="(.+?)" data-page', re.DOTALL).findall(r)
	
	if match2:
		# match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		match3 = match2[0]
		match3 = match3.replace('&amp;', '&')
		addDir(5, '[COLOR gold]>>> Next Page >>>[/COLOR]', match3, '')		
	else:
		print "no more next page"
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def get_movies():

	if url:
		r=make_request(url)
	else:
		new_url ='/movies?page=1&ListingForm%5BorderBy%5D='+moviessort+'&ListingForm%5Blanguage%5D='+language+'&ListingForm%5Bgenre%5D=All'
		r = make_request(base_url+new_url)

	match = re.compile('<div class="unit item movie-item pull-left".+?<a href="(.+?)".+?img src=\'(.+?)\'.+?alt="(.+?)"', re.DOTALL).findall(r)
	print match

	for link, img, name in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(29, name, link, img, isplayable=True)  

	match2 = re.compile('<li class="next"><a href="(.+?)" data-page').findall(r)

	if match2:
		# match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		match3 = match2[0].replace('name%2Casc', moviessort)
		match3 = match3.replace('&amp;', '&')
		addDir(3, '[COLOR gold]>>> Next Page >>>[/COLOR]', match3, '')		
	else:
		print "no more next page"

	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
	setView('movies', 'movie-view')
        
def get_shows():
	if url:
		r=make_request(url)
	else:
		new_url ='/tvshows?page=1&ListingForm%5BorderBy%5D='+tvsort+'&ListingForm%5Blanguage%5D='+language+'&ListingForm%5Bgenre%5D=All'
		r = make_request(base_url+new_url)

	match = re.compile('<div class="unit item movie-item pull-left".+?<a href="(.+?)".+?img src=\'(.+?)\'.+?alt="(.+?)"', re.DOTALL).findall(r)
	print match

	for link, img, name in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(1, name, base_url+link, img, dirmode='allshows', isplayable=False)  

	match2 = re.compile('<li class="next"><a href="(.+?)" data-page').findall(r)

	if match2:
		# match3 = re.compile('<a href="(.+?)" class="next-epg"').findall(r)
		match3 = match2[0].replace('name%2Casc', moviessort)
		match3 = match3.replace('&amp;', '&')
		addDir(2, '[COLOR gold]>>> Next Page >>>[/COLOR]', match3, '', isplayable=False)		
	else:
		print "no more next page"
		
	# if (moviessort == "name"):
		# xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )

	# xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
	# setView('', 'movie-view')

	setView('episodes', 'episode-view')

def get_episodes():
	# print 'inside getepisodes', url
	r = make_request(url)
	match = re.compile('<li\s+>.+?<a href="(.+?)">.+?</svg>\s+(.+?)\s+</a>', re.DOTALL).findall(r)
	for link, name in match:
		if '&amp;' in name:
			name = name.replace('&amp;', '&')
		if '&#39;' in name:
			name = name.replace('&#39;', '\'')
		addDir(30, name, base_url+link, '', isplayable=True) 
    
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

	setView('episodes', 'episode-view')
    
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
	
def addDir(mode,name,url,image,dirmode=None,isplayable=False):
	print 'inside addDir'

	if 0==mode:
		link = url
	else:
		link = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&image="+urllib.quote_plus(image)

	ok=True
	item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
	item.setInfo( type="Video", infoLabels={ "Title": name } )
	if 'tv-show' in url:
		item.setArt({'fanart': image})

	if dirmode == 'allshows': 
		add_fav_cmd = 'MODE:ADD\;NAME:{0}\;URL:{1}\;IMG:{2}'.format(urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image))
		RunPlugin2 = 'RunPlugin({0}?mode=13&fav_arg={1})'.format(sys.argv[0], add_fav_cmd)
		item.addContextMenuItems([('Add Ditto Favorites', RunPlugin2,)])
	if dirmode == 'favorites':
		rem_fav_cmd = 'MODE:REMOVE\;NAME:{0}\;URL:{1}\;IMG:{2}'.format(urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image))
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

if mode==5:
	get_search()
	
if mode==1:
    get_episodes()

if mode==12:
	get_favorites()

if mode==13:
	edit_favorites(fav_arg)
	
if mode==14:
	get_live_favorites()
	
if mode==24:
	new_live_tv()

if mode==28:
	new_live_tv_url(name, url)
	
if mode==29:
	new_movies_url(name, url)
	
if mode==30:
	new_episodes_url(name, url)
	
# if mode==31:
	# play_new_movies_url(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
s.close()