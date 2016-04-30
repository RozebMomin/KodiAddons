import resources.lib.util as util


class Host():
    def __init__(self, server, label, thumb=''):
        self.server = server
        self.label = label
        self.__thumb = thumb

    @property
    def thumb(self):
        if self.__thumb:
            self.__thumb = util.get_image_path(self.__thumb)
        return self.__thumb


''' Resolvable Hosts '''
dailymotion = Host('dailymotion.com', 'Daily Motion', 'dailymotion.png')
facebook = Host('facebook.com', 'Facebook', 'facebook.png')
hostingbulk = Host('hostingbulk.com', 'Hosting Bulk')
nowvideo = Host('nowvideo.eu', 'Now Video', 'nowvideo.png')
putlocker = Host('putlocker.com', 'PutLocker', 'putlocker.png')
tunepk = Host('tune.pk', 'Tune PK', 'tunepk.jpg')
videoweed = Host('videoweed.es', 'Video Weed', 'videoweed.jpg')
youtube = Host('youtube.com', 'Youtube', 'youtube.png')
novamov = Host('novamov.com', 'Novamov', 'novamov.jpg')
movshare = Host('movshare.net', 'Movshare', 'movshare.png')
videotanker = Host('videotanker.co', 'VideoTanker', 'videotanker.png')
