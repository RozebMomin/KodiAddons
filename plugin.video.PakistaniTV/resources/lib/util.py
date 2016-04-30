import requests
import json


# allows us to get mobile version
user_agent_mobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'

user_agent_desktop = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0'

addon_id = 'plugin.video.PakistaniTV'


def get_image_path(image):
    ''' get image path '''
    image = 'special://home/addons/{id}/resources/images/{image}'.format(
        id=addon_id, image=image)
    return image


def get_remote_data(url, ismobile=True, referer=None):
    ''' fetch website data as mobile or desktop browser'''
    user_agent = user_agent_mobile if ismobile else user_agent_desktop

    headers = {'User-Agent': user_agent}
    if referer:
        headers['Referer'] = referer

    r = requests.get(url, headers=headers)
    return r.content


def is_site_available(url):
    ''' ping site to see if it is up '''

    print 'Checking url: {url}'.format(url=url)

    try:
        r = requests.head(url)
        return r.status_code < 400

    except:
        return False


def clean_post_links(linklist):
    ''' There are a lot of mal-formed links
    e.g. <a href='link1'>part of </a><a href='link1'>text</a>
    This method will merge them into a unique dictionary
    and concatenate texts associated with each url
    '''
    tag_dic = {}

    for li in linklist:
        key = li['href']
        value = li.text

        if value:
            if not (key in tag_dic):
                tag_dic[key] = value
            else:
                tag_dic[key] = tag_dic[key] + ' ' + value

    return tag_dic


def find_host_link(tag_dic):
    '''
    Some post links lead to pages where id is different from host video id
    post link: http://faltulinks.net/media/video.php?id=123
    vid link: http://tune.pk/player/embed_player.php?vid=456

    input: key/value -> link/title
    '''

    # using Yahoo Pipes to do parsing cuz
    # it provides built-in caching and formatting
    parser_url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=411841d418a3c257695b95fa2bc98121&_render=json'

    for key in tag_dic:
        if (key.find('video.php')):
            # fetch page
            r = requests.get(parser_url, params={'urlinput': key})

            # get actual link
            jd = json.loads(r.content)

            if jd['count'] > 0:
                vid_link = jd['value']['items'][0]['src']

                # replace list item
                tag_dic[vid_link] = tag_dic.pop(key)

    return tag_dic
