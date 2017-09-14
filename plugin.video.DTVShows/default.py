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

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

#################################
#  START OF DIRECTORY LISTINGS  #
#################################

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

## Get Online Data ##

def Main_Menu():
	channelsOnlineURL = "http://sonaled.com/dtvmc/channels/index.php"
	content = Open_URL(channelsOnlineURL)
	# xbmc.log('### CONTENTS: %s' % content)
	matches = re.compile('name="(.+?)"mode="(.+?)"icon="(.+?)"fanart="(.+?)"').findall(content)
	for item in matches:
		channel_name = 		item[0]
		dir_mode = 			item[1]
		channel_icon = 		item[2]
		channel_fanart = 	item[3]
		addDir('folder', 'load_channels', channel_name, channel_name, channel_icon, channel_fanart)

## Finish Online Data ##

## Channel Definitions ##

def load_shows():
	base_url = sys.argv[2]
	base_url = base_url.split('load_channels')[1].split('&', 2)
	base_url = base_url[1].replace('name=', '').replace('%20', '')
	channelName = base_url
	print base_url
	if base_url == 'StarPlus': fetchUrl = 'http://www.desirulez.me/forums/42-Star-Plus'
	elif base_url == 'AndTV': fetchUrl = 'http://www.desirulez.me/forums/3138-Tv'
	elif base_url == 'ZeeTV': fetchUrl = 'http://www.desirulez.me/forums/73-Zee-Tv'
	elif base_url == 'SonyTV': fetchUrl = 'http://www.desirulez.me/forums/63-Sony-Tv'
	elif base_url == 'LifeOK': fetchUrl = 'http://www.desirulez.me/forums/1375-Life-OK'
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
	r = requests.get(fetchUrl)
	data = r.text
	soup = BeautifulSoup(data)
	videoTitle = soup.findAll('h2', {'class':'forumtitle'})
	for row in videoTitle:
		showLink = row.find('a')
		finalShowLink = showLink.get('href')
		finalShowLink = finalShowLink.replace("forums/", "").replace("bfont-colorred", "").replace("fontb", "")
		show_name = finalShowLink.split("?s=", 1)[0].split("-", 1)[1].replace("-", " ").replace("bfont colorblue", "")
		showLink = showLink.get('href')
		showURL = "http://www.desirulez.me/" + showLink
		showURL = build_url({'linkName': showURL})
		addDir('folder', 'load_episodes', showURL, show_name, '', '')

## END CHANNEL DEFINITIONS ##

## Episode Definitions ##

def load_episodes():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	base_url = main_url.replace("plugin://plugin.video.DTVShows/?linkName=","").replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=").split("?s=")[0]
	showName = base_url.replace("http://www.desirulez.me/forums/", "").split("-", 1)[1].replace("-", " ")

	r = requests.get(base_url)
	data = r.text
	soup = BeautifulSoup(data)
	# for tr in soup.findAll('tr', {'class': ['odd', 'even']})
	videoTitle = soup.findAll('h3', {'class':'threadtitle'})
	for row in videoTitle:
		episodeLink = row.find('a').get('href')
		episodeName = row.find('a').text
		episodeName = episodeName.replace("Watch Online", "").replace(showName + " ", "")
		linksURL = build_url({'linkName': episodeLink + "===" + showName})
		addDir('folder', 'load_ep_links', linksURL, episodeName, '', '')

## END EPISODE DEFINITIONS ##

## START LINK DEFINITIONS ##

def load_ep_links():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	main_url = main_url.replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=")
	split_url = main_url.split("===")
	main_url = split_url[0]
	showName = split_url[1].replace("+", " ")
	episode_url = main_url.replace("plugin://plugin.video.DTVShows/?linkName=","").split("?s=")[0]
	episode_url = "http://www.desirulez.me/" + episode_url
	# print "############# " + episode_url
	r = requests.get(episode_url)
	data = r.text
	soup = BeautifulSoup(data)
	videoTitle = soup.findAll('blockquote', {"class": "postcontent restore "})
	for row in videoTitle:
		showLink = row.findAll('a')
		for link in showLink:
			linkName = link.text
			linkName = linkName.replace(showName, "").replace(" Watch Online Video-", "").replace(" Watch Online Video -", "").replace(" ", "-").rsplit("-", 2)
			linkName = linkName[1] + "-" + linkName[2]
			if linkName == "Watch-Online":
				linkName = "Full-Episode"
			else:
				linkName = linkName
			# print "############# " + linkName
			linkUrl = link.get('href')
			if "=" in linkUrl:
				linkID = linkUrl.split("=")[1]
			else:
				linkID = linkUrl
			if "vidwatch.php" in linkUrl:
				print "### VIDWATCH ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: VIDWATCH[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===VIDWATCH"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif "watchvideo.php" in linkUrl:
				print "### WATCHVIDEO ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===WATCHVIDEO"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif "vidoza.php" in linkUrl:
				print "### VIDOZA ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: VIDOZA[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===VIDOZA"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif "openload.php" in linkUrl:
				print "### OPENLOAD ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: OPENLOAD[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===OPENLOAD"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif "embedupload.com" in linkUrl:
				print "### EMBEDUPLOAD ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: EMBEDUPLOAD[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===EMBEDUPLOAD"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif len(linkID) == 7 and linkID.isdigit():
				print "### TUNEPK ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: TUNEPK[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===TUNEPK"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif len(linkID) == 19:
				print "### DAILYMOTION ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: DAILYMOTION[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===DAILYMOTION"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			elif len(linkID) == 7:
                if "reviewtv.in" in linkUrl:
                    print "### TVLOGY ### " + linkUrl
                    linkName = linkName + "[COLOR yellow]: TVLOGY[/COLOR]"
                    linkUrl = linkUrl + "===TVLOGY"
                    resultingLink = resolve_link(linkUrl)
                    addDir('', 'resolve_link', resultingLink, linkName, '', '')
                elif "tellysony.com" in linkUrl:
                    print "### TVLOGY ### " + linkUrl
                    linkName = linkName + "[COLOR yellow]: TVLOGY[/COLOR]"
                    linkUrl = linkUrl + "===TVLOGY"
                    resultingLink = resolve_link(linkUrl)
                    addDir('', 'resolve_link', resultingLink, linkName, '', '')
                else:
                	print "No Links Found"

			elif len(linkID) == 12:
				print "### SPEEDWATCH ### " + linkUrl
				linkName = linkName + "[COLOR yellow]: SPEEDWATCH[/COLOR]"
				linkUrl = build_url({'resolveLink': linkUrl + "===SPEEDWATCH"})
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

			else:
				print linkUrl
				linkName = "[COLOR yellow]"+linkName+"[/COLOR]"
				# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

def resolve_link(link_url):
	# main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	# main_url = main_url.replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=")
	# link_url = main_url.split("=", 1)[1].split("===")[0]
	link_host = link_url.split("===")[1]
	# print "########### " + link_url
	# print "########### " + link_host
	if link_host == "TVLOGY":
		videoId = link_url.split("=")[1]
		url = "http://tvlogy.to/watch.php?v=" + videoId
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)

		text_to_find = '.m3u8'

		soup = BeautifulSoup(data)

		for script in soup.findAll('script'):
		    parser = Parser()
		    tree = parser.parse(script.text)
		    for node in nodevisitor.visit(tree):
		        if isinstance(node, ast.Assign):
		            value = getattr(node.right, 'value', '')
		            if text_to_find in value:
		                value = value[1:-1]
		                return value
		                # print "##########" + value

## END LINK DEFINITIONS ##


mode = None

args = sys.argv[2]

if len(args) > 0:
	mode = args.split('mode=')
	mode = mode[1].split('&')
	mode = mode[0]


if mode == None 			:		Main_Menu()
elif mode == 'load_channels': 		load_shows()
elif mode == 'load_episodes': 		load_episodes()
elif mode == 'load_ep_links': 		load_ep_links()
elif mode == 'resolve_link':		resolve_link()

#################################
#   END OF DIRECTORY LISTINGS   #
#################################

xbmcplugin.endOfDirectory(addon_handle)