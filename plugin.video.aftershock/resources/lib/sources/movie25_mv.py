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


import re,urllib,urlparse,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import proxy
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.domains = ['movie25.ph', 'movie25.hk', 'tinklepad.is']
        self.base_link = 'http://tinklepad.ag'
        self.search_link = 'http://tinklepad.ag/search.php?q=%s'

    def request(self, url, check):
        try:
            result = client.request(url)
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

            result = client.request(proxy.get() + urllib.quote_plus(url))
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

            result = client.request(proxy.get() + urllib.quote_plus(url))
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.request(query, post=urllib.urlencode({'chts': 'Click Here to Continue'}))

            result = client.parseDOM(result, 'div', attrs = {'class': 'movie_table'})

            title = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['q'][0], i[1]) for i in result]
            except: pass
            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in result]
            except: pass
            try: result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]
            except: pass

            match = [i[0] for i in result if title == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    result = proxy.request(urlparse.urljoin(self.base_link, i), 'link_name')
                    if imdb in str(result): url = i ; break
                except:
                    pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = proxy.request(url, 'Links - Quality')
            result = result.replace('\n','')

            quality = re.compile('>Links - Quality(.+?)<').findall(result)[0]
            quality = quality.strip()
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = client.parseDOM(result, 'div', attrs = {'id': 'links'})[0]
            links = links.split('link_name')

            for i in links:
                try:
                    url = client.parseDOM(i, 'a', ret='href')[0]
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
                    except: pass
                    url = urlparse.urlparse(url).query
                    url = base64.b64decode(url)
                    url = re.findall('((?:http|https)://.+?/.+?)(?:&|$)', url)[0]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url, resolverList=None):
        return url


