import os, os.path
import sys
import xbmc, xbmcgui
import xbmcplugin
import urllib
import urllib2
import re
import json
import glob
import requests
from resources.utils import encoders
from resources.slimit import ast
from resources.slimit.parser import Parser
from resources.slimit.visitors import nodevisitor
from BeautifulSoup import BeautifulSoup 
import urlparse

## Global Variables & Functions
player = xbmc.Player()
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')


#######################################################

def movieUnpackerFunction(encryptedObject):
	paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(encryptedObject)
	video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
	video_links = re.compile(r"(file:\'(.+?)\')").findall(video_info_link)
	for item in video_links:
		item = str(item)
		if "m3u8" not in item:
			if ".vtt" not in item:
				item = item.split('", ')[0].replace('("file:', '').replace("'", "")
				if item is None:
					return "Video Not Found"
				else:
					return item
				# return item or "Video Not Found"

#######################################################

def movieDomainResolver(domain, mediaId, link, name):
	if "watchshare" in domain:
		# pass
		hostUrl = "http://watchshare.net/embed/"+mediaId
		soup = BeautifulSoup(requests.get(hostUrl).text)
		sourceTag = soup.find("source",{"type":"video/mp4"}, src=True)
		mediaLink = sourceTag["src"]
		result = mediaLink
		streamingName = name + "[COLOR green]: WatchShare[/COLOR]"
		addDir('', '', result, streamingName, '', '')
		# createPlayableItem(domain, name, mediaLink)
	elif "vkprime" in domain:
		functionsArray = []
		hostUrl = "https://vkprime.com/embed-"+mediaId+".html"
		soup = BeautifulSoup(requests.get(hostUrl).text)
		fullPackedFunction = soup.findAll("script", {"type":"text/javascript"})
		for function in fullPackedFunction:
			functionsArray.append(function)
		for line in functionsArray:
			if "eval(function(p,a,c,k,e,d)" in line.text:
				encryptedFunction = str(line).replace('<script type="text/javascript">', '').replace("</script>","").strip()
				mediaLink = movieUnpackerFunction(encryptedFunction)
				result = mediaLink
				streamingName = name + "[COLOR yellow]: VK Prime[/COLOR]"
				addDir('', '', result, streamingName, '', '')
			elif "file:" in line.text:
				lines = str(line).splitlines()
				for item in lines:
					if "/ads/" in item:
						print "No Video Found"
					elif "mp4" in item:
						videoArray = item.strip().replace("sources: [{", "").replace("}],", "").replace("},{", "...").replace("file:", "").replace('"','').split("...")
						for link in videoArray:
							if "m3u8" not in link:
								finalLink = link.split(",label:")[0]
								mediaLink = finalLink
								if finalLink is None:
									print "Video Not Found"
								else:
									result = mediaLink
									streamingName = name + "[COLOR yellow]: VK Prime[/COLOR]"
									addDir('', '', result, streamingName, '', '')
	elif "vidoza" in domain:
		# pass
		hostUrl = "https://vidoza.net/embed-"+mediaId+".html"
		soup = BeautifulSoup(requests.get(hostUrl).text)
		soup = soup.text.splitlines()
		if "Full movie" in name:
			name = "Full Movie"
		for line in soup:
			if "sourcesCode" in line:
				line = line.strip().replace("sourcesCode: ", "").replace("[{", "").replace("}],", "").split(",")
				for item in line:
					if "src:" in item:
						mediaLink = item.strip().replace('src: "', '').replace('mp4"', 'mp4')
						result = mediaLink
						streamingName = name + "[COLOR green]: Vidoza[/COLOR]"
						addDir('', '', result, streamingName, '', '')
	elif "vkspeed" in domain:
		# pass
		functionsArray = []
		hostUrl = "http://vkspeed.com/embed-"+mediaId+".html"
		soup = BeautifulSoup(requests.get(hostUrl).text)
		fullPackedFunction = soup.findAll("script", {"type":"text/javascript"})
		for function in fullPackedFunction:
			functionsArray.append(function)
		for line in functionsArray:
			if "eval(function(p,a,c,k,e,d)" in line.text:
				encryptedFunction = str(line).replace('<script type="text/javascript">', '').replace("</script>","").strip()
				mediaLink = movieUnpackerFunction(encryptedFunction)
				result = mediaLink
				streamingName = name + "[COLOR yellow]: VK Speed[/COLOR]"
				addDir('', '', result, streamingName, '', '')
			elif "file:" in line.text:
				lines = str(line).splitlines()
				for item in lines:
					if "/ads/" in item:
						print "No Video Found"
					elif "mp4" in item:
						videoArray = item.strip().replace("sources: [{", "").replace("}],", "").replace("},{", "...").replace("file:", "").replace('"','').split("...")
						for link in videoArray:
							if "m3u8" not in link:
								finalLink = link.split(",label:")[0]
								mediaLink = finalLink
								if finalLink is None:
									print "Video Not Found"
								else:
									result = mediaLink
									streamingName = name + "[COLOR yellow]: VK Speed[/COLOR]"
									addDir('', '', result, streamingName, '', '')
	else:
		pass

#######################################################
#######################################################

def tvUnpackerFunction(encryptedObject):
	paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(encryptedObject)
	video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
	video_links = re.compile(r"(file:\'(.+?)\')").findall(video_info_link)
	for item in video_links:
		item = str(item)
		if "m3u8" not in item:
			if ".vtt" not in item:
				item = item.split('", ')[0].replace('("file:', '').replace("'", "")
				if item is None:
					return "Video Not Found"
				else:
					return item
				# return item or "Video Not Found"

################################################

def domainResolver(domain, mediaId, link, name, xbmcUrl):
	if "watchshare" in domain:
		# pass
		hostUrl = "http://watchshare.net/embed/"+mediaId
		soup = BeautifulSoup(requests.get(hostUrl).text)
		sourceTag = soup.find("source",{"type":"video/mp4"}, src=True)
		if sourceTag is None:
			pass
		else:
			mediaLink = sourceTag["src"]
			result = mediaLink
			streamingName = name + "[COLOR yellow]: Watch Share[/COLOR]"
			addDir('', '', result, streamingName, '', '')
	elif "daily" in domain:
		try:
			hostUrl = "https://p1.tvlogy.me/hls/"+mediaId+"/"+mediaId+".m3u8"
			soup = BeautifulSoup(requests.get(hostUrl).text)
			if "Not ready" in soup:
				pass
			else:
				result = hostUrl
				streamingName = name + "[COLOR green]: Daily Motion[/COLOR]"
				addDir('', '', result, streamingName, '', '')
		except Exception as e:
			print "Error"
		else:
			hostUrl = "https://p2.tvlogy.me/hls/"+mediaId+"/"+mediaId+".m3u8"
			soup = BeautifulSoup(requests.get(hostUrl).text)
			# print soup.prettify()
			if "Not ready" in soup:
				pass
			else:
				result = hostUrl
				streamingName = name + "[COLOR green]: Daily Motion[/COLOR]"
				addDir('', '', result, streamingName, '', '')
		finally:
			hostUrl = "https://p3.tvlogy.me/hls/"+mediaId+"/"+mediaId+".m3u8"
			soup = BeautifulSoup(requests.get(hostUrl).text)
			# print soup.prettify()
			if "Not ready" in soup:
				pass
			else:
				result = hostUrl
				streamingName = name + "[COLOR green]: Daily Motion[/COLOR]"
				addDir('', '', result, streamingName, '', '')
	elif "speed" in domain:
		# pass
		functionsArray = []
		hostUrl = "http://vkspeed.com/embed-"+mediaId+"-600x380.html"
		soup = BeautifulSoup(requests.get(hostUrl).text)
		fullPackedFunction = soup.findAll("script", {"type":"text/javascript"})
		for function in fullPackedFunction:
			functionsArray.append(function)
		for line in functionsArray:
			if "eval(function(p,a,c,k,e,d)" in line.text:
				encryptedFunction = str(line).replace('<script type="text/javascript">', '').replace("</script>","").strip()
				mediaLink = tvUnpackerFunction(encryptedFunction)
				result = mediaLink
				streamingName = name + "[COLOR yellow]: Speed Watch[/COLOR]"
				addDir('', '', result, streamingName, '', '')
			elif "file:" in line.text:
				lines = str(line).splitlines()
				for item in lines:
					if "/ads/" in item:
						print "No Video Found"
					elif "mp4" in item:
						videoArray = item.strip().replace("sources: [{", "").replace("}],", "").replace("},{", "...").replace("file:", "").replace('"','').split("...")
						for link in videoArray:
							if "m3u8" not in link:
								finalLink = link.split(",label:")[0]
								mediaLink = finalLink
								if finalLink is None:
									print "Video Not Found"
								else:
									result = mediaLink
									streamingName = name + "[COLOR yellow]: Speed Watch[/COLOR]"
									addDir('', '', result, streamingName, '', '')
	else:
		pass

################################################

################################################

def getEpisodeSources(name, link, xbmcUrl):
	r = requests.get(link)
	data = r.text

	soup = BeautifulSoup(data)

	## Pass Episode Page Link to Aggregate Host Links

	mainArea = soup.findAll("a", {"rel":"nofollow"}, href=True)

	for link in mainArea:
		if "Watch Online" in link.text:
			sourceName = link.text.split("-")[1].strip()
			sourceLink = link["href"]
			sourceMediaId = sourceLink.split("=")[1]
			if "php?" in sourceLink:
				sourceDomain = re.search(".[a-zA-Z]/(.*?)\.php", sourceLink)
				if sourceDomain is None:
					pass
				else:
					sourceDomain = sourceDomain.group(1)
					domainResolver(sourceDomain, sourceMediaId, sourceLink, sourceName, xbmcUrl)
			elif "?sim" in sourceLink:
				if len(sourceMediaId) == 32:
					sourceDomain = "daily"
					domainResolver(sourceDomain, sourceMediaId, sourceLink, sourceName, xbmcUrl)
				else:
					sourceDomain = "vkprime"
					domainResolver(sourceDomain, sourceMediaId, sourceLink, sourceName, xbmcUrl)
			else:
				pass

##########################################################################################################################################################
# NECESSARY KODI FUNCTIONS
# FILE SYSTEM, DIRECTORY, & BUILDING URL FUNCTIONS 
##########################################################################################################################################################

def addDir(dir_type, mode, url, name, iconimage, fanart):
	base_url = sys.argv[0]
	base_url += "?url="       +urllib.quote_plus(url)
	base_url += "&mode="      +str(mode)
	base_url += "&name="      +urllib.quote_plus(name)
	base_url += "&iconimage=" +urllib.quote_plus(iconimage)
	base_url += "&fanart="    +urllib.quote_plus(fanart)

	li = xbmcgui.ListItem(name, iconImage=iconimage)

	li.setInfo(type="Video", infoLabels={"Title": name})
	li.setProperty("Fanart_Image", fanart)

	if dir_type != '':
		link = xbmcplugin.addDirectoryItem(handle=addon_handle, url=base_url, listitem=li, isFolder=True)
	else:
		link = xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	return link

def read_file(filename):
	readfile = open(filename, 'r')
	content = readfile.read()
	readfile.close()
	return content

def Open_URL(url):
	req = urllib2.Request(url)
	req.add_header('User-agent', 'Mozilla 5.10')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	return link.replace('\n','').replace('\t','').replace('\r','')

def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

##########################################################################################################################################################
# LATEST PARSING AS OF 08/19/2018
# SIMPLIFIED PARSING
##########################################################################################################################################################

def load_episode_links():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	main_url = main_url.replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=")
	split_url = main_url.split("===")
	main_url = split_url[0]
	showName = split_url[1].replace("+", " ")
	episode_url = main_url.replace("plugin://plugin.video.DTVShows/?linkName=","").split("?s=")[0]
	print "EPISODE URL -->" + episode_url

	episodeName = showName
	episodeLink = episode_url

	getEpisodeSources(episodeName, episodeLink, main_url)


def fetch_show_names(url):
	print url
	r = requests.get(url)
	showNames = []
	linksArray = []
	for line in r.text.splitlines():
		if "<h2 class=\"forumtitle\">" in line:
			line = line.strip()
			line = line.encode('utf-8')
			line = line.replace("<h2 class=\"forumtitle\"><a href=\"", "").replace("</a></h2>", "").replace("<b><font color=\"blue\">", "").replace("</font></b>","").replace("&amp;", "&")
			showLink = line.split("\">")[0]
			linksArray.append(showLink)
			line = line.split("\">")[1]
			showNames.append(line)
		else:
			pass
	del showNames[-1]
	outputArray = zip(showNames, linksArray)
	return outputArray


def fetch_show_episodes():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	base_url = main_url.replace("plugin://plugin.video.DTVShows/?linkName=","").replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=").split("?s=")[0]
	showName = base_url.split("=SNAME=")[1].replace("+", " ")
	base_url = base_url.split("=SNAME=")[0]

	url = base_url

	r = requests.get(url)
	data = r.text

	soup = BeautifulSoup(data)

	## Pass Episode Page Link to Aggregate Host Links

	mainArea = soup.findAll("a", {"class":"title"}, href=True)

	for link in mainArea:
			if "Watch Online" in link.text:
				episodeLink = link["href"]
				episodeName = link.text
				episodeName = re.search("([0-9]+[a-z]+ [A-Za-z]+)", episodeName).group(1)
				linksURL = build_url({'linkName': episodeLink + "===" + episodeName})
				addDir('folder', 'episode_to_links', linksURL, episodeName, '', '')


##########################################################################################################################################################
# MAIN MENU & MOVIE MENU
##########################################################################################################################################################

def Main_Menu():
	## Movies ##
	movies_fanart = "http://www.techicy.com/wp-content/uploads/2015/01/Indian-Flag-Wallpapers-HD-Images-Free-Download-2-1024x576.jpg"
	movies_icon = "http://www.owensvalleyhistory.com/at_the_movies22/themovies01.png"
	addDir('folder', 'load_movies', "[COLOR blue]MOVIES[/COLOR]", "[COLOR blue]LATEST MOVIES[/COLOR]", movies_icon, movies_fanart)

	## On Demand Shows ##
	channelsOnlineURL = "http://sonaled.com/dtvmc/channels/index.php"
	content = Open_URL(channelsOnlineURL)
	# xbmc.log('### CONTENTS: %s' % content)
	matches = re.compile('name="(.+?)"mode="(.+?)"icon="(.+?)"fanart="(.+?)"').findall(content)
	for item in matches:
		channel_name =      item[0]
		dir_mode =          item[1]
		channel_icon =      item[2]
		channel_fanart =    item[3]
		addDir('folder', 'channel_to_shows', channel_name, channel_name, channel_icon, channel_fanart)

def movie_menu():
	url = "http://www.desirulez.cc/exclusive-movie-hq-20/"
	r = requests.get(url)
	data = r.text

	soup = BeautifulSoup(data)

	mainArea = soup.findAll("a", {"class":"title"}, href=True)

	for title in mainArea:
	  movieTitle = title.text.replace("Watch Online / Download", "").replace(" Full Hindi Dubbed Movie Online Free", "").replace(" Full Hindi Dubbed Movie Online", "")
	  if "(All EPISODE)" not in movieTitle:
		if "(Season " not in movieTitle:
		  if "(E01-" not in movieTitle:
			movieTitle = movieTitle.split("| ")[0]
			movieLink = title["href"].split("?s=")[0]
			linksURL = build_url({'linkName': movieLink + "===" + movieTitle})
			addDir('folder', 'load_movie_links', linksURL, movieTitle, '', '')

##########################################################################################################################################################
# LOAD SHOWS ONCE CHANNEL IS SELECTED 
##########################################################################################################################################################

def load_shows():
	base_url = sys.argv[2]
	base_url = base_url.split('channel_to_shows')[1].split('&', 2)
	base_url = base_url[1].replace('name=', '').replace('%20', '')
	channelName = base_url
	# print base_url
	if base_url == 'StarPlus': fetchUrl = 'http://www.desirulez.me/forums/42-Star-Plus'
	elif base_url == 'AndTV': fetchUrl = 'http://www.desirulez.me/forums/3138-Tv'
	elif base_url == 'ZeeTV': fetchUrl = 'http://www.desirulez.me/forums/73-Zee-Tv'
	elif base_url == 'SonyTV': fetchUrl = 'http://www.desirulez.me/forums/63-Sony-Tv'
	elif base_url == 'StarBharat': fetchUrl = 'http://www.desirulez.me/forums/4856-Star-Bharat'
	elif base_url == 'ColorsTV': fetchUrl = 'http://www.desirulez.me/forums/176-Colors-Channel'
	elif base_url == 'SabTV': fetchUrl = 'http://www.desirulez.me/forums/254-Sab-TV'
	elif base_url == 'StarJalsha': fetchUrl = 'http://www.desirulez.me/forums/667-Star-Jalsha'
	elif base_url == 'SaharaOne': fetchUrl = 'http://www.desirulez.me/forums/134-Sahara-One'
	elif base_url == 'SonyPal': fetchUrl = 'http://www.desirulez.me/forums/2757-Sony-Pal'
	elif base_url == 'StarPravah': fetchUrl = 'http://www.desirulez.me/forums/1138-Star-Pravah'
	elif base_url == 'ZindagiTV': fetchUrl = 'http://www.desirulez.me/forums/2679-Zindagi-Tv'
	elif base_url == 'MTV': fetchUrl = 'http://www.desirulez.me/forums/339-MTV-IndiaPakistan'
	elif base_url == 'BindassTV': fetchUrl = 'http://www.desirulez.me/forums/504-Bindass-TV'
	elif base_url == 'ChannelV': fetchUrl = 'http://www.desirulez.me/forums/633-Channel-V'
	elif base_url == 'ARYDigital': fetchUrl = 'http://www.desirulez.me/forums/384-ARY-Digital'
	elif base_url == 'ColorsMarathi': fetchUrl = 'http://www.desirulez.me/forums/2369-Colors-Marathi'
	elif base_url == 'GEOTV': fetchUrl = 'http://www.desirulez.me/forums/413-Geo-Tv'
	elif base_url == 'HUMTV': fetchUrl = 'http://www.desirulez.me/forums/448-Hum-TV'
	elif base_url == 'MaaTV': fetchUrl = 'http://www.desirulez.me/forums/3165-Star-Maa'
	elif base_url == 'StarVijay': fetchUrl = 'http://www.desirulez.me/forums/1609-Star-Vijay'
	elif base_url == 'WWE': fetchUrl = 'http://www.desirulez.me/forums/1609-Star-Vijay'
	elif base_url == 'ZeeBangla': fetchUrl = 'http://www.desirulez.me/forums/676-Zee-Bangla'
	elif base_url == 'ZeeMarathi': fetchUrl = 'http://www.desirulez.me/forums/1299-Zee-Marathi'
	elif base_url == 'ZingTV': fetchUrl = 'http://www.desirulez.me/forums/2624-Zing-Tv'
	else: fetchUrl = 'NONE'
	# Get Shows Code 
	# 8/19/2018
	parentChannelShowArray = fetch_show_names(fetchUrl)
	zippedArray = parentChannelShowArray
	for (showName, showLink) in zippedArray:
		showURL = showLink + "=SNAME=" + showName
		showURL = build_url({'linkName': showURL})
		addDir('folder', 'show_to_episodes', showURL, showName, '', '')

############################################################################################################################################################
# Movie Getter Functions
############################################################################################################################################################

def load_movie_links():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]

	main_url = main_url.replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=").replace("%28", "(").replace("%29", ")")
	split_url = main_url.split("===")
	movieURL = split_url[0].replace("plugin://plugin.video.DTVShows/?linkName=","")
	movieName = split_url[1].replace("+", " ")

	r = requests.get(movieURL)
	data = r.text

	soup = BeautifulSoup(data)

	## Pass Episode Page Link to Aggregate Host Links

	mainArea = soup.findAll("a", {"rel":"nofollow"}, href=True)

	for link in mainArea:
	  if "Watch Online" in link.text:
			if "=" in link["href"]:
				sourceName = link.text.replace("Watch Online", "").strip()
				sourceLink = link["href"]
				sourceMediaId = sourceLink.split("=")[1]
				sourceDomain = re.search(".[a-zA-Z]/(.*?)\.php", sourceLink)
				if sourceDomain is None:
					pass
				else:
					sourceDomain = sourceDomain.group(1)
					movieDomainResolver(sourceDomain, sourceMediaId, sourceLink, sourceName)

def load_episodes():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	base_url = main_url.replace("plugin://plugin.video.DTVShows/?linkName=","").replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=").split("?s=")[0]
	showName = base_url.split("=SNAME=")[1].replace("+", " ")
	base_url = base_url.split("=SNAME=")[0]

	url = base_url
	r = requests.get(url)
	data = r.text

	soup = BeautifulSoup(data)

	## Pass Episode Page Link to Aggregate Host Links

	mainArea = soup.findAll("a", {"class":"title"}, href=True)

	print "------------------------"

	for link in mainArea:
			if "Watch Online" in link.text:
				episodeLink = link["href"]
				episodeName = link.text
				episodeName = re.search("([0-9]+[a-z]+ [A-Za-z]+)", episodeName).group(1)
				linksURL = build_url({'linkName': episodeLink + "===" + episodeName})
				getEpisodeSources(episodeName, episodeLink, linksURL)


## END EPISODE DEFINITIONS ##


mode = None

args = sys.argv[2]

if len(args) > 0:
	mode = args.split('mode=')
	mode = mode[1].split('&')
	mode = mode[0]


if mode == None             :       Main_Menu()
elif mode == 'channel_to_shows':	load_shows()
elif mode == 'show_to_episodes':	fetch_show_episodes()
elif mode == 'episode_to_links':    load_episode_links()
elif mode == 'resolve_link':        resolve_link()
elif mode == 'load_movies':         movie_menu()
elif mode == 'load_movie_links':    load_movie_links()

#################################
#   END OF DIRECTORY LISTINGS   #
#################################

xbmcplugin.endOfDirectory(addon_handle)