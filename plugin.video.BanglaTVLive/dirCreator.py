'''
Created on 6 Mar 2014

@author: home
'''
import urllib,urllib2, HTMLParser;
import sys,xbmcgui,xbmcplugin;

class parseList(object):
    def __init__(self, listToParse):
        for entry in listToParse:
            name=entry["name"];
            url=entry["url"];
            mode=entry["mode"];
            paramList=None;
            try:
                paramList=entry["paramList"];
            except: pass
            
            contextMenuList=None;
            try:
                contextMenuList=entry["contextMenuList"];
            except: pass
            
            iconimage='';
            try:
                iconimage=entry["iconimage"];
            except: pass
            
            isFolder=True;
            try:
                isFolder=entry["isFolder"];
            except: pass
            #print name
            self.addDir(name, url,mode, paramList, iconimage, contextMenuList,isFolder)
        return
    
    def addDir(self,name,url,mode,parameterList,iconimage,contextMenuList=None,isFolder=True ):
    	h = HTMLParser.HTMLParser()
    	name= h.unescape(name).decode("utf-8")
    	rname=  name.encode("utf-8")
        paramString=""
    	if parameterList:
            for param in parameterList:
                paramString+="&"
                paramString+=param["name"] + "="+urllib.quote_plus(param["value"]);#="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(rname)
    	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(rname)
        u+=paramString
        ok=True
   
    	liz=xbmcgui.ListItem(rname, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    
    	if contextMenuList:
            commandList=[]
            for contextMenuList in contextMenuList:
                commandList.append(( contextMenuList["name"], "XBMC.RunPlugin(%s&contextMenu=%s)" % (u, contextMenuList["value"]), ))
            liz.addContextMenuItems( commands )
    	#print name,url,parameterList,iconimage
    	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
    	return ok
