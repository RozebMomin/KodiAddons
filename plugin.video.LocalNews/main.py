# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

#http://livestream.com/accounts/14014394/events/4198951/player?autoPlay=true&mute=false
# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {'Atlanta': [{'name': 'Watch My Fox Atlanta LIVE',
                       'thumb': 'http://www.fox5atlanta.com/fox-main-theme/images/color-schemes/waga/apple-touch-icon.png',
                       'video': 'plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=Fox5Atlanta&event_id=2152811&owner_id=4241684&video_id=LIVE',
                       'genre': 'Atlanta'}
                      ],
            'New York': [{'name': 'Watch Fox 5 New York LIVE',
                      'thumb': 'http://www.roomy-tv.com/images/161.png',
                      'video': 'plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=Fox5NewYork&event_id=2592483&owner_id=6372917&video_id=LIVE',
                      'genre': 'New York'}
                     ],
            'Florida': [{'name': 'Watch NBC 2 LIVE',
                      'thumb': 'http://wbbh.images.worldnow.com/images/273803_G.jpg',
                      'video': 'plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=FloridaNBC2&event_id=4105198&owner_id=1140&video_id=LIVE',
                      'genre': 'Florida'}
                     ],
            'Alabama': [{'name': 'Watch WBRC Fox6 LIVE',
                      'thumb': 'http://ftpcontent4.worldnow.com/wbrc/custom/2015/images/hdr_branding.png',
                      'video': 'plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=AlabamaFox6&event_id=3855294&owner_id=12446860&video_id=LIVE',
                      'genre': 'Alabama'}
                     ],
            'Tennessee': [{'name': 'Watch WSMV CH4 LIVE',
                      'thumb': 'https://img.new.livestream.com/accounts/0000000000619a8c/92494261-962d-4761-9367-82fcb6fbcaee_170x170.png',
                      'video': 'plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=TennesseeCH4&event_id=3622128&owner_id=6396556&video_id=LIVE',
                      'genre': 'Tennessee'}
                     ],
            'South Carolina': [{'name': 'Watch WCSC LIVE',
                      'thumb': 'https://img.new.livestream.com/accounts/0000000000a81ab8/66696b3c-d583-47de-b493-f741159d70aa_170x170.png',
                      'video': 'plugin://plugin.video.livestream/?url=%2Flive_now&mode=104&name=SouthCarolinaWCSC&event_id=3600153&owner_id=11016888&video_id=LIVE',
                      'genre': 'South Carolina'}
                     ]}
                     
def get_categories():
    """
    Get the list of video categories.
    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    :return: list
    """
    return VIDEOS.keys()


def get_videos(category):
    """
    Get the list of videofiles/streams.
    Here you can insert some parsing code that retrieves
    the list of videostreams in a given category from some site or server.

    :param category: str
    :return: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Create a list for our items.
    listing = []
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category, thumbnailImage=VIDEOS[category][0]['thumb'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing&category={1}'.format(_url, category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Create a list for our items.
    listing = []
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        #url = '{0}?action=play&video={1}'.format(_url, video['video'])
        url = '{1}'.format(_url, video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
