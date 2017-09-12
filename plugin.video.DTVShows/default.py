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

## Global Variables
player = xbmc.Player()

#################################
# START OF CHANNEL DEFINITIONS  #
#################################

# def lifeok_shows():
	# addDir('', '', part1, 'Zee TV 1', TaarakMehtaIcon, TaarakMehtaFanart)
	# addDir('', '', part1, 'Tarak Mehta Part 1', '', '')
	# addDir('', '', part2, 'Tarak Mehta Part 2', '', '')

# # def Zeetv_Shows():
# # 	addDir('', '', part1, 'Zee TV 1', TaarakMehtaIcon, TaarakMehtaFanart)
# # 	addDir('', '', part1, 'Tarak Mehta Part 1', TaarakMehtaIcon, TaarakMehtaFanart)

# def LifeOK_Shows():
# 	addDir()

#################################
#  END OF CHANNEL DEFINITIONS   #
#################################

# part1 = "http://proxy-029.ix7.dailymotion.com/sec(4921ea6750810a9ab09ccd63746fe8dc)/video/630/343/360343036_mp4_h264_aac_hd_1.m3u8"
# part2 = "http://proxy-043.ix7.dailymotion.com/sec(f85b67dc9c335ab7e432e5034122b90e)/video/370/343/360343073_mp4_h264_aac_hd_1.m3u8"

# TaarakMehtaIcon = "http://www.sabtv.com/media_content/2_3807.png"
# TaarakMehtaFanart = "http://resources.sonyliv.com/image/fetch/w_891,h_438,c_fill/http%3A%2F%2Fsetindiapd.brightcove.com.edgesuite.net%2F4338955589001%2F2017%2F03%2F4338955589001_5380327010001_4600324971001-th.jpg%3FpubId%3D4338955589001"

# SabTV_Icon = "https://pr24x7.files.wordpress.com/2012/05/sab-tv1.png"
# SabTV_Fanart = "https://bizasialivecom-6bb5.kxcdn.com/wp-content/uploads/2017/06/sonysabtv001-1000x500.jpg"

# ZeeTV_Icon = "https://vignette2.wikia.nocookie.net/logopedia/images/3/38/Zee_TV_2011.png/revision/latest?cb=20110926114755"
# ZeeTV_Fanart = "http://www.underconsideration.com/brandnew/archives/zee_tv_rainbow_of_hope.jpg"

# mainChannels = {'Life OK==http://2.bp.blogspot.com/-pGh5g602DVw/TwPCs5peSZI/AAAAAAAADo0/x4nNTexDIuA/s1600/LifeOK+logo+2011.jpg=fan=http://4.bp.blogspot.com/-WtDdmUWtnt0/T8b_uvL3NhI/AAAAAAAACcg/c1arDxM4zOg/s1600/life_ok_01.jpg': 'Chidiya Ghar==http://www.sabtv.com/media_content/2_3807.png'}

addon_handle = int(sys.argv[1])
#################################
#  START OF DIRECTORY LISTINGS  #
#################################

xbmcplugin.setContent(addon_handle, 'movies')

def addDir(dir_type, mode, url, name, iconimage, fanart):
	base_url = sys.argv[0]
	base_url += "?url="       +urllib.quote_plus(url)
	xbmc.log('#### BASE 1: %s' % base_url)
	base_url += "&mode="      +str(mode)
	xbmc.log('#### BASE 2: %s' % base_url)
	base_url += "&name="      +urllib.quote_plus(name)
	xbmc.log('#### BASE 3: %s' % base_url)
	base_url += "&iconimage=" +urllib.quote_plus(iconimage)
	xbmc.log('#### BASE 4: %s' % base_url)
	base_url += "&fanart="    +urllib.quote_plus(fanart)
	xbmc.log('#### BASE 5: %s' % base_url)

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
	xbmc.log('### CONTENTS: %s' % content)
	matches = re.compile('name="(.+?)"mode="(.+?)"icon="(.+?)"fanart="(.+?)"').findall(content)
	for item in matches:
		channel_name = 		item[0]
		dir_mode = 			item[1]
		channel_icon = 		item[2]
		channel_fanart = 	item[3]
		addDir('folder', 'load_channels', channel_name, channel_name, channel_icon, channel_fanart)

## Finish Online Data ##

## Channel Definitions ##

def load_channels():
	base_url = sys.argv[2]
	base_url = base_url.split('load_channels')[1].split('&', 2)
	base_url = base_url[1].replace('name=', '').replace('%20', '')
	channelName = base_url
	episodePerChannelURL = "http://sonaled.com/dtvmc/channels/getShows.php?channel="+channelName
	content = Open_URL(episodePerChannelURL)
	xbmc.log('### URGENT: %s' % base_url)
	matches = re.compile('channelname="(.+?)"showname="(.+?)"icon="(.+?)"fanart="(.+?)"').findall(content)
	for item in matches:
		channel_name = 		item[0]
		show_name = 		item[1]
		show_icon =			item[2]
		show_fanart =		item[3]
		addDir('folder', 'load_episodes', channel_name, show_name, show_icon, show_fanart)

## END CHANNEL DEFINITIONS ##

## Episode Definitions ##

def load_episodes():
	base_url = sys.argv[2]
	base_url = base_url.split('load_episodes')[1].split('&', 2)
	showName = base_url[1].replace('name=','')
	channelName = base_url[2].replace('url=','')
	getEpisodesUrl = "http://sonaled.com/dtvmc/channels/getEpisodes.php?channel="+channelName+"&show="+showName
	content = Open_URL(getEpisodesUrl)
	xbmc.log('### URGENT: %s' % getEpisodesUrl)
	matches = re.compile('channelname="(.+?)"showname="(.+?)"icon="(.+?)"fanart="(.+?)"epdate="(.+?)"eppart="(.+?)"eplink="(.+?)"').findall(content)
	for item in matches:
		channel_name = 		item[0]
		show_name = 		item[1]
		show_icon =			item[2]
		show_fanart =		item[3]
		ep_date =			item[4]
		ep_part =			"[COLOR=gold]"+item[5]+"[/COLOR]"
		ep_link =			item[6]
		ep_title = ep_date + "  " + ep_part
		addDir('', 'url', ep_link, ep_title, '', '')

## END EPISODE DEFINITIONS ##

mode = None

args = sys.argv[2]

if len(args) > 0:
	mode = args.split('mode=')
	mode = mode[1].split('&')
	mode = mode[0]

if mode == None 			:		Main_Menu()
elif mode == 'load_channels' : 		load_channels()
elif mode == 'load_episodes'	: 	load_episodes() 

#################################
#   END OF DIRECTORY LISTINGS   #
#################################
xbmcplugin.endOfDirectory(addon_handle)

# def addDir(mode, url, title, icon):
# 	li = xbmcgui.ListItem(title, iconImage=icon)
# 	xbmcplugin.addDirectoryItem(handle=addon_handle, url=part1, listitem=li)