'''
Created on Apr 30, 2015

@author: jchirag
'''

#from xoze.snapvideo import VideoHost
import logging
import re

from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_HD_720, STREAM_QUAL_SD
from xoze.utils import http, encoders


VIDEO_HOST_NAME = 'letwatch'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://letwatch.us.com/images/logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    # Old Method
    #import urlresolver
    #videoUrl =  'http://letwatch.us/embed-' + str(video_id) + '-595x430.html'
    #media = urlresolver.HostedMediaFile(url=videoUrl, title='')   

    #New method to get 720links
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)

    try:
        video_link = 'http://letwatch.us/embed-' + str(video_id) + '-595x430.html'
        html = http.HttpClient().get_html_content(url=video_link)
        paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(html)
        print paramSet
        if len(paramSet) > 0:
            video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
            
            img_data = re.compile(r"image:\'(.+?)\'").findall(video_info_link)
            if len(img_data) == 1:
                video.set_thumb_image(img_data[0])
            video_link = re.compile(r"file:\'(.+?)\'").findall(video_info_link)[0]
        else:
            html = html.replace(' ', '')
            html = html.replace('\'', '"')
            try:
                video_link = 'http' + re.compile('file:"http(.+?)m3u8"').findall(html)[0] + 'm3u8'
            except:
                video_link = 'http' + re.compile('file:"http(.+?)mp4"').findall(html)[0] + 'mp4'
            img_link = re.compile('image:"(.+?)"').findall(html)[0]
            video.set_thumb_image(img_link)
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)

    except:
        video.set_stopped(True)
    return video