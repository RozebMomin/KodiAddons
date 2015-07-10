import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os

addon = xbmcaddon.Addon('plugin.video.ZeeTVLive')

util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 'http://dittotv.live-s.cdn.bitgravity.com/cdn-live/_definst_/dittotv/secure/zee_tv_3G.smil/chunklist_w1661535512_b864000.m3u8?e=1436421596&a=US&h=a0965711a254d90af92683009216fe53')