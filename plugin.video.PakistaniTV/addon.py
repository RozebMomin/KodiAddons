from xbmcswift2 import Plugin, xbmcgui
from resources.lib.abc_base import BaseForum
from resources.lib.sites import *
import resources.lib.util as util
from operator import itemgetter
import resources.lib.structure as s
import resources.lib.sites.live as live


bookmark_storage = 'my_bookmarks'
temp_storage = 'temp_storage'
livestream_xml_url = 'livestream_xml_url'

plugin = Plugin()


STRINGS = {
    'url_resolver_settings': 30100,
    'live_streams': 30016,
    'try_again': 30020,
    'site_unavailable': 30021,
    'is_unavailable': 30022,
    'try_again_later': 30023,
    'channel_xml_fail': 30024,
    'no_episodes': 30026,
    'no_valid_links': 30027,
    'cannot_play': 30028,
    'choose_source': 30029,
    'bookmarks': 30110,
    'add_bookmark': 30111,
    'remove_bookmark': 30112,
    'no_bookmarks': 30113,
    'bookmark_success': 30114,
    'bookmark_storage_fail': 30115,
    'bookmark_error': 30116,
    'bookmark_remove_question': 30117,
}


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id])
    else:
        plugin.log.warning('String is missing: %s' % string_id)
        return string_id


###############################################


@plugin.route('/')
def index():
    items = [{
        'label': '[B]{txt}[/B]'.format(txt=_('bookmarks')),
        'path': plugin.url_for('show_bookmarks'),
        'thumbnail': util.get_image_path('bookmark.png')}]

    items.extend([{
        'label': sc.long_name,
        'path': plugin.url_for(
            'get_category_menu', siteid=index,
            cls=sc.__name__),
        'thumbnail': util.get_image_path(sc.local_thumb),
        'icon': util.get_image_path(sc.local_thumb),
        } for index, sc in enumerate(BaseForum.__subclasses__())])

    # live streams if xml url specified
    url = plugin.get_setting(livestream_xml_url, str)
    if url:
        thumb = util.get_image_path('thumb_live.jpg')
        items.append({
            'label': '[B]{txt}[/B]'.format(
                txt=_('live_streams')),
            'path': plugin.url_for('get_live_channels'),
            'thumbnail': thumb,
            'icon': thumb
        })

    thumb = util.get_image_path('settings.png')
    items.append({
        'label': '[COLOR white]{txt}[/COLOR]'.format(
            txt=_('url_resolver_settings')),
        'path': plugin.url_for('get_urlresolver_settings'),
        'thumbnail': thumb,
        'icon': thumb
        })
    return items


###############################################


@plugin.route('/bookmarks/')
def show_bookmarks():
    def context_menu(item_path):
        context_menu = [(
            _('remove_bookmark'),
            'XBMC.RunPlugin(%s)' % plugin.url_for('remove_bookmark',
                                                  item_path=item_path,
                                                  refresh=True),
        )]
        return context_menu

    bookmarks = plugin.get_storage(bookmark_storage)
    items = bookmarks.values()

    for item in items:
        item['context_menu'] = context_menu(item['path'])
    if not items:
        items = [{
            'label': _('no_bookmarks'),
            'path': plugin.url_for('show_bookmarks'),
        }]

    return sorted(items, key=lambda x: x['label'].partition('-')[2])


@plugin.route('/bookmarks/add/<item_path>')
def add_bookmark(item_path):
    bookmarks = plugin.get_storage(bookmark_storage)

    if bookmarks is not None:
        if item_path not in bookmarks:
            temp = plugin.get_storage(temp_storage)
            item = temp[item_path]

            groupname = plugin.request.args['groupname'][0]
            if groupname:
                item['label'] = groupname + ' - ' + item['label']

            bookmarks[item_path] = item
        else:
            item = bookmarks[item_path]

        dialog = xbmcgui.Dialog()
        dialog.ok(_('add_bookmark'),
                  _('bookmark_success'),
                  '{label}'.format(label=item['label']))
    else:
        msg = [_('bookmark_storage_fail'), _('try_again')]
        plugin.log.error(msg[0])
        dialog = xbmcgui.Dialog()
        dialog.ok(_('bookmark_error'), *msg)


@plugin.route('/bookmarks/remove/<item_path>')
def remove_bookmark(item_path):
    bookmarks = plugin.get_storage(bookmark_storage)
    label = bookmarks[item_path]['label']

    dialog = xbmcgui.Dialog()
    if dialog.yesno(_('remove_bookmark'),
                    _('bookmark_remove_question'),
                    '{label}'.format(label=label)):

        plugin.log.debug('remove bookmark: {label}'.format(label=label))

        if item_path in bookmarks:
            del bookmarks[item_path]
            bookmarks.sync()
            xbmc.executebuiltin("Container.Refresh")


###############################################


def __add_listitem(items, groupname=''):
    '''
    Redirect all entries through here
    to add bookmark option in context menu and
    to add item info to temp storage
    '''
    def context_menu(item_path, groupname):
        context_menu = [(
            _('add_bookmark'),
            'XBMC.RunPlugin(%s)' % plugin.url_for(
                endpoint='add_bookmark',
                item_path=item_path,
                groupname=groupname
            ),
        )]
        return context_menu

    temp = plugin.get_storage(temp_storage)
    temp.clear()
    for item in items:
        temp[item['path']] = item
        item['context_menu'] = context_menu(item['path'], groupname)
    temp.sync()
    return items


def get_cached(func, *args, **kwargs):
    '''Return the result of func with the given args and kwargs
    from cache or execute it if needed'''
    @plugin.cached(kwargs.pop('TTL', 1440))
    def wrap(func_name, *args, **kwargs):
        return func(*args, **kwargs)
    return wrap(func.__name__, *args, **kwargs)


###############################################


@plugin.route('/urlresolver/')
def get_urlresolver_settings():
    import urlresolver
    urlresolver.display_settings()
    return


@plugin.route('/sites/<siteid>-<cls>/')
def get_category_menu(siteid, cls):
    siteid = int(siteid)
    api = BaseForum.__subclasses__()[siteid]()

    plugin.log.debug('browse site: {site}'.format(site=cls))

    # check if site is available
    if api.base_url:
        available = util.is_site_available(api.base_url)

        if available:
            frameitems = []
            categoryitems = []

            # get frames
            f = api.get_frame_menu()
            if f:
                frameitems = [{
                    'label': item['label'],
                    'path': plugin.url_for(
                        'browse_frame', siteid=siteid, cls=cls,
                        frameid=index, url=item['url'])
                } for index, item in enumerate(f)]

            # get categories
            c = api.get_category_menu()
            if c:
                categoryitems = [{
                    'label': '[B]{item}[/B]'.format(item=item['label']),
                    'path': plugin.url_for(
                        'browse_category', siteid=siteid, cls=cls,
                        categoryid=item['categoryid'])
                } for item in c]

            by_label = itemgetter('label')
            items = frameitems + sorted(categoryitems, key=by_label)
            return items

        else:
            msg = [
                '[B][COLOR red]{txt}[/COLOR][/B]'.format(
                    txt=_('site_unavailable')),
                '{site} {txt}'.format(
                    site=api.long_name, txt=_('is_unavailable')),
                _('try_again_later')]
            plugin.log.error(msg[1])

            dialog = xbmcgui.Dialog()
            dialog.ok(api.long_name, *msg)
    else:
        msg = 'Base url not implemented'
        plugin.log.error(msg)
        raise Exception(msg)


@plugin.route('/sites/<siteid>-<cls>/category/<categoryid>/')
def browse_category(siteid, cls, categoryid):
    siteid = int(siteid)
    api = BaseForum.__subclasses__()[siteid]()

    plugin.log.debug('browse category: {category}'.format(category=categoryid))

    items = [{
        'label': item.label,
        'thumbnail': item.thumb,
        'icon': item.thumb,
        'path': plugin.url_for(
            'browse_channels', siteid=siteid, cls=cls,
            channelid=item.id)
    } for item in api.get_channel_menu(categoryid)]

    by_label = itemgetter('label')
    return __add_listitem(groupname=api.short_name,
                          items=sorted(items, key=by_label))


@plugin.route('/sites/<siteid>-<cls>/frames/f<frameid>/')
def browse_frame(siteid, cls, frameid):
    siteid = int(siteid)
    url = plugin.request.args['url'][0]
    api = BaseForum.__subclasses__()[siteid]()

    plugin.log.debug('browse frame: {frame}'.format(frame=url))

    # Some forum frames contain shows
    # while others contain episodes
    contents, contype = get_cached(api.browse_frame, frameid, url)
    if contype and contype == s.ThreadType().Episode:
        items = [{
            'label': item['label'],
            'path': plugin.url_for(
                'get_episode_data', siteid=siteid, cls=cls, frameid=frameid,
                epid=item.get('pk', '0'), url=item['url'])
        } for item in contents]
    else:
        items = [{
            'label': item['label'],
            'path': plugin.url_for(
                'browse_shows', siteid=siteid, cls=cls, frameid=frameid,
                showid=item.get('pk', '0'), showpage=1, url=item['url'])
        } for item in contents]

    return __add_listitem(groupname=api.short_name, items=items)


@plugin.route('/sites/<siteid>-<cls>/channels/c<channelid>/')
def browse_channels(siteid, cls, channelid):
    siteid = int(siteid)
    api = BaseForum.__subclasses__()[siteid]()

    plugin.log.debug('browse channel: {channel}'.format(channel=channelid))

    channels, shows = get_cached(api.get_show_menu, channelid)

    showitems = [{
        'label': item['label'],
        'path': plugin.url_for(
            'browse_shows', siteid=siteid, cls=cls,
            showid=item['pk'], showpage=1, url=item['url'])
    } for item in shows]

    channelitems = [{
        'label': '[B]{item}[/B]'.format(item=item['label']),
        'path': plugin.url_for(
            'browse_channels', siteid=siteid, cls=cls,
            channelid=item['pk'], url=item['url'])
    } for item in channels]

    by_label = itemgetter('label')
    items = showitems + sorted(channelitems, key=by_label)
    return __add_listitem(groupname=api.short_name, items=items)


@plugin.route('/sites/<siteid>-<cls>/shows/s<showid>/<showpage>/')
def browse_shows(siteid, cls, showid, showpage=1):
    siteid = int(siteid)
    url = plugin.request.args['url'][0]
    api = BaseForum.__subclasses__()[siteid]()

    showpage = int(showpage)

    plugin.log.debug('browse show: {show}'.format(show=url))

    videos, next_url = get_cached(api.get_episode_menu, url, showpage)

    items = []

    if videos:
        items = [{
            'label': item['label'],
            'path': plugin.url_for(
                'get_episode_data', siteid=siteid, cls=cls,
                showid=showid, epid=item.get('pk', 0), url=item['url'])
        } for item in videos]

        if next_url:
            items.append({
                'label': 'Next >>',
                'path': plugin.url_for(
                    'browse_shows', siteid=siteid,
                    cls=cls, showid=showid, showpage=str(showpage + 1),
                    url=next_url)
            })

        return __add_listitem(groupname=api.short_name, items=items)
    else:
        msg = '[B][COLOR red]{txt}[/COLOR][/B]'.format(
            txt=_('no_episodes'))
        plugin.log.error(msg)
        dialog = xbmcgui.Dialog()
        dialog.ok(api.long_name, msg)


@plugin.route('/sites/<siteid>-<cls>/episodes/e<epid>/')
def get_episode_data(siteid, cls, epid):
    siteid = int(siteid)
    url = plugin.request.args['url'][0]
    api = BaseForum.__subclasses__()[siteid]()

    plugin.log.debug('browse episode: {ep}'.format(ep=url))

    data = api.get_episode_data(url)
    if data:
        items = [{
            'label': item['label'],
            'path': plugin.url_for(
                'play_video', siteid=siteid, cls=cls,
                epid=epid, partnum=item['partnum'],
                media=item['media']),
            'is_playable': True
            } for item in data]

        # Add continuous play to top
        # if Single Link (Part 0) does not exist
        # and more than 1 parts
        if (data[0]['partnum'] != 0 and
                len(data) > 1):

            # save post data to temp
            temp = plugin.get_storage(temp_storage)
            temp.clear()
            temp['items'] = data

            items.insert(0, {
                'label': 'Continuous Play',
                'path': plugin.url_for(
                    'play_video_continuous', siteid=siteid, cls=cls,
                    epid=epid),
                'is_playable': True
            })

        return items

    else:
        msg = '[B][COLOR red]{txt}[/COLOR][/B]'.format(
            txt=_('no_valid_links'))
        plugin.log.error(msg)
        dialog = xbmcgui.Dialog()
        dialog.ok(api.long_name, msg)


def __is_resolved(url):
    return (url and isinstance(url, basestring))


def __resolve_item(item):
    import urlresolver
    media = urlresolver.HostedMediaFile(
        host=item[0].server, media_id=item[1])
    return media.resolve(), item[0].thumb


def __resolve_part(medialist, selected_host):
    ''' resolve stream url for part
    based on selected host or next best case
    '''

    stream_url, thumb = None, None
    # try to resolve selected host
    for item in medialist:
        if (item[0].server == selected_host):
            stream_url, thumb = __resolve_item(item)

            # remove from list (to avoid repeated resolving)
            medialist.remove(item)
            break

    # if fail, get the next best thing
    if not stream_url:
        while medialist:
            stream_url, thumb = __resolve_item(medialist.pop())
            if __is_resolved(stream_url):
                break

    # still fail?
    if __is_resolved(stream_url):
        return stream_url, thumb
    else:
        msg = str(stream_url.msg)
        raise Exception(msg)


@plugin.route('/sites/<siteid>-<cls>/episodes/e<epid>/all')
def play_video_continuous(siteid, cls, epid):
    siteid = int(siteid)
    api = BaseForum.__subclasses__()[siteid]()

    temp = plugin.get_storage(temp_storage)
    data = temp['items']

    part_media = data[0]['media']

    media = []

    import urlresolver
    for host, vid in sorted(part_media, key=lambda x: x[0].server):
        r = urlresolver.HostedMediaFile(
            host=host.server, media_id=vid)
        if r:
            media.append(r)

    source = urlresolver.choose_source(media)
    plugin.log.debug('>>> Source selected')
    plugin.log.debug(source)

    if source:
        selected_host = source.get_host()
        plugin.log.debug('play from host {host}'.format(host=selected_host))

        items = []

        for part in data:
            medialist = part['media']
            stream_url, thumb = __resolve_part(medialist, selected_host)

            items.append({
                'label': 'Continuous Play: {part}'.format(part=part['label']),
                'path': stream_url,
                'thumbnail': thumb,
                'icon': thumb,
            })

        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
        plugin.add_to_playlist(items)

        # Setting resolved url for first item
        # otherwise playlist seems to skip it
        plugin.set_resolved_url(items[0])

    else:
        msg = [_('cannot_play'), _('choose_source')]
        plugin.log.error(msg[0])
        dialog = xbmcgui.Dialog()
        dialog.ok(api.long_name, *msg)


@plugin.route('/sites/<siteid>-<cls>/episodes/e<epid>/<partnum>')
def play_video(siteid, cls, epid, partnum):
    siteid = int(siteid)
    api = BaseForum.__subclasses__()[siteid]()

    part_media = plugin.request.args['media'][0]
    media = []

    import urlresolver
    for host, vid in sorted(part_media, key=lambda x: x[0].server):
        r = urlresolver.HostedMediaFile(
            host=host.server, media_id=vid)
        if r:
            media.append(r)

    source = urlresolver.choose_source(media)
    plugin.log.debug('>>> Source selected')
    plugin.log.debug(source)

    if source:
        url = source.resolve()

        if not __is_resolved(url):
            msg = str(url.msg)
            raise Exception(msg)

        else:
            plugin.log.debug('play video: {url}'.format(url=url))
            plugin.set_resolved_url(url)        
        
    else:
        msg = [_('cannot_play'), _('choose_source')]
        plugin.log.error(msg[0])
        dialog = xbmcgui.Dialog()
        dialog.ok(api.long_name, *msg)


###############################################


@plugin.route('/live/')
def get_live_channels():
    plugin.log.debug('browse live channels')

    api = live.LiveStreamApi()
    url = plugin.get_setting(livestream_xml_url, str)

    channels = get_cached(api.get_xml_data, url)

    if channels:
        items = [{
            'label': item['label'],
            'thumbnail': item['thumb'],
            'icon': item['thumb'],
            'path': plugin.url_for(
                'play_stream', url=item['url'],
                regex=item['regex']
            ),
            'is_playable': True
        } for item in channels]

        return __add_listitem(groupname=api.short_name,
                              items=items)
    else:
        msg = '[B][COLOR red]{txt}[/COLOR][/B]'.format(
                txt=_('channel_xml_fail'))
        plugin.log.error(msg)

        dialog = xbmcgui.Dialog()
        dialog.ok(_('live_streams'), msg)


@plugin.route('/live/<url>')
def play_stream(url):
    regex = plugin.request.args.get('regex', [s.LiveStreamRegex()])[0]
    if regex.label:
        api = live.LiveStreamApi()
        url = get_cached(api.get_parsed_url, url, regex)

    plugin.log.debug('play live stream: {url}'.format(url=url))
    plugin.set_resolved_url(url)


###############################################


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception, e:
        plugin.log.error(e)
        plugin.notify(msg=e, delay=8000)
