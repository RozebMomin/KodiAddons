from resources.lib.abc_base import BaseForum
from BeautifulSoup import BeautifulSoup
import resources.lib.util as util
import HTMLParser
import resources.lib.structure as s
import resources.lib.hosts as hosts
import datetime


class ApnaDramasApi(BaseForum):
    short_name = 'apnadramas'
    long_name = 'Apna Dramas Forum'
    local_thumb = 'thumb_apnadramas.png'
    base_url = 'http://www.apnapakforums.com/'
    sub_id_regex = '\?(\d+)\-'

    section_url_template = 'forumdisplay.php?'
    thread_url_template = 'showthread.php?'

###############################################
    category_drama = s.Category('Browse Pakistani Dramas', [
        s.Channel('20', 'Ary Digital', 'ary.png'),
        s.Channel('22', 'Geo', 'geo.png'),
        s.Channel('21', 'Hum TV', 'hum.png'),
        s.Channel('1131', 'Hum Sitaray', 'humsitaray.png'),
        s.Channel('1058', 'ARY Zindagi', 'aryZindagi.png'),
        s.Channel('23', 'PTV Home', 'ptv.png'),
        s.Channel('592', 'Express Entertainment', 'expressEntertainment.png'),
        s.Channel('768', 'Urdu 1', 'urdu1.png'),
        s.Channel('98', 'A Plus', 'aplus.png'),
        s.Channel('24', 'TV One', 'tv1.png'),
    ])

    category_morning = s.Category('Browse Morning/Cooking Shows', [
        s.Channel('453', 'Morning Shows', 'morning.png'),
        s.Channel('189', 'Cooking Shows', 'cooking.png'),
    ])

    category_news = s.Category('Browse Current Affairs Talk Shows', [
        s.Channel('106', 'Geo News', 'geoNews.png'),
        s.Channel('109', 'Dunya TV', 'dunya.png'),
        s.Channel('107', 'Express News', 'expressNews.png'),
        s.Channel('108', 'Ary News', 'aryNews.png'),
        s.Channel('105', 'AAJ News', 'aaj.png'),
        s.Channel('259', 'Samaa News', 'samaa.png'),
        s.Channel('348', 'Dawn News', 'dawn.png'),
    ])

    categories = {
        'drama': category_drama,
        'morning': category_morning,
        'news': category_news,
    }

###############################################
    match_string = {
        'yytu.php': (hosts.youtube, 'v='),
        'dmm.php': (hosts.dailymotion, 'v='),
    }

###############################################

    def get_parents(self, linklist):
        '''identify forum sections/subsections'''
        newlist = []

        for l in linklist:
            if (l.get('id')):
                newlist.append(l)
            
                if (l.ol):
                    parent = newlist[-1]
                    parent['data-has-children'] = True

        return newlist

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

        sub = soup.find('div', attrs={'id': 'forumbits'}).find('ol')
        h = sub.findAll('li', attrs={'class': 'forumbit_post old L1'})
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

        container = soup.find('ol', id='threads')
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

            navlink = soup.find('div', attrs={'class': 'threadpagenav'})

            if navlink:
                anchor = navlink.find('a', attrs={'rel': 'next'})
                if anchor:
                    next_url = self.base_url + anchor['href']

        return items, next_url