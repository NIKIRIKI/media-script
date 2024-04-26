import concurrent.futures
import logging
from pathlib import Path
import yt_dlp


class AudioDownloader:
    def __init__(self, urls, input_dir, audio_format='mp3'):
        self.urls = urls
        self.input_dir = Path(input_dir)
        self.audio_format = audio_format

    def download_audio(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.process_url, self.urls, range(len(self.urls)))

    def process_url(self, url, i):
        audio_dir = self.input_dir / f'input_audio_{i}'
        audio_dir.mkdir(parents=True, exist_ok=True)
        filename = audio_dir / f'input_audio.{self.audio_format}'
        if not filename.exists():
            self.download_audio_from_url(url, filename)

    def download_audio_from_url(self, url, filename):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(filename),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format,
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logging.info(f'Successfully downloaded {url} to {filename}')
        except Exception as e:
            logging.error(f'Error downloading {url} to {filename}: {e}', exc_info=True)
