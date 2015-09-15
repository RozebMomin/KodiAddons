import xbmcaddon, util
import subprocess
from subprocess import call
import json
import os
import requests
from bs4 import BeautifulSoup
import re

addon = xbmcaddon.Addon('plugin.video.UpdateDesiTV')

xbmc.executebuiltin(UpdateAddonRepos, True)
