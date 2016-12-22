# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re, urllib, urlparse, json
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import logger
from resources.lib.libraries import cache
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import *

class source:
    def __init__(self):
        self.base_location = 'https://offshoregit.com/vineegu/aftershock-repo/iptv_base.json'
        self.base_link = []
        self.list = []
        self.fileName = 'iptv.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)
        self.vlc_user_agent = 'VLC/2.2.1 LibVLC/2.2.17&Icy-MetaData=1'

    def removeJSON(self, name):
        control.delete(self.fileName)
        return 0

    def getLiveSource(self):
        try :
            generateJSON = cache.get(self.removeJSON, 168, __name__, table='live_cache')
            if not os.path.exists(self.filePath):
                generateJSON = 1

            if generateJSON:
                logger.debug('Generating %s JSON' % __name__, __name__)
                '''
                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(self.base_link, outfile, sort_keys=True, indent=2)

                filename = open(self.filePath)
                result = filename.read()
                filename.close()

                self.base_link = json.loads(result)
                '''
                channelList = {}
                if control.setting('livelocal') == 'true' :
                    self.base_location = os.path.join(control.dataPath, 'iptv_base.local')
                    file = open(self.base_location)
                    result = file.read()
                    file.close()
                else:
                    result = client.request(self.base_location)

                self.base_link = json.loads(result)
                for item in self.base_link:
                    try:
                        enabled = item['enabled']
                        if enabled == "false" :
                            logger.debug('Skipping %s' % item['link'], __name__)
                            continue
                        type = item['source']
                        link = item['link']
                        regex = item['regex']
                        headers = link.rsplit('|', 1)[1]
                        link = link.rsplit('|', 1)[0]
                    except: headers = None

                    '''
                    if control.setting('livelocal') == 'true' :
                        self.base_location = os.path.join(control.dataPath, 'test_base.local')
                        file = open(self.base_location)
                        result = file.read()
                        file.close()
                    else:
                        result = client.request(link, timeout=5)
                    '''

                    logger.debug('Fetching %s' % link, __name__)
                    result = client.request(link, timeout=5)

                    if result == None :
                        continue

                    result = result.replace('\r', '')

                    result = re.findall(regex, result, re.IGNORECASE)

                    for source, title, cUrl in result:
                        from resources.lib.libraries import livemeta
                        names = cache.get(livemeta.source().getLiveNames, 200, table='live_cache')
                        title = cleantitle.live(title, names)
                        if title == 'SKIP':
                            continue
                        if not headers == None:
                            cUrl = '%s|%s' % (cUrl, headers)
                        channelList['%s||%s' % (title, type)] ={'icon':'','url':cUrl,'provider':'iptv','source':type,'direct':False, 'quality':'HD'}


                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(channelList, outfile, sort_keys=True, indent=2)

                liveParser = LiveParser(self.fileName, control.addon)
                self.list = liveParser.parseFile(decode=False)
            return (generateJSON, self.list)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(e)
            pass

    def resolve(self, url, resolverList):
        if not 'User-Agent' in url:
            url = '%s|User-Agent=%s' % (url, self.vlc_user_agent)
            if '.ts' in url or '.mpegts' in url:
                url='plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urllib.quote_plus(url))
            elif '.m3u8' in url:
                url='plugin://plugin.video.f4mTester/?url=%s&streamtype=HLSRETRY'%(urllib.quote_plus(url))
        return url
