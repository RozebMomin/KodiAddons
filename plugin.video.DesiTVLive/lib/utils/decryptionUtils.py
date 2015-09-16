# -*- coding: utf-8 -*-

import pyDes
import urllib
import re

from regexUtils import parseTextToGroups

from javascriptUtils import JsFunctions, JsUnpacker, JsUnpackerV2, JsUnpacker95High, JsUnwiser, JsUnwiser2, JsUnIonCube, JsUnFunc, JsUnPP, JsUnPush


def encryptDES_ECB(data, key):
    data = data.encode()
    k = pyDes.des(key, pyDes.ECB, IV=None, pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data)
    assert k.decrypt(d, padmode=pyDes.PAD_PKCS5) == data
    return d

def gAesDec(data, key):
    import mycrypt
    return mycrypt.decrypt(key,data)

def aesDec(data, key):
    from base64 import b64decode
    try:
        from Crypto.Cipher import AES
    except ImportError:
        import pyaes as AES
    iv = 16 * '\x00'
    cipher = AES.new(b64decode(key), AES.MODE_CBC, IV=iv)
    padded_plaintext = cipher.decrypt(b64decode(data))
    padding_len = ord(padded_plaintext[-1])
    return padded_plaintext[:-padding_len]

def encryptJimey(data):
    result = encryptDES_ECB(data,"PASSWORD").encode('base64').replace('/','').strip()
    return result

# used by 24cast
def destreamer(s):
    #remove all but[0-9A-Z]
    string = re.sub("[^0-9A-Z]", "", s.upper())
    result = ""
    nextchar = ""
    for i in range(0,len(string)-1):
        nextchar += string[i]
        if len(nextchar) == 2:
            result += ntos(int(nextchar,16))
            nextchar = ""
    return result

def ntos(n):
    n = hex(n)[2:]
    if len(n) == 1:
        n = "0" + n
    n = "%" + n
    return urllib.unquote(n)

def doDemystify(data):

    #init jsFunctions and jsUnpacker
    jsF = JsFunctions()
    jsU = JsUnpacker()
    jsUV2 =JsUnpackerV2()
    jsUW = JsUnwiser()
    jsUW2 = JsUnwiser2()
    jsUI = JsUnIonCube()
    jsUF = JsUnFunc()
    jsUP = JsUnPP()
    jsU95 = JsUnpacker95High()
    JsPush = JsUnPush()

    # replace NUL
    data = data.replace('\0','')


    # unescape
    r = re.compile('a1=["\'](%3C(?=[^\'"]*%\w\w)[^\'"]+)["\']')
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, urllib.unquote_plus(quoted))
    
    
    r = re.compile('unescape\(\s*["\']((?=[^\'"]*%\w\w)[^\'"]+)["\']')
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, urllib.unquote_plus(quoted))
    
    r = re.compile('unescape\(\s*["\']((?=[^\'"]*\\u00)[^\'"]+)["\']')
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, quoted.decode('unicode-escape'))
       

    # n98c4d2c
    if 'function n98c4d2c(' in data:
        gs = parseTextToGroups(data, ".*n98c4d2c\(''\).*?'(%[^']+)'.*")
        if gs != None and gs != []:
            data = data.replace(gs[0], jsF.n98c4d2c(gs[0]))

    # o61a2a8f
    if 'function o61a2a8f(' in data:
        gs = parseTextToGroups(data, ".*o61a2a8f\(''\).*?'(%[^']+)'.*")
        if gs != None and gs != []:
            data = data.replace(gs[0], jsF.o61a2a8f(gs[0]))

    # RrRrRrRr
    if 'function RrRrRrRr(' in data:
        r = re.compile("(RrRrRrRr\(\"(.*?)\"\);)</SCRIPT>", re.IGNORECASE + re.DOTALL)
        gs = r.findall(data)
        if gs != None and gs != []:
            for g in gs:
                data = data.replace(g[0], jsF.RrRrRrRr(g[1].replace('\\','')))

    # hp_d01
    if 'function hp_d01(' in data:
        r = re.compile("hp_d01\(unescape\(\"(.+?)\"\)\);//-->")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, jsF.hp_d01(g))

    # ew_dc
    if 'function ew_dc(' in data:
        r = re.compile("ew_dc\(unescape\(\"(.+?)\"\)\);</SCRIPT>")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, jsF.ew_dc(g))

    # pbbfa0
    if 'function pbbfa0(' in data:
        r = re.compile("pbbfa0\(''\).*?'(.+?)'.\+.unescape")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, jsF.pbbfa0(g))


    # util.de
    if 'Util.de' in data:
        r = re.compile("Util.de\(unescape\(['\"](.+?)['\"]\)\)")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g,g.decode('base64'))

    # 24cast
    if 'destreamer(' in data:
        r = re.compile("destreamer\(\"(.+?)\"\)")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, destreamer(g))

    # JS P,A,C,K,E,D
    if jsU.containsPacked(data):
        data = jsU.unpackAll(data)
        
    escape_again=False
    #if still exists then apply v2
    if jsUV2.containsPacked(data):
        data = jsUV2.unpackAll(data)
        escape_again=True
        
    if jsU95.containsPacked(data):
        data = jsU95.unpackAll(data)
        escape_again=True

    # JS W,I,S,E
    if jsUW.containsWise(data):
        data = jsUW.unwiseAll(data)
        escape_again=True
        
    if jsUW2.containsWise(data):
        data = jsUW2.unwiseAll(data)
        escape_again=True

    # JS IonCube
    if jsUI.containsIon(data):
        data = jsUI.unIonALL(data)
        escape_again=True
        
    # Js unFunc
    if jsUF.cointainUnFunc(data):
        data = jsUF.unFuncALL(data)
        escape_again=True
    
    if jsUP.containUnPP(data):
        data = jsUP.UnPPAll(data)
        escape_again=True
        
    if JsPush.containUnPush(data):
        data = JsPush.UnPush(data)

    # unescape again
    if escape_again:
        data = doDemystify(data)
    return data

    
