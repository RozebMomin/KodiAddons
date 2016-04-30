import abc
import re
from BeautifulSoup import BeautifulSoup
import resources.lib.util as util
import HTMLParser
from resources.lib.post import Post
from xbmcswift2 import xbmcgui


class BaseForum(object):
    __metaclass__ = abc.ABCMeta

    short_name = 'base'
    long_name = 'Base Forum'
    local_thumb = ''
    base_url = ''

    sub_id_regex = '(?:\?f=|\/f|\?t=)(\d+)'
    mobile_style = ''

###############################################

    def get_frame_menu(self):
        return

    def browse_frame(self, frameid, url):
        return

    def get_sub_id(self, url):
        ''' get sub forum/thread id'''
        pk = None
        if url:
            t = re.compile(self.sub_id_regex).findall(url)
            if t:
                pk = t[0]
        return pk

    def get_parents(self, linklist):
        '''identify forum sections/subsections'''
        newlist = []

        for l in linklist:
            if (l.get('id')):
                newlist.append(l)
            else:
                parent = newlist[-1]
                parent['data-has-children'] = True

        return newlist

    def has_new_episodes(self, listitem):
        if ((listitem.img['src'].find('new') > 0) or
                (listitem.a.img)):
            return True
        return False

###############################################

    def get_category_menu(self):
        items = [{
            'label': value.label,
            'categoryid': key
            } for key, value in self.categories.items()]
        return items

    def get_channel_menu(self, categoryid):
        return self.categories[categoryid].channels

    def get_show_menu(self, channelid):
        ''' Get shows for specified channel'''

        url = '{base}{section}{pk}{style}'.format(
            base=self.base_url,
            section=self.section_url_template,
            pk=channelid,
            style=self.mobile_style)

        print 'Get show menu: {url}'.format(url=url)

        data = util.get_remote_data(url)
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)

        sub = soup.find('ul', attrs={
            'data-role': 'listview', 'data-theme': 'd', 'class': 'forumbits'})
        h = sub.findAll('li')
        linklist = self.get_parents(h)

        channels = []
        shows = []

        if linklist and len(linklist) > 0:

            # New items on top
            linklist = sorted(linklist, key=lambda l: self.has_new_episodes(l), reverse=True)

            for l in linklist:
                tagline = HTMLParser.HTMLParser().unescape(
                    l.a.text.encode('utf-8', 'ignore'))
                link = self.base_url + l.a['href'].encode('utf-8', 'ignore')
                fid = self.get_sub_id(link)

                # identify new items
                if (self.has_new_episodes(l)):
                    tagline = tagline + '     [B]**NEW**[/B]'

                data = {
                    'label': tagline,
                    'url': link,
                    'pk': fid,
                }

                if (l.get('data-has-children')):
                    channels.append(data)
                else:
                    shows.append(data)

        return channels, shows

    def get_episode_menu(self, url, page=1):
        ''' Get episodes for specified show '''

        url = '{url}{style}'.format(
            url=url, style=self.mobile_style)
        data = util.get_remote_data(url)
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)

        items = []
        next_url = None

        container = soup.find('ul', id='threads')
        if container and len(container) > 0:
            linklist = container.findAll('h3')

            for l in linklist:
                tagline = HTMLParser.HTMLParser().unescape(
                    l.a.text.encode('utf-8', 'ignore'))
                link = l.a['href'].encode('utf-8', 'ignore')

                tid = self.get_sub_id(link)

                items.append({
                    'label': tagline,
                    'url': self.base_url + link,
                    'pk': tid,
                })

            navlink = soup.find('div', attrs={'data-role': 'vbpagenav'})

            if navlink:
                total_pages = int(navlink['data-totalpages'])
                if (total_pages and total_pages > page):
                    pg = url.find('&page=')
                    url = url[:pg] if pg > 0 else url
                    next_url = url + '&page=' + str(page + 1)

        return items, next_url

    def get_episode_data(self, url):
        url = '{url}{style}'.format(
            url=url, style=self.mobile_style)
        print 'Get episode data: {url}'.format(url=url)

        data = util.get_remote_data(url)
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)

        linklist = soup.find('ol', id='posts').find(
            'blockquote', 'postcontent restore').findAll('a')

        # correct links for erroneous formatting
        cleanlinks = util.clean_post_links(linklist)

        # parse post links
        p = Post(self.match_string)

        progress = xbmcgui.DialogProgress()
        progress.create('[B]Processing found links[/B]')
        total = len(cleanlinks)
        current = 0

        for url, text in cleanlinks.items():
            current += 1
            percent = (current * 100) // total
            msg = 'Processing {current} of {total}'.format(
                current=current, total=total)
            progress.update(percent, '', msg, '')

            if progress.iscanceled():
                break

            # process here
            p.add_link(url, text)

        progress.close()

        items = [{
            'label': HTMLParser.HTMLParser().unescape(part.text),
            'partnum': num,
            'media': part.media
        } for num, part in sorted(p.parts.items())]

        return items
