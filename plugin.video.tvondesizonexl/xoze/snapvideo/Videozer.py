'''
Created on Dec 22, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import base64
import binascii
import urllib
try:
    import json
except ImportError:
    import simplejson as json


def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.videozer.com/images/logo.jpg')
    video_host.set_name('Videozer')
    return video_host


def retrieveVideoInfo(video_id):
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://www.videozer.com/player_control/settings.php?v=' + video_id + '&fv=v1.1.45'
        jsonObj = json.load(urllib.urlopen(video_info_link))
                
        key1 = jsonObj["cfg"]["environment"]["rkts"]
        key2 = jsonObj["cfg"]["login"]["pepper"]
        key3 = jsonObj["cfg"]["ads"]["lightbox2"]["time"]
        
        values = binascii.unhexlify(decrypt(jsonObj["cfg"]["login"]["spen"], jsonObj["cfg"]["login"]["salt"], 950569)).split(';')
        spn = http.parse_url_params(values[0])
        outk = http.parse_url_params(values[1])
        ikey = getikey(int(outk["ik"]))
        
        urlKey = ''
        for spnkey in spn:
            spnval = spn[spnkey]
            if spnval == '1':
                cypher = jsonObj["cfg"]["info"]["sece2"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey, ln=256) + '&'
            if spnval == '2':
                cypher = jsonObj["cfg"]["ads"]["g_ads"]["url"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey) + '&'
            if spnval == '3':
                cypher = jsonObj["cfg"]["ads"]["g_ads"]["type"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey, 26, 25431, 56989, 93, 32589, 784152) + '&'
            if spnval == '4':
                cypher = jsonObj["cfg"]["ads"]["g_ads"]["time"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey, 82, 84669, 48779, 32, 65598, 115498) + '&'
            if spnval == '5':
                cypher = jsonObj["cfg"]["login"]["euno"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key2, ikey, 10, 12254, 95369, 39, 21544, 545555) + '&'
            if spnval == '6':
                cypher = jsonObj["cfg"]["login"]["sugar"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key3, ikey, 22, 66595, 17447, 52, 66852, 400595) + '&'
        
        urlKey = urlKey + "start=0"
        
        video_link = ""
        for videoStrm in jsonObj["cfg"]["quality"]:
            if videoStrm["d"]:
                video_link = str(base64.b64decode(videoStrm["u"]))
        if video_link == "":
            video_info.set_video_stopped(False)
            raise Exception("VIDEO_STOPPED")
        video_link = video_link + '&' + urlKey
        
        video_info.set_name(jsonObj["cfg"]["info"]["video"]["title"])
        video_info.set_thumb_image(jsonObj["cfg"]["environment"]["thumbnail"])
        video_info.set_stopped(False)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
    except:
        video_info.set_video_stopped(True)
    return video_info


def getikey(i):
    if i == 1:
        return 215678
    elif i == 2:
        return 516929
    elif i == 3:
        return 962043
    elif i == 4:
        return 461752
    elif i == 5:
        return 141994
    else:
        return -1


def hex2bin(hexStr):
    binaryStr = ''
    for c in hexStr:
        binaryStr = binaryStr + bin(int(c, 16))[2:].zfill(4)
    return binaryStr


def bin2hex(binStr):
    hexStr = ''
    for i in range(len(binStr) - 4, -1, -4):
        oneBinStr = binStr[i:i + 4]
        hexStr = hexStr + hex(int(oneBinStr.zfill(4), 2))[2:]
    hexStr = hexStr[::-1]
    return hexStr


def decrypt(cypher, key1, key2, keySetA_1=11, keySetA_2=77213, keySetA_3=81371, keySetB_1=17, keySetB_2=92717, keySetB_3=192811, ln=None):
    
    C = list(hex2bin(cypher))
    if ln is None:
        ln = len(C) * 2
    B = int(ln * 1.5) * [None]
    
    for i in range(0, int(ln * 1.5)):
        key1 = (key1 * keySetA_1 + keySetA_2) % keySetA_3
        key2 = (key2 * keySetB_1 + keySetB_2) % keySetB_3
        B[i] = (key1 + key2) % int(ln * 0.5)

    x = y = z = 0
    
    for i in range(ln, -1 , -1):
        x = B[i]
        y = i % int(ln * 0.5)
        z = C[x]
        C[x] = C[y]
        C[y] = z

    for i in range(0, int(ln * 0.5), 1):
        C[i] = str(int(C[i]) ^ int(B[i + ln]) & 1)

    binStr = ''.join(C)
    return bin2hex(binStr)

