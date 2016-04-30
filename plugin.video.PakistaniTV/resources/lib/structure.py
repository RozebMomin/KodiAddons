import resources.lib.util as util
import HTMLParser


class ThreadType():
    '''
    Enum representing types a forum can contain
    '''
    Show, Episode = range(2)


class Category():
    def __init__(self, label, channels):
        self.label = label
        self.channels = channels


class Channel():
    def __init__(self, id, label, thumb=''):
        self.id = id
        self.label = label
        self.__thumb = thumb

    @property
    def thumb(self):
        if self.__thumb:
            self.__thumb = util.get_image_path(self.__thumb)
        return self.__thumb


class LiveStreamRegex():
    '''
    Represents the regex portion supplied for a Live Stream
    (optional)
    '''
    def __init__(self, label='', expres='', page='', refer='', agent=''):
        self.label = HTMLParser.HTMLParser().unescape(label)
        self.expres = expres
        self.page = HTMLParser.HTMLParser().unescape(page)
        self.refer = HTMLParser.HTMLParser().unescape(refer)
        self.agent = agent

    def __str__(self):
        return '''
                label: {label},
                express: {expres},
                page: {page},
                refer: {refer},
                agent: {agent}'''.format(
            label=self.label,
            expres=self.expres,
            page=self.page,
            refer=self.refer,
            agent=self.agent)
