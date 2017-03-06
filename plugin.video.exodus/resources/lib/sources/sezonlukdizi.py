# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['sezonlukdizi.net', 'sezonlukdizi.com']
        self.base_link = 'http://sezonlukdizi.net'
        self.search_link = '/js/dizi.js'
        self.video_link = '/ajax/dataEmbed.asp'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            result = cache.get(self.sezonlukdizi_tvcache, 120)

            tvshowtitle = cleantitle.get(tvshowtitle)

            result = [i[0] for i in result if tvshowtitle == i[1]][0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sezonlukdizi_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            result = re.compile('{(.+?)}').findall(result)
            result = [(re.findall('u\s*:\s*(?:\'|\")(.+?)(?:\'|\")', i), re.findall('d\s*:\s*(?:\'|\")(.+?)(?:\'|\")', i)) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(re.compile('/diziler(/.+?)(?://|\.|$)').findall(i[0]), re.sub('&#\d*;','', i[1])) for i in result]
            result = [(i[0][0] + '/', cleantitle.get(i[1])) for i in result if len(i[0]) > 0]

            return result
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if url == None: return

        url = '%s%01d-sezon-%01d-bolum.html' % (url.replace('.html', ''), int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            result = re.sub(r'[^\x00-\x7F]+', ' ', result)

            pages = client.parseDOM(result, 'div', attrs = {'class': 'menu'})
            pages = client.parseDOM(pages, 'div', ret='data-id')

            for page in pages:
                try:
                    url = urlparse.urljoin(self.base_link, self.video_link)
                    post = 'id=%s' % page

                    for i in range(3):
                        result = client.request(url, post=post)
                        if not result == None: break

                    url = client.parseDOM(result, 'iframe', ret='src')[0]

                    if 'openload.co' in url: sources.append({'source': 'openload.co', 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    if not '.asp' in url: raise Exception()

                    if not url.startswith('http'):
                        url = 'http:' + url

                    for i in range(3):
                        result = client.request(url)
                        if not result == None: break

                    captions = re.search('kind\s*:\s*(?:\'|\")captions(?:\'|\")', result)
                    if not captions: raise Exception()

                    r = re.findall('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?[^"]*"', result)

                    links = [(i[0], '1080p') for i in r if int(i[1]) >= 1080]
                    links += [(i[0], 'HD') for i in r if 720 <= int(i[1]) < 1080]
                    links += [(i[0], 'SD') for i in r if 480 <= int(i[1]) < 720]

                    for i in links: sources.append({'source': 'gvideo', 'quality': i[1], 'language': 'en', 'url': i[0], 'direct': True, 'debridonly': False})

                    if r: break
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if not url.startswith('http'):
                url = 'http:' + url

            for i in range(3):
                u = directstream.googlepass(url)
                if not u == None: break

            return u
        except:
            return


