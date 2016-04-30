from BeautifulSoup import BeautifulStoneSoup
import resources.lib.util as util
import HTMLParser
import re
import resources.lib.structure as s
import operator


# Based on XBMC LiveStreams Add-on
# http://forum.xbmc.org/showthread.php?tid=97116
class LiveStreamApi(object):
    short_name = 'live'

    def get_xml_data(self, url):
        print 'Fetching xml from url: {url}'.format(
            url=url)
        data = util.get_remote_data(url)
        soup = BeautifulStoneSoup(
            data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

        items = []

        # not expecting channels
        for item in soup('item'):
            if (item.title):
                name = HTMLParser.HTMLParser().unescape(item.title.string)
                thumbnail = item.thumbnail.string
                url = ''

                # helps with sorting
                is_stream = 0

                if (item.link != None and item.link.string != None):
                    url = item.link.string
                    is_stream = 1 if '/' in url else 0

                if item.regex:
                    livestream_regex = s.LiveStreamRegex(
                        # name is a BeautifulSoup keyword
                        item.regex('name')[0].string,
                        item.regex.expres.string,
                        item.regex.page.string)

                    try:
                        livestream_regex.refer = item.regex.referer.string
                    except:
                        pass

                    #try:
                    #    livestream_regex.agent = item.regex.agent
                    #except:
                    #    pass
                else:
                    livestream_regex = s.LiveStreamRegex()

                items.append({
                    'label': name,
                    'url': url,
                    'thumb': thumbnail,
                    'regex': livestream_regex,
                    'is_stream': is_stream,
                })

        return sorted(items, key=operator.itemgetter('is_stream', 'label'))

    def get_parsed_url(self, url, regex):
        print 'Fetching parsed url: {url} -- {regex}'.format(
            url=url, regex=regex)

        doregex = re.compile('\$doregex\[([^\]]*)\]').findall(url)

        for name in doregex:
            if name == regex.label:
                content = util.get_remote_data(regex.page, True, regex.refer)
                r = re.compile(regex.expres).search(content)

                url = url.replace(
                    '$doregex[{name}]'.format(name=name),
                    r.group(1).strip())
                break

        return url
