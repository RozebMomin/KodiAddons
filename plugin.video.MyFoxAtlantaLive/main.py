import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.MyFoxAtlantaLive')

xbmc.executebuiltin('PlayMedia(plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=%5BCOLOR%3DFF00B7EB%2F%5DWAGA+-+24%2F7%5B%2FCOLOR%5D&event_id=2152811&owner_id=4241684&video_id=LIVE)')

# import sys
# import xbmc, xbmcplugin, xbmcgui, xbmcaddon
# import re, os, time
# from datetime import datetime, timedelta
# import urllib, urllib2
# import json
# import calendar

# addon_handle = int(sys.argv[1])

# #Localisation
# local_string = xbmcaddon.Addon(id='plugin.video.MyFoxAtlantaLive').getLocalizedString
# ROOTDIR = xbmcaddon.Addon(id='plugin.video.MyFoxAtlantaLive').getAddonInfo('path')
# ICON = ROOTDIR+"/icon.png"
# FANART = ROOTDIR+"/fanart.jpg"
# IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4'
# SEARCH_HITS = '2'
    
# def CATEGORIES():                    
#     #addDir('Live & Upcoming','/livestream',100,ICON,FANART)
#     #addDir('Search Live','/search',102,ICON,FANART)
#     #addDir('Search Archive','/search',103,ICON,FANART)
#     addDir('Fox 5 News Live','/search',101,ICON,FANART)
     

# def LIST_STREAMS():
#     live_streams = []
#     upcoming_streams = []
#     url = 'http://api.new.livestream.com/curated_events?page=1&maxItems=500'
#     req = urllib2.Request(url)
#     req.add_header('User-Agent', IPHONE_UA)              
#     response = urllib2.urlopen(req)      
#     json_source = json.load(response)
#     response.close()

#     for event in json_source['data']:            
#         event_id = str(event['id'])
#         owner_id = str(event['owner_account_id'])

#         owner_name = name = event['owner']['full_name'].encode('utf-8')
#         full_name = event['full_name'].encode('utf-8')
#         name = owner_name + ' - ' + full_name
#         icon = event['logo']['url']

#         #2013-03-26T14:28:00.000Z
#         pattern = "%Y-%m-%dT%H:%M:%S.000Z"
#         start_time = str(event['start_time'])
#         end_time =  str(event['end_time'])
#         current_time =  datetime.utcnow().strftime(pattern) 
#         my_time = int(time.mktime(time.strptime(current_time, pattern)))             
#         event_end = int(time.mktime(time.strptime(end_time, pattern)))

#         length = 0
#         try:
#             length = int(item['duration'])
#         except:        
#             pass

#         print start_time         
#         aired = start_time[0:4]+'-'+start_time[5:7]+'-'+start_time[8:10]
#         print aired

#         info = {'plot':'','tvshowtitle':'Livestream','title':name,'originaltitle':name,'duration':length,'aired':aired}
        
#         if event['in_progress']:
#             name = '[COLOR=FF00B7EB]'+name+'[/COLOR]'
#             live_streams.append([name,icon,event_id,owner_id,info])
#         else:

#             if my_time < event_end:                
#                 start_date = datetime.fromtimestamp(time.mktime(time.strptime(start_time, pattern)))    
#                 start_date = datetime.strftime(utc_to_local(start_date),xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))
#                 info['plot'] = "Starting at: "+str(start_date)
#                 #name = name + ' ' + start_date
#                 upcoming_streams.append([name,icon,event_id,owner_id,info])

    
#     for stream in  sorted(live_streams, key=lambda tup: tup[0]):        
#         addDir(stream[0],'/live_now',101,stream[1],FANART,stream[2],stream[3],stream[4])            


#     for stream in  sorted(upcoming_streams, key=lambda tup: tup[0]):
#         addDir(stream[0],'/live_now',101,stream[1],FANART,stream[2],stream[3],stream[4])            
    


# def utc_to_local(utc_dt):
#     # get integer timestamp to avoid precision lost
#     timestamp = calendar.timegm(utc_dt.timetuple())
#     local_dt = datetime.fromtimestamp(timestamp)
#     assert utc_dt.resolution >= timedelta(microseconds=1)
#     return local_dt.replace(microsecond=utc_dt.microsecond)


# def SEARCH():
#     '''
#     POST http://7kjecl120u-2.algolia.io/1/indexes/*/queries HTTP/1.1
#     Host: 7kjecl120u-2.algolia.io
#     Connection: keep-alive
#     Content-Length: 378
#     X-Algolia-Application-Id: 7KJECL120U
#     Origin: http://livestream.com
#     X-Algolia-API-Key: 98f12273997c31eab6cfbfbe64f99d92
#     User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
#     Content-type: application/json
#     Accept: */*
#     Referer: http://livestream.com/watch
#     Accept-Encoding: gzip, deflate
#     Accept-Language: en-US,en;q=0.8

#     {"requests":[{"indexName":"events","params":"query=summ&hitsPerPage=3"},{"indexName":"accounts","params":"query=summ&hitsPerPage=3"},{"indexName":"videos","params":"query=summ&hitsPerPage=3"},{"indexName":"images","params":"query=summ&hitsPerPage=3"},{"indexName":"statuses","params":"query=summ&hitsPerPage=3"}],"apiKey":"98f12273997c31eab6cfbfbe64f99d92","appID":"7KJECL120U"}
#     '''
#     search_txt = ''
#     dialog = xbmcgui.Dialog()
#     search_txt = dialog.input('Enter search text', type=xbmcgui.INPUT_ALPHANUM)

#     json_source = ''

#     if search_txt != '':

#         url = 'http://7kjecl120u-2.algolia.io/1/indexes/*/queries'
#         req = urllib2.Request(url)
#         req.addheaders = [ ("Accept", "*/*"),
#                             ("Accept-Language", "en-US,en;q=0.8"),
#                             ("Accept-Encoding", "gzip, deflate"),
#                             ("X-Algolia-Application-Id", "7KJECL120U"),
#                             ("X-Algolia-API-Key", "98f12273997c31eab6cfbfbe64f99d92"),
#                             ("Content-type", "application/json"),
#                             ("Connection", "keep-alive"),
#                             ("Referer", "http://livestream.com/watch"),
#                             ("User-Agent",'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36')]                
        
        
#         json_search = '{"requests":[{"indexName":"events","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"accounts","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"videos","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"images","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"statuses","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"}],"apiKey":"98f12273997c31eab6cfbfbe64f99d92","appID":"7KJECL120U"}'

#         response = urllib2.urlopen(req,json_search)
#         json_source = json.load(response)
#         #print json_source
#         response.close()


#     return json_source

# def CUSTOM_SEARCH():
#     '''
#     POST http://7kjecl120u-2.algolia.io/1/indexes/*/queries HTTP/1.1
#     Host: 7kjecl120u-2.algolia.io
#     Connection: keep-alive
#     Content-Length: 378
#     X-Algolia-Application-Id: 7KJECL120U
#     Origin: http://livestream.com
#     X-Algolia-API-Key: 98f12273997c31eab6cfbfbe64f99d92
#     User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
#     Content-type: application/json
#     Accept: */*
#     Referer: http://livestream.com/watch
#     Accept-Encoding: gzip, deflate
#     Accept-Language: en-US,en;q=0.8

#     {"requests":[{"indexName":"events","params":"query=summ&hitsPerPage=3"},{"indexName":"accounts","params":"query=summ&hitsPerPage=3"},{"indexName":"videos","params":"query=summ&hitsPerPage=3"},{"indexName":"images","params":"query=summ&hitsPerPage=3"},{"indexName":"statuses","params":"query=summ&hitsPerPage=3"}],"apiKey":"98f12273997c31eab6cfbfbe64f99d92","appID":"7KJECL120U"}
#     '''
#     search_txt = ''
#     dialog = xbmcgui.Dialog()
#     search_txt = 'WAGA'

#     json_source = ''

#     if search_txt != '':

#         url = 'http://7kjecl120u-2.algolia.io/1/indexes/*/queries'
#         req = urllib2.Request(url)
#         req.addheaders = [ ("Accept", "*/*"),
#                             ("Accept-Language", "en-US,en;q=0.8"),
#                             ("Accept-Encoding", "gzip, deflate"),
#                             ("X-Algolia-Application-Id", "7KJECL120U"),
#                             ("X-Algolia-API-Key", "98f12273997c31eab6cfbfbe64f99d92"),
#                             ("Content-type", "application/json"),
#                             ("Connection", "keep-alive"),
#                             ("Referer", "http://livestream.com/watch"),
#                             ("User-Agent",'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36')]                
        
        
#         json_search = '{"requests":[{"indexName":"events","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"accounts","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"videos","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"images","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"statuses","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"}],"apiKey":"98f12273997c31eab6cfbfbe64f99d92","appID":"7KJECL120U"}'

#         response = urllib2.urlopen(req,json_search)
#         json_source = json.load(response)
#         #print json_source
#         response.close()


#     return json_source


# def SEARCH_WAGA():
#     json_source = CUSTOM_SEARCH()
#     if json_source != '':
#         for hits in json_source['results']: 
#             for event in hits['hits']:
#                 try:
#                     print event
#                     event_id = str(event['id'])
#                     owner_id = str(event['owner_account_id'])
#                     name = event['full_name'].encode('utf-8')
#                     name = event['owner_account_full_name'].encode('utf-8') + ' - ' + name
#                     #icon = event['logo']['thumbnail']['url']
#                     icon = event['logo']['large']['url']
                    
#                     start_time = str(event['start_time'])                        
#                     duration = 0
#                     try:
#                         duration = int(item['duration'])
#                     except:        
#                         pass

#                     print start_time         
#                     aired = start_time[0:4]+'-'+start_time[5:7]+'-'+start_time[8:10]
#                     print aired

#                     info = {'plot':'','tvshowtitle':'Livestream','title':name,'originaltitle':name,'duration':duration,'aired':aired}

#                     addDir(name,'/live_now',101,icon,FANART,event_id,owner_id)
#                 except:
#                     pass

# def SEARCH_LIVE():
#     json_source = SEARCH()
#     if json_source != '':
#         for hits in json_source['results']: 
#             for event in hits['hits']:
#                 try:
#                     print event
#                     event_id = str(event['id'])
#                     owner_id = str(event['owner_account_id'])
#                     name = event['full_name'].encode('utf-8')
#                     name = event['owner_account_full_name'].encode('utf-8') + ' - ' + name
#                     #icon = event['logo']['thumbnail']['url']
#                     icon = event['logo']['large']['url']
                    
#                     start_time = str(event['start_time'])                        
#                     duration = 0
#                     try:
#                         duration = int(item['duration'])
#                     except:        
#                         pass

#                     print start_time         
#                     aired = start_time[0:4]+'-'+start_time[5:7]+'-'+start_time[8:10]
#                     print aired

#                     info = {'plot':'','tvshowtitle':'Livestream','title':name,'originaltitle':name,'duration':duration,'aired':aired}

#                     addDir(name,'/live_now',101,icon,FANART,event_id,owner_id)
#                 except:
#                     pass
                

# def SEARCH_ARCHIVE():
#     json_source = SEARCH()
#     if json_source != '':
#         for hits in json_source['results']: 
#             for event in hits['hits']:       
#                 try:         
#                     owner_id = str(event['id'])
#                     url = 'http://new.livestream.com/api/accounts/'+owner_id
#                     json_source = GET_JSON_FILE(url)
#                     #Load all past events            
#                     for past_event in json_source['past_events']['data']:            
#                         name = past_event['full_name']
#                         icon = past_event['logo']['url']
#                         event_id = str(past_event['id'])

#                         start_time = str(past_event['start_time'])                        
#                         duration = 0
#                         try:
#                             duration = int(item['duration'])
#                         except:        
#                             pass

#                         print start_time         
#                         aired = start_time[0:4]+'-'+start_time[5:7]+'-'+start_time[8:10]
#                         print aired

#                         info = {'plot':'','tvshowtitle':'Livestream','title':name,'originaltitle':name,'duration':duration,'aired':aired}
                        
#                         addDir(name,'/archive',101,icon,FANART,event_id,owner_id,info)
#                 except:
#                     pass
            

# def GET_JSON_FILE(url):
#     req = urllib2.Request(url) 
#     req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')     
#     response = urllib2.urlopen(req)            
#     json_source = json.load(response)
#     response.close()  

#     return json_source


# def GET_LIVE_STREAM(owner_id,event_id,icon):    
#     try:
#         url2 = "http://livestream.com/WAGA/live.json"
#         response2 = urllib.urlopen(url2)
#         data2 = json.loads(response2.read())
#         owner_id = "4241684"
#         event_id = str(data2["event_id"])
#         url = 'http://livestream.com/api/accounts/'+owner_id+'/events/'+event_id+'/feed.json?&filter=video'                
#         req = urllib2.Request(url)       
#         req.add_header('User-Agent', IPHONE_UA)
#         response = urllib2.urlopen(req)                    
#         json_source = json.load(response)
#         response.close()
#         m3u8_url = json_source['data'][0]['data']['m3u8_url']
#     except:
#         url = 'http://api.new.livestream.com/accounts/'+owner_id+'/events/'+event_id+'/viewing_info'
#         req = urllib2.Request(url)       
#         req.add_header('User-Agent', IPHONE_UA)
#         try:
#             response = urllib2.urlopen(req)                    
#             json_source = json.load(response)
#             response.close()        
#             m3u8_url = json_source['streamInfo']['m3u8_url']
#         except:
#             pass
#             pass
#             addon = xbmcaddon.Addon()
#             addonname = addon.getAddonInfo('name')
#             xbmcgui.Dialog().ok(addonname, 'Sorry Fox 5 News is not streaming LIVE currently.', 'Please try again later')

#     try:
#         print "M3U8!!!" + m3u8_url
#         req = urllib2.Request(m3u8_url)
#         response = urllib2.urlopen(req)                    
#         master = response.read()
#         response.close()
#         cookie = ''
#         try:
#             cookie =  urllib.quote(response.info().getheader('Set-Cookie'))
#         except:
#             pass

#         print cookie
#         print master

#         line = re.compile("(.+?)\n").findall(master)  

#         for temp_url in line:
#             if '.m3u8' in temp_url:
#                 print temp_url
#                 print desc                  
#                 temp_url = temp_url+'|User-Agent='+IPHONE_UA              
#                 if cookie != '':
#                     temp_url = temp_url + '&Cookie='+cookie

#                 xbmcgui.Dialog().notification('CHOOSE RESOLUTION', 'Please choose the resolution that you would like to watch.', xbmcgui.NOTIFICATION_WARNING)
#                 addLink('Fox 5 - ' + '('+desc+')',temp_url, name +' ('+desc+')', icon)
#             else:
#                 desc = ''
#                 start = temp_url.find('RESOLUTION=')
#                 if start > 0:
#                     start = start + len('RESOLUTION=')
#                     end = temp_url.find(',',start)
#                     desc = temp_url[start:end]
#                 else:
#                     desc = "Audio"
#     except:
#         pass
    

# def addLink(name,url,title,iconimage,fanart=None):
#     ok=True
#     liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
#     liz.setProperty('fanart_image',FANART)
#     liz.setProperty("IsPlayable", "true")
#     liz.setInfo( type="Video", infoLabels={ "Title": title } )
#     if fanart != None:
#         liz.setProperty('fanart_image', fanart)
#     else:
#         liz.setProperty('fanart_image', FANART)
#     ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
#     return ok


# def addDir(name,url,mode,iconimage,fanart=None,event_id=None,owner_id=None,info=None):       
#     ok=True
#     u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&icon="+urllib.quote_plus(iconimage)
#     if event_id != None:
#         u = u+"&event_id="+urllib.quote_plus(event_id)
#     if owner_id != None:
#         u = u+"&owner_id="+urllib.quote_plus(owner_id)
#     liz=xbmcgui.ListItem(name, iconImage=ICON, thumbnailImage=iconimage)
#     liz.setInfo( type="Video", infoLabels={ "Title": name } )
#     if fanart != None:
#         liz.setProperty('fanart_image', fanart)
#     else:
#         liz.setProperty('fanart_image', FANART)

#     if info != None:
#         liz.setInfo( type="Video", infoLabels=info)

#     ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)    
#     xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#     return ok

# def get_params():
#     param=[]
#     paramstring=sys.argv[2]
#     if len(paramstring)>=2:
#             params=sys.argv[2]
#             cleanedparams=params.replace('?','')
#             if (params[len(params)-1]=='/'):
#                     params=params[0:len(params)-2]
#             pairsofparams=cleanedparams.split('&')
#             param={}
#             for i in range(len(pairsofparams)):
#                     splitparams={}
#                     splitparams=pairsofparams[i].split('=')
#                     if (len(splitparams))==2:
#                             param[splitparams[0]]=splitparams[1]
                            
#     return param

# params=get_params()
# url=None
# name=None
# mode=None
# event_id=None
# owner_id=None
# icon = None

# try:
#     url=urllib.unquote_plus(params["url"])
# except:
#     pass
# try:
#     name=urllib.unquote_plus(params["name"])
# except:
#     pass
# try:
#     mode=int(params["mode"])
# except:
#     pass
# try:
#     event_id=urllib.unquote_plus(params["event_id"])
# except:
#     pass
# try:
#     owner_id=urllib.unquote_plus(params["owner_id"])
# except:
#     pass
# try:
#     icon=urllib.unquote_plus(params["icon"])
# except:
#     pass

# print "Mode: "+str(mode)
# #print "URL: "+str(url)
# print "Name: "+str(name)
# print "Event ID:"+str(event_id)
# print "Owner ID:"+str(owner_id)



# if mode==None or url==None or len(url)<1:
#         #print ""                
#         CATEGORIES()  
# elif mode==100:        
#         LIST_STREAMS()
# elif mode==101:        
#         GET_LIVE_STREAM(owner_id,event_id,icon)
# elif mode==102:
#         SEARCH_LIVE()
# elif mode==103:
#         SEARCH_ARCHIVE()
# elif mode==104:
#         SEARCH_WAGA()

# if mode == 100:
#     xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
# else:
#     xbmcplugin.endOfDirectory(addon_handle)
