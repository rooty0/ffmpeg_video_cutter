from pytube import YouTube
import os

class YTDownloader:
    def __init__(self, url, resolution):
        self.url = url
        self.resolution = resolution
        self.yt = YouTube(str(url))

    def download(self):
        itag = self.get_resolution()
        stream = self.yt.streams.get_by_itag(itag)
        file_name = "".join(ch for ch in self.yt.title if ch.isalnum()) + '.mp4' # remove special characteres.
        stream.download(filename=file_name)
        print(f'\n"{self.yt.title}" Vídeo Downloaded!')

    def get_resolution(self):
        if self.resolution == 'low':
            itag = 18
        elif self.resolution == 'medium':
            itag = 22
        elif self.resolution == 'high':
            itag = 137
        else:
            itag = 18
        return itag
    
    def get_lenght(self):
        print(f'Length of vídeo: {self.yt.length}')
