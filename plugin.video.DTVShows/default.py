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

def determine_iframe_source(url):
	print "Determining IFRAME Source ......."
	regex = r"file: \".*.mp4\""
	r = requests.get(url)
	results = []
	for line in r.text.splitlines():
		if text_to_find in line:
			iframe_source = line.split("\"http")
			iframe_source = iframe_source[1].replace("://", "http://").split("ml\"")
			iframe_source = iframe_source[0].replace(".ht", ".html")
			results.append(iframe_source)
		else:
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				print "########### " + finalValue
				return finalValue
			else:
				pass
		# if re.findall(regex, line):
		#     line = 'http:' + line[9:-2]
		#     results.append(str(line))
	if not results:
		print "Array Empty"
	else:
		print results[0]
		return results[0]

text_to_find_parsing = "sources:"

def find_jw_source(url, vidID):
	print url + " " + vidID
	regex = r"sources: \".*.mp4\""
	r = requests.get(url)
	results = []
	for line in r.text.splitlines():
		if text_to_find_parsing in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			results.append(line)
			# print len(results)
		else:
			pass
	if len(results) == 0:
		#Vidwatch
		return scrape_vidwatch(vidID)
	else:
		# print "STREAMING LINK -> "+ str(results[0])
		return str(results[0])

def scrape_watchvideo(vidID):
	try:
		#WatchVideo
		url = "https://watchvideo.us/embed-"+vidID+"-540x304.html"
		return find_jw_source(url, vidID)
	except Exception as e:
		raise
	else:
		pass

def scrape_vidwatch(vidID):
	try:
		#VidWatch
		url = "https://vidwatch.me/embed-"+vidID+".html"
		return find_jw_source(url, vidID)
	except Exception as e:
		raise
	else:
		pass

#### END 8/12/2018

def scrape_watchvideo_movies(url):
	vidID = url.split("?url=")[1]
	vidID = vidID.split("===")[0]
	print vidID
	newUrl = "https://watchvideo.us/embed-"+vidID+"-540x304.html"
	print newUrl
	regex = r"sources: \".*.mp4\""
	r = requests.get(newUrl)
	results = []
	for line in r.text.splitlines():
		if "sources:" in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			results.append(line)
			# print len(results)
		else:
			pass
	if len(results) == 0:
		#Vidwatch
		pass
	else:
		print results[0]
		return results[0]

def resolveVidoza(linkUrl):
	vidozaID = linkUrl.split("url=")[1]
	vidozaLink = "http://www.vidoza.net/embed-" + vidozaID + ".html"

	r = requests.get(vidozaLink, verify=False)
	# data = r.text
	# soup = BeautifulSoup(data)
	# videoDirectLink = soup.findAll('source', {'type':'video/mp4'})
	# print len(videoDirectLink)

def parseWatchVideo(data):

	text_to_find = 'm3u8|master'

	soup = BeautifulSoup(data)

	pageScripts = soup.findAll('script')

	resultingScript = []

	for script in pageScripts:
		searchableString = str(script)
		if "m3u8|master" in searchableString:
			print "SUCCESS!! ####"
			resultingScript.append(searchableString)
		else:
			print "--------------"

	paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(resultingScript[0])

	if len(paramSet) > 0:
		video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
		# print video_info_link
		img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
		value = img_data[0]
		# print value
		value = value.split(",")
		finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
		# print "########### " + finalValue
		return finalValue
	else:
		print "None Found Here Buddy"

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

	r = requests.get(episode_url)
	linksArray = []
	for line in r.text.splitlines():
		if "<a rel=\"nofollow\"" in line and "style=\"" not in line and "<li" not in line and "twitter" not in line and "<p" not in line and "Powered" not in line and "dragonbyte" not in line:
			line = line.strip()
			line = line.replace("<a rel=\"nofollow\" href=\"", "")
			line = line.replace("\" target=\"_blank\">", "- ")
			line = line.replace("</a><br />", "")
			line = line.split("- ")

			if len(line) == 2:
				ep_sourceLink = line[0]
				ep_sourcePart = "Full Episode"
			else:
				ep_sourceLink = line[0]
				ep_sourcePart = line[2]

			arrayValue = ep_sourceLink + " -- " + ep_sourcePart

			linksArray.append(arrayValue)
		else:
			pass

	## Split out Each Array

	for arrayValue in linksArray:
		## PARSE WATCHVIDEO WITH 'WATCHVIDEO' IN LINK
		if "watchvideo.php" in arrayValue:
			fetch_obvious_watchvideo(arrayValue)
		elif "vidwatch.php" in arrayValue:
			fetch_obvious_vidwatch(arrayValue)
		elif "vidoza" in arrayValue:
			fetch_obvious_vidoza(arrayValue)
		elif "speed" in arrayValue:
			fetch_obvious_speedwatch(arrayValue)
		elif "http://www.desirulez.net/register.php" in arrayValue:
			print "Bypassing Registration Link"
			pass
		else:
			## PARSING HIDDEN LINKS
			## MUST DETERMINE ID & PARSE FURTHER

			## STEPS TO GET ID VALUE
			try:
				arrayValueID = arrayValue.split("=")[1].split(" -- ")[0]
			except:
				pass

			## WATCHVIDEO & VIDWATCH IDs ARE 12 IN COUNT
			## SEPARATE 12 & NON-12 IDs

			if len(arrayValueID) == 12:

				# PARSE THE DIFFERENT IDs & DETERMINE WHICH IS WATCHVIDEO & VIDWATCH
				## THERE ARE 3 DIFFERENT SPLITS --> '?sim=' | '?si=' | '?id='
				
				## NEED TO SPLIT ARRAYVALUE INTO URL & PART NUMBER
				parseableLink = arrayValue.split(" -- ")[0]

				## ITERATE THROUGH SPLITS
				if "?si=" in parseableLink:
					fetch_hidden_watchvideo(arrayValue)
				elif "?sim=" in parseableLink:
					fetch_hidden_speedwatch(arrayValue)
				else:
					pass

				# print "ARRAY VALUE --> " + arrayValue
				# print "ARRAY VALUE ID --> " + arrayValueID
			else:
				pass

			# print "ARRAY VALUE --> " + arrayValue
			# print "ARRAY VALUE ID --> " + arrayValueID
			pass

##########################################################################################################################################################
# LATEST FUNCTIONS AS OF 08/19/2018
# SOURCE PARSING BY INDIVIDUAL WEBSITE
##########################################################################################################################################################
### HIDDEN PARSERS BELOW
##########################################################################################################################################################

def fetch_hidden_watchvideo(value):
	# NEED TO SPLIT INCOMING VALUE
	value = value.split(" -- ")
	sourceLink = value[0]
	sourcePart = value[1]

	videoID = sourceLink.split("=")[1]

	print videoID

	embeddedLink = "http://watchvideo.us/embed-"+videoID+"-540x304.html"

	regex = r"sources: \".*.mp4\""
	r = requests.get(embeddedLink)
	results = []
	for line in r.text.splitlines():
		if "sources:" in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			print line
			results.append(line)
			# print len(results)
		elif "File was deleted" in line:
			print "SOURCE FILE DELETED"
		else:
			pass
			
	if len(results) == 0:

		## NEED TO FETCH PACKED FUNCTION IF NO LINKS FOUND IN EXPLICIT WATCHVIDEO
		## IF PACKED FUNCTION RETURNS FALSE, THEN OUTPUT NO LINKS FOUND
		### STEP 1 = SEE IF THE URL CONTAINS A PACKED FUNCTION OR NOT
		for line in r.text.splitlines():
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				print "########### " + finalValue
				streamingName = sourcePart + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
				addDir('', '', finalValue, streamingName, '', '')
				return finalValue
			else:
				pass
				
		addDir('', '', '', "[COLOR red]NO LINKS FOUND[/COLOR]", '', '')
	else:
		streamingLink = results[0]
		streamingName = sourcePart + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
		addDir('', '', streamingLink, streamingName, '', '')


def fetch_hidden_speedwatch(value):
	# NEED TO SPLIT INCOMING VALUE
	value = value.split(" -- ")
	sourceLink = value[0]
	sourcePart = value[1]

	videoID = sourceLink.split("=")[1]

	print videoID + " :SPEEDWATCH"

	embeddedLink = "http://speedwatch.us/embed-"+videoID+"-595x430.html"

	regex = r"sources: \".*.mp4\""
	r = requests.get(embeddedLink)
	results = []
	for line in r.text.splitlines():
		if "sources:" in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			print line
			results.append(line)
			# print len(results)
		elif "File was deleted" in line:
			print "SOURCE FILE DELETED"
		else:
			pass
			
	if len(results) == 0:

		## NEED TO FETCH PACKED FUNCTION IF NO LINKS FOUND IN EXPLICIT WATCHVIDEO
		## IF PACKED FUNCTION RETURNS FALSE, THEN OUTPUT NO LINKS FOUND
		### STEP 1 = SEE IF THE URL CONTAINS A PACKED FUNCTION OR NOT
		for line in r.text.splitlines():
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				print "########### " + finalValue
				streamingName = sourcePart + "[COLOR yellow]: SPEEDWATCH[/COLOR]"
				addDir('', '', finalValue, streamingName, '', '')
				return finalValue
			else:
				pass
				
		addDir('', '', '', "[COLOR red]NO LINKS FOUND[/COLOR]", '', '')
	else:
		streamingLink = results[0]
		streamingName = sourcePart + "[COLOR yellow]: SPEEDWATCH[/COLOR]"
		addDir('', '', streamingLink, streamingName, '', '')

##########################################################################################################################################################
### OBVIOUS PARSERS BELOW
##########################################################################################################################################################

def fetch_obvious_watchvideo(value):
	print value
	# NEED TO SPLIT INCOMING VALUE
	value = value.split(" -- ")
	sourceLink = value[0]
	sourcePart = value[1]
	
	# if "Part" not in value[1]:
	#   sourcePart = "Full Episode"
	# else:
	#   sourcePart = value[1]

	videoID = sourceLink.split("?id=")[1]

	embeddedLink = "http://watchvideo.us/embed-"+videoID+"-540x304.html"

	regex = r"sources: \".*.mp4\""
	r = requests.get(embeddedLink)
	results = []
	for line in r.text.splitlines():
		if "sources:" in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			# print line
			results.append(line)
			# print len(results)
		elif "File was deleted" in line:
			print "SOURCE FILE DELETED"
		else:
			pass
			
	if len(results) == 0:

		## NEED TO FETCH PACKED FUNCTION IF NO LINKS FOUND IN EXPLICIT WATCHVIDEO
		## IF PACKED FUNCTION RETURNS FALSE, THEN OUTPUT NO LINKS FOUND
		### STEP 1 = SEE IF THE URL CONTAINS A PACKED FUNCTION OR NOT
		for line in r.text.splitlines():
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				print "########### " + finalValue
				streamingName = sourcePart + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
				addDir('', '', finalValue, streamingName, '', '')
				return finalValue
			else:
				pass
				
		addDir('', '', '', "[COLOR red]NO LINKS FOUND[/COLOR]", '', '')
	else:
		streamingLink = results[0]
		streamingName = sourcePart + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
		addDir('', '', streamingLink, streamingName, '', '')


def fetch_obvious_vidwatch(value):
	# NEED TO SPLIT INCOMING VALUE
	value = value.split(" -- ")
	sourceLink = value[0]
	sourcePart = value[1]

	# if "Part" not in value[1]:
	#   sourcePart = "Full Episode"
	# else:
	#   sourcePart = value[1]

	print sourceLink

	videoID = sourceLink.split("?id=")[1]

	embeddedLink = "http://vidwatch.me/embed-"+videoID+"-540x304.html"

	regex = r"sources: \".*.mp4\""
	r = requests.get(embeddedLink)
	results = []
	for line in r.text.splitlines():
		if "sources:" in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			# print line
			results.append(line)
			# print len(results)
		elif "File was deleted" in line:
			print "SOURCE FILE DELETED"
		else:
			pass
			
	if len(results) == 0:

		## NEED TO FETCH PACKED FUNCTION IF NO LINKS FOUND IN EXPLICIT VIDWATCH
		## IF PACKED FUNCTION RETURNS FALSE, THEN OUTPUT NO LINKS FOUND
		### STEP 1 = SEE IF THE URL CONTAINS A PACKED FUNCTION OR NOT
		for line in r.text.splitlines():
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				print "########### " + finalValue
				streamingName = sourcePart + "[COLOR yellow]: VIDWATCH[/COLOR]"
				addDir('', '', finalValue, streamingName, '', '')
				return finalValue
			else:
				pass

		addDir('', '', '', "[COLOR red]NO LINKS FOUND[/COLOR]", '', '')
	else:
		streamingLink = results[0]
		streamingName = sourcePart + "[COLOR yellow]: VIDWATCH[/COLOR]"
		addDir('', '', streamingLink, streamingName, '', '')


def fetch_obvious_vidoza(value):
	# NEED TO SPLIT INCOMING VALUE
	value = value.split(" -- ")
	sourceLink = value[0]
	sourcePart = value[1]

	# if "Part" not in value[1]:
	#   sourcePart = "Full Episode"
	# else:
	#   sourcePart = value[1]

	print sourceLink

	videoID = sourceLink.split("?id=")[1]

	embeddedLink = "http://vidoza.net/embed-"+videoID+".html"

	regex = r"sources: \".*.mp4\""
	r = requests.get(embeddedLink)
	results = []
	for line in r.text.splitlines():
		if "sourcesCode:" in line:
			line = line.strip().replace("sourcesCode: [{ src: ","").split(",")[0].replace("\"","")
			results.append(line)
		elif "File was deleted" in line:
			print "SOURCE FILE DELETED"
		else:
			pass
			
	if len(results) == 0:

		## NEED TO FETCH PACKED FUNCTION IF NO LINKS FOUND IN EXPLICIT VIDWATCH
		## IF PACKED FUNCTION RETURNS FALSE, THEN OUTPUT NO LINKS FOUND
		### STEP 1 = SEE IF THE URL CONTAINS A PACKED FUNCTION OR NOT
		for line in r.text.splitlines():
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				print "########### " + finalValue
				streamingName = sourcePart + "[COLOR green]: VIDOZA[/COLOR]"
				addDir('', '', finalValue, streamingName, '', '')
				return finalValue
			else:
				pass

		addDir('', '', '', "[COLOR red]NO LINKS FOUND[/COLOR]", '', '')
	else:
		streamingLink = results[0]
		streamingName = sourcePart + "[COLOR green]: VIDOZA[/COLOR]"
		addDir('', '', streamingLink, streamingName, '', '')

def fetch_obvious_speedwatch(value):
	print value
	# NEED TO SPLIT INCOMING VALUE
	value = value.split(" -- ")
	sourceLink = value[0]
	sourcePart = value[1]
	
	#REMOVE MUMBLE SCRIPTS
	sourceLink = sourceLink.replace("<font size=\"4\"><b>", "")
	print sourceLink + "********"
	# if "Part" not in value[1]:
	#   sourcePart = "Full Episode"
	# else:
	#   sourcePart = value[1]

	# videoID = sourceLink.split("?url=")[1]

	try:
			videoID = sourceLink.split("?url=")[1]
	except:
			videoID = sourceLink.split("?id=")[1]

	embeddedLink = "http://speedwatch.us/embed-"+videoID+"-520x400.html"

	regex = r"sources: \".*.mp4\""
	r = requests.get(embeddedLink)
	results = []
	for line in r.text.splitlines():
		if "sources:" in line:
			line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
			# line = rtrim(line, ',')
			line = line[0].replace("{file:", "").replace("\"","")
			# print line
			results.append(line)
			# print len(results)
		elif "File was deleted" in line:
			print "SOURCE FILE DELETED"
		else:
			pass
			
	if len(results) == 0:

		## NEED TO FETCH PACKED FUNCTION IF NO LINKS FOUND IN EXPLICIT WATCHVIDEO
		## IF PACKED FUNCTION RETURNS FALSE, THEN OUTPUT NO LINKS FOUND
		### STEP 1 = SEE IF THE URL CONTAINS A PACKED FUNCTION OR NOT
		for line in r.text.splitlines():
			if "eval(function(p,a,c,k,e,d)" in line:
				print "Evaluating PACKED function ..."
				line = line.replace("<script type='text/javascript'>", "")
				paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(line)
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				#print value
				value = value.split(",")
				try:
						finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				except:
						pass
				try:
						higherQualityValue = value[0] + value[2] + "/index-v1-a1.m3u8"
				except:
						pass
				print "########### " + finalValue
				streamingName = sourcePart + "[COLOR yellow]: SPEEDWATCH[/COLOR]"
				HighStreamingName = sourcePart + "[COLOR red]: SPEEDWATCH HD[/COLOR]"
				addDir('', '', finalValue, streamingName, '', '')
				addDir('', '', higherQualityValue, HighStreamingName, '', '')
				return finalValue
			else:
				pass
				
		addDir('', '', '', "[COLOR red]NO LINKS FOUND[/COLOR]", '', '')
	else:
		streamingLink = results[0]
		streamingName = sourcePart + "[COLOR yellow]: SPEEDWATCH[/COLOR]"
		addDir('', '', streamingLink, streamingName, '', '')



##########################################################################################################################################################
# LATEST FUNCTIONS AS OF 08/19/2018
# PULLS LINES OF HTML & PARSES EACH INSTEAD OF ITERATING OVER ENTIRE HTML CODE FOR EACH LINE
##########################################################################################################################################################

def fetch_show_names(url):
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

	r = requests.get(base_url)
	episodeNames = []
	linksArray = []
	for line in r.text.splitlines():
		if "<a class=\"title\"" in line:
			line = line.strip()
			line = line.replace("<a class=\"title\" href=\"", "")
			dateLink = line.split("?s=")[0]
			print "LINK:" + dateLink
			linksArray.append(dateLink)
			dateTitle = line.split("?s=")[1].split("\">")[1].replace("</a>", "")
			#PARSE TITLES TO REMOVE EXCESS VERBAGE
			dateTitle = dateTitle.replace("Watch Online", "").replace("Watch Onlin","").replace(",","").replace(showName + " ", "").encode('ascii', 'ignore').decode('ascii').replace("by Ary Digital -","")
			dateTitle = dateTitle.replace("&amp;", "&")
			#END PARSING & RETURN FINAL CLEANED UP TITLE
			print "TITLE:" + dateTitle
			episodeNames.append(dateTitle)
		else:
			pass

	parentChannelShowArray = zip(episodeNames, linksArray)
	zippedArray = parentChannelShowArray
	for (episodeName, episodeLink) in zippedArray:
		linksURL = build_url({'linkName': episodeLink + "===" + episodeName})
		addDir('folder', 'load_ep_links', linksURL, episodeName, '', '')

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
		addDir('folder', 'load_channels', channel_name, channel_name, channel_icon, channel_fanart)

def movie_menu():
	movieListURL = "http://www.desirulez.me/forums/20-Latest-Exclusive-Movie-HQ"
	## Get Movie Links & Names
	r = requests.get(movieListURL)
	data = r.text
	soup = BeautifulSoup(data)
	videoTitle = soup.findAll('h3', {'class':'threadtitle'})
	for row in videoTitle:
		showLink = row.find('a', {'class':'title'})
		movieLink = showLink.get('href')
		# print movieLink
		movieLink = movieLink.rsplit('?')[0]

		movieName = showLink.text
		movieName = movieName.encode('ascii', 'ignore').decode('ascii').replace("'","")
		movieName = movieName.replace(" Watch Online / Download", "").replace(" Watch Online / Download (Lollywood Movie)","").replace(" Watch Online / Download - DVD RIP","").replace(" - DVD RIP", "").replace(" (Lollywood Movie)","")
		linksURL = build_url({'linkName': movieLink + "===" + movieName})
		addDir('folder', 'load_movie_links', linksURL, movieName, '', '')

		# finalShowLink = finalShowLink.replace("forums/", "").replace("bfont-colorred", "").replace("fontb", "")
		# show_name = finalShowLink.split("?s=", 1)[0].split("-", 1)[1].replace("-", " ").replace("bfont colorblue", "").replace("'","")
		# showLink = showLink.get('href')
		# showURL = "http://www.desirulez.me/" + showLink
		# showURL = build_url({'linkName': showURL})
		# addDir('folder', 'load_episodes', showURL, show_name, '', '')

##########################################################################################################################################################
# LOAD SHOWS ONCE CHANNEL IS SELECTED 
##########################################################################################################################################################

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
		addDir('folder', 'load_episodes', showURL, showName, '', '')
	# r = requests.get(fetchUrl)
	# data = r.text
	# soup = BeautifulSoup(data)
	# videoTitle = soup.findAll('h2', {'class':'forumtitle'})
	# for row in videoTitle:
	#   showLink = row.find('a')
	#   finalShowLink = showLink.get('href')
	#   finalShowLink = finalShowLink.replace("forums/", "").replace("bfont-colorred", "").replace("fontb", "")
	#   # show_name = finalShowLink.split("?s=", 1)[0].split("-", 1)[1].replace("-", " ").replace("bfont colorblue", "").replace("'","")
	#   # show_name = finalShowLink.split("?s=", 1)[0]
	#   show_name = row.text.encode('ascii', 'ignore').decode('ascii')
	#   showLink = showLink.get('href')
		# showURL = showLink + "=SNAME=" + show_name
		# showURL = build_url({'linkName': showURL})
		# addDir('folder', 'load_episodes', showURL, show_name, '', '')

############################################################################################################################################################

def load_movie_links():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	print main_url
	main_url = main_url.replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=").replace("%28", "(").replace("%29", ")")
	split_url = main_url.split("===")
	movieURL = split_url[0].replace("plugin://plugin.video.DTVShows/?linkName=","")
	movieName = split_url[1].replace("+", " ")
	print "### " + movieName
	print "### " + movieURL
	r = requests.get(movieURL)
	data = r.text
	soup = BeautifulSoup(data)
	videoTitle = soup.findAll('blockquote', {"class": "postcontent restore "})
	for row in videoTitle:
		showLink = row.findAll('a')
		for link in showLink:
			linkName = link.text
			linkName = linkName.replace(" Watch Online Pre Dvd Rip", "").replace(movieName, "").replace(" - ", "")
			
			linkUrl = link.get("href")

			# ## Vidoza Parse
			# if "vidoza.php" in linkUrl:
			#   resolveVidoza(linkUrl)
			# else:
			#   pass

			if "watchvideo.php" in linkUrl:
				print "### WATCHVIDEO ### " + linkUrl
				linkName2 = linkName + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
				print "#### - " + linkName
				#linkUrl = linkUrl + "===WATCHVIDEO"
				linkUrl = linkUrl.replace("?url","?id")
				passAlongURL = linkUrl + " -- " + linkName
				fetch_obvious_watchvideo(passAlongURL)
				#resultingLink = scrape_watchvideo_movies(linkUrl)
				#print resultingLink
				#if resultingLink == 'None':
				#       print "None"
				#elif resultingLink == 'No Links Found':
				#       print "None"
				#else:
				#       addDir('', '', resultingLink, linkName, '', '')
			else:
				print linkUrl
				print "######"


## End MOVIE Definitions ##

def load_episodes():
	main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	base_url = main_url.replace("plugin://plugin.video.DTVShows/?linkName=","").replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=").split("?s=")[0]
	showName = base_url.split("=SNAME=")[1].replace("+", " ")
	base_url = base_url.split("=SNAME=")[0]
	print base_url
	# print showName + " ####"

	r = requests.get(base_url)
	data = r.text
	soup = BeautifulSoup(data)
	# for tr in soup.findAll('tr', {'class': ['odd', 'even']})
	videoTitle = soup.findAll('h3', {'class':'threadtitle'})
	for row in videoTitle:
		episodeLink = row.find('a').get('href')
		episodeName = row.find('a').text
		episodeName = episodeName.replace("Watch Online", "").replace("Watch Onlin","").replace(",","").replace(showName + " ", "").encode('ascii', 'ignore').decode('ascii').replace("by Ary Digital -","")
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
	print episode_url
	# episode_url = "http://www.desirulez.me/" + episode_url
	# print "############# " + episode_url
	r = requests.get(episode_url)
	data = r.text
	soup = BeautifulSoup(data)
	videoTitle = soup.findAll('blockquote', {"class": "postcontent restore "})
	for row in videoTitle:
		youtubeLink = row.findAll({'iframe':'src'})
		for link in youtubeLink:
			print "############"
			link_clean = re.compile('src="(.+?)"').findall(str(link))
			for item in link_clean:
				finalLink = item.replace("//www.youtube.com/embed/", "").replace("?wmode=opaque", "")
				print finalLink
				url = "plugin://plugin.video.youtube/play/?video_id=" + finalLink
				li = xbmcgui.ListItem('YouTube Link', iconImage='http://i.ytimg.com/vi/'+finalLink+'/maxresdefault.jpg')
				li.setProperty('IsPlayable', 'true')
				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
		showLink = row.findAll('a')
		for link in showLink:
			print "############"
			# print link
			if "http://www.desirulez.us" in link.get('href'):
				print "No LINK"
			elif "http://www.desirulez.net/register.php" in link.get('href'):
				print "No LINk"
			elif "http://www.*************" in link.get('href'):
				print "No LINk"
			else:
				linkName = link.text
				linkName = linkName.replace(showName, "").replace(" Watch Online Video-", "").replace(" Watch Online Video -", "").replace(" ", "-")
				linkName = linkName.rsplit("-", 2)
				# print linkName
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
					pass
					# print "### VIDWATCH ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: VIDWATCH[/COLOR]"
					# linkUrl = build_url({'resolveLink': linkUrl + "===VIDWATCH"})
					# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

				## WATCH --------

				# elif "watchvideo.php" in linkUrl:
				#   print "### WATCHVIDEO ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
					# linkUrl = linkUrl + "===WATCHVIDEO"
					# resultingLink = resolve_link(linkUrl)
					# if resultingLink == 'None':
					#   print "None"
					# elif resultingLink == 'No Links Found':
					#   print "None"
					# else:
					#   addDir('', 'resolve_link', resultingLink, linkName, '', '')


				elif len(linkID) == 12 and "?si=" in linkUrl or "?sim=" in linkUrl:
					print linkUrl
					iframeLink = determine_iframe_source(linkUrl)
					print iframeLink
					if "watchvideo" in iframeLink:
						print "** WATCHVIDEO **"
						regex = r"sources: \".*.mp4\""
						r = requests.get(iframeLink)
						results = []
						for line in r.text.splitlines():
							if text_to_find_parsing in line:
								print line
								line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
								# line = rtrim(line, ',')
								line = line[0].replace("{file:", "").replace("\"","")
								results.append(line)
								watchvideoLink = results[0]
								linkName = linkName + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
								addDir('', '', watchvideoLink, linkName, '', '')
								# print len(results)
							else:
								pass
					# if "vidwatch" in iframeLink:
					#   print "** VIDWATCH **"
					#   regex = r"sources: \".*.mp4\""
					#   r = requests.get(iframeLink)
					#   results = []
					#   for line in r.text.splitlines():
					#       if text_to_find_parsing in line:
					#           print line
					#           line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
					#           # line = rtrim(line, ',')
					#           line = line[0].replace("{file:", "").replace("\"","")
					#           results.append(line)
					#           watchvideoLink = results[0]
					#           linkName = linkName + "[COLOR yellow]: VIDWATCH[/COLOR]"
					#           addDir('', '', watchvideoLink, linkName, '', '')
					#           # print len(results)
					#       else:
					#           pass

					elif "speedwatch" in iframeLink:
						print "** SPEEDWATCH **"
						regex = r"sources: \".*.mp4\""
						r = requests.get(iframeLink)
						results = []
						for line in r.text.splitlines():
							if text_to_find_parsing in line:
								# print line
								line = line.strip().replace("sources: ", "").replace("[","").replace("],","").split("},{")
								# line = rtrim(line, ',')
								line = line[0].replace("{file:", "").replace("\"","")
								results.append(line)
								watchvideoLink = results[0]
								print watchvideoLink
								linkName = linkName + "[COLOR yellow]: SPEEDWATCH[/COLOR]"
								addDir('', '', watchvideoLink, linkName, '', '')
								# print len(results)
							else:
								print resolve_packed_function(iframeLink)
					else:
						pass
					# print linkID
					# resultingLink = scrape_watchvideo(linkID)
					# linkName = linkName + "[COLOR yellow]: WV | VW[/COLOR]"
					# print "RESULTING LINK -> "+ str(resultingLink)
					# addDir('', '', resultingLink, linkName, '', '')


				elif "vidoza.php" in linkUrl:
					pass
					# print "### VIDOZA ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: VIDOZA[/COLOR]"
					# linkUrl = linkUrl + "===VIDOZA"
					# resultingLink = resolve_link(linkUrl)
					# addDir('', 'resolve_link', resultingLink, linkName, '', '')

				elif "openload.php" in linkUrl:
					pass
					# print "### OPENLOAD ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: OPENLOAD[/COLOR]"
					# linkUrl = build_url({'resolveLink': linkUrl + "===OPENLOAD"})
					# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

				elif "embedupload.com" in linkUrl:
					pass
					# print "### EMBEDUPLOAD ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: EMBEDUPLOAD[/COLOR]"
					# linkUrl = build_url({'resolveLink': linkUrl + "===EMBEDUPLOAD"})
					# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

				elif len(linkID) == 7 and linkID.isdigit():
					pass
					# print "### TUNEPK ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: TUNEPK[/COLOR]"
					# linkUrl = build_url({'resolveLink': linkUrl + "===TUNEPK"})
					# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

				elif len(linkID) == 19:
					pass
					# print "### DAILYMOTION ### " + linkUrl
					# linkName = linkName + "[COLOR yellow]: DAILYMOTION[/COLOR]"
					# linkUrl = build_url({'resolveLink': linkUrl + "===DAILYMOTION"})
					# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

				elif len(linkID) == 7:
					pass
					# if "reviewtv.in" in linkUrl:
					#   # print "### TVLOGY ### " + linkUrl
					#   linkName = linkName + "[COLOR yellow]: TVLOGY[/COLOR]"
					#   linkUrl = linkUrl + "===TVLOGY"
					#   resultingLink = resolve_link(linkUrl)
					#   addDir('', 'resolve_link', resultingLink, linkName, '', '')
					# elif "tellysony.com" in linkUrl:
					#   # print "### TVLOGY ### " + linkUrl
					#   linkName = linkName + "[COLOR yellow]: TVLOGY[/COLOR]"
					#   linkUrl = linkUrl + "===TVLOGY"
					#   resultingLink = resolve_link(linkUrl)
					#   addDir('', 'resolve_link', resultingLink, linkName, '', '')
					# else:
					#   print "No Links Found"

				# elif len(linkID) == 12:
				#   print "### UNFILTERED ### " + linkID
				#   # resolve_unfiltered(linkID)
				#   # + linkUrl
				#   # resolve_unfiltered(linkID)
				#   resultingLink = resolve_unfiltered(linkID)
				#   playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
				#   # print resultingLink
				#   if resultingLink == "#### NO FILE":
				#       print "## NOTHING"
				#   else:
				#       print "#########" + linkName
				#       linkName = linkName + "[COLOR yellow]: WATCHVIDEO[/COLOR]"
				#       print resultingLink
				#       addDir('', 'resolve_link', resultingLink, linkName, '', '')
				#       if 'Part-1' in linkName:
				#           video = resultingLink
				#           listitem = xbmcgui.ListItem(linkName)
				#           listitem.setInfo('video', {'Title': linkName})
				#           playlist.add(url=video, listitem=listitem)
				#           # addDir('', 'resolve_link', resultingLink, 'Part 1', '', '')
				#       else:
				#           video = resultingLink
				#           listitem = xbmcgui.ListItem(linkName)
				#           listitem.setInfo('video', {'Title': linkName})
				#           playlist.add(url=video, listitem=listitem)
				#           print playlist
				#           # addDir('', 'resolve_link', '', 'Continuous Play[COLOR yellow]: WATCHVIDEO[/COLOR]', '', '')

				else:
					pass
					# print linkUrl
					# linkName = "[COLOR yellow]"+linkName+"[/COLOR]"
					# addDir('folder', 'resolve_link', linkUrl, linkName, '', '')

def resolve_unfiltered(linkID):
	# link_host = link_url.split("===")[1]
	url = "http://watchvideo18.us/embed-" + linkID + "-540x304.html"
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	text_to_find = 'File was deleted'

	if text_to_find in soup:
		return "#### NO FILE"
		print "#### NO FILE"
	else:
		print "############ FILE FOUND"
		return resolve_watchvideo(linkID)


def resolve_packed_function(url):
	# url = "http://watchvideo18.us/embed-" + linkID + "-540x304.html"
	print url
	try:
		# print "################ " + url
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)

		# parseWatchVideo(data)

		text_to_find = 'm3u8|master'

		soup = BeautifulSoup(data)

		pageScripts = soup.findAll('script')

		resultingScript = []

		for script in pageScripts:
			searchableString = str(script)
			if "m3u8|master" in searchableString:
				print "SUCCESS!! ####"
				resultingScript.append(searchableString)
			else:
				print "--------------"

		paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(resultingScript[0])

		if len(paramSet) > 0:
			video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
			# print video_info_link
			img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
			value = img_data[0]
			# print value
			value = value.split(",")
			finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
			# print "########### " + finalValue
			return finalValue
		else:
			print "None Found Here Buddy"


		# for script in pageScripts:
		#   print script
		#   print "---------"

		# if (len(pageScripts) >= 1):
		#   for script in [pageScripts][12]:
		#       paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(script)
		#       if len(paramSet) > 0:
		#           video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
		#           # print video_info_link
		#           img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
		#           value = img_data[0]
		#           # print value
		#           value = value.split(",")
		#           finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
		#           # print "########### " + finalValue
		#           return finalValue
		#       else:
		#           print 'Nooone'
		# else:
		#   print "No Links Found"
	except:
		print "An Error Occurred"


def resolve_watchvideo(linkID):
	url = "http://watchvideo18.us/embed-" + linkID + "-540x304.html"
	# print url
	try:
		# print "################ " + url
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)

		# parseWatchVideo(data)

		text_to_find = 'm3u8|master'

		soup = BeautifulSoup(data)

		pageScripts = soup.findAll('script')

		resultingScript = []

		for script in pageScripts:
			searchableString = str(script)
			if "m3u8|master" in searchableString:
				print "SUCCESS!! ####"
				resultingScript.append(searchableString)
			else:
				print "--------------"

		paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(resultingScript[0])

		if len(paramSet) > 0:
			video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
			# print video_info_link
			img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
			value = img_data[0]
			# print value
			value = value.split(",")
			finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
			# print "########### " + finalValue
			return finalValue
		else:
			print "None Found Here Buddy"


		# for script in pageScripts:
		#   print script
		#   print "---------"

		# if (len(pageScripts) >= 1):
		#   for script in [pageScripts][12]:
		#       paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(script)
		#       if len(paramSet) > 0:
		#           video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
		#           # print video_info_link
		#           img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
		#           value = img_data[0]
		#           # print value
		#           value = value.split(",")
		#           finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
		#           # print "########### " + finalValue
		#           return finalValue
		#       else:
		#           print 'Nooone'
		# else:
		#   print "No Links Found"
	except:
		print "An Error Occurred"


def resolve_link(link_url):
	# main_url = urlparse.parse_qs(sys.argv[2][1:]).get('url')[0]
	# main_url = main_url.replace("%3A", ":").replace("%2F", "/").replace("%3F", "?").replace("%3D", "=")
	# link_url = main_url.split("=", 1)[1].split("===")[0]
	link_host = link_url.split("===")[1]
	# print "########### " + link_url
	# print "########### " + link_host
	if link_host == "TVLOGY":
		try:
			if link_host == "TVLOGY":
				videoId = link_url.split("=")[1]
				url = "http://tvlogy.to/watch.php?v=" + videoId
			elif link_host == "VIDOZA":
				videoId = link_url.split("=")[1]
				url = "http://vidoza.net/embed-" + videoId + ".html"
			
			r = requests.get(url)
			data = r.text
			soup = BeautifulSoup(data)

			# print soup.prettify()

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
							print "########### " + value
							return value
		except:
			print "An Error Occurred"
			
	elif link_host == "WATCHVIDEO":
		try:
			videoId = link_url.split("=")[1]
			url = "http://watchvideo18.us/embed-" + videoId + "-540x304.html"
			print "################ " + url
			r = requests.get(url)
			data = r.text
			soup = BeautifulSoup(data)

			text_to_find = 'm3u8|master'

			soup = BeautifulSoup(data)

			pageScripts = soup.findAll('script')

			resultingScript = []

			for script in pageScripts:
				searchableString = str(script)
				if "m3u8|master" in searchableString:
					print "SUCCESS!! ####"
					resultingScript.append(searchableString)
				else:
					print "--------------"

			paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(resultingScript[0])

			if len(paramSet) > 0:
				video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
				# print video_info_link
				img_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
				value = img_data[0]
				# print value
				value = value.split(",")
				finalValue = value[0] + value[1] + "/index-v1-a1.m3u8"
				# print "########### " + finalValue
				return finalValue
			else:
				print "None Found Here Buddy"
			
		except:
			print "An Error Occurred"
			return 'An Error Occurred'


def filter_non_links():
	print "############ NON LINKS ###"

## END LINK DEFINITIONS ##


mode = None

args = sys.argv[2]

if len(args) > 0:
	mode = args.split('mode=')
	mode = mode[1].split('&')
	mode = mode[0]


if mode == None             :       Main_Menu()
elif mode == 'load_channels':       load_shows()
elif mode == 'load_episodes':       fetch_show_episodes()
elif mode == 'load_ep_links':       load_episode_links()
elif mode == 'resolve_link':        resolve_link()
elif mode == 'load_movies':         movie_menu()
elif mode == 'load_movie_links':    load_movie_links()

#################################
#   END OF DIRECTORY LISTINGS   #
#################################

xbmcplugin.endOfDirectory(addon_handle)