import re
import resources.lib.util as util


class Part():
    '''
    part holds part title and list of associated media.
    media list consists of host & video id tuples.
    these will be resolved later as I am unable to
    pass HostedMediaFile objects between function calls
    (they simply end up as type lists and need to be redone)
    '''

    def __init__(self, partnum, host, vid, text):
        self.partnum = partnum
        self.text = text
        self.media = [(host, vid)]
        #print 'Part initialized: {part}'.format(part=text)

    def add_media(self, host, vid):
        self.media.append((host, vid))


class Post():
    __warningmsg = '{addon}: **WARNING** No {item} found for {text}'
    regex_find_promo = re.compile('\(?[pP](?:romo|review)\)?')
    regex_find_parts = re.compile('[pP]art\s*(\d+)')
    regex_match_string = re.compile('(\w+\.\w+)(?:\/(?:embed|player)|\?)')

    def __init__(self, matchstr):
        self.parts = {}
        self.__matchstr = matchstr

    def __get_part_text(self, partnum):
        if partnum > 0:
            return 'Part {partnum}'.format(partnum=partnum)
        return 'Single link'

    #def __get_media_file(self, host, vid, text):
    #    '''
    #    resolve media file url
    #    '''
    #    import urlresolver
    #    return urlresolver.HostedMediaFile(
    #        host=host.server,
    #        media_id=vid,
    #        title=text)

    def __get_video_id(self, url, vidstr):
        '''
        get video id from url
        '''
        v = url.find(vidstr)
        vid = None
        if (v > 0):
            vid = url[v+len(vidstr):]
        return vid

    def __get_match_string(self, text):
        '''
        get match string for host mapping
        e.g. tube.php -> youtube
        '''
        m = self.regex_match_string.findall(text)
        match = None
        if m:
            match = m[0]
        return match

    def __get_part_number(self, text):
        '''
        get part number from text.
        Single link is Part 0
        Ignore 'promo' links
        '''
        if self.regex_find_promo.findall(text):
            return None
        else:
            p = self.regex_find_parts.findall(text)
            if p:
                return int(p[0])
            return 0

    def add_link(self, posturl, urltext):
        '''
        parse links from forum post
        add to local parts dictionary
        '''
        # parse text to get part number
        partnum = self.__get_part_number(urltext)
        if partnum is not None:

            # parse posturl to get matchstr
            match = self.__get_match_string(posturl)
            if match:
                #print 'Match string: {match}'.format(match=match)

                # get host from local match string dictionary
                host, vidstr = self.__matchstr.get(match) or (None, None)
                if host:
                    #print 'Host found: {host}, {vidstr}'.format(
                    #    host=host.label, vidstr=vidstr)

                    # get video id
                    vid = self.__get_video_id(posturl, vidstr)
                    if vid:
                        #print 'Video ID: {vid}'.format(vid=vid)

                        text = self.__get_part_text(partnum)
                        #print 'part title: {text}'.format(text=text)

                        # add to parts dictionary
                        part = self.parts.get(partnum, None)
                        if part:
                            ''' append media to existing part '''
                            part.add_media(host, vid)
                        else:
                            ''' add new part to new part number '''
                            self.parts[partnum] = Part(partnum, host, vid, text)
                    else:
                        print self.__warningmsg.format(
                            addon=util.addon_id, item='video id', text=posturl)
                else:
                    print self.__warningmsg.format(
                        addon=util.addon_id, item='host', text=posturl)
            else:
                print self.__warningmsg.format(
                    addon=util.addon_id, item='match', text=posturl)
        else:
            print self.__warningmsg.format(
                addon=util.addon_id, item='partnum',
                text=urltext.encode(
                    'utf-8', 'ignore') + ' - ' + posturl.encode(
                    'utf-8', 'ignore'))
