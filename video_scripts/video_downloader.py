import yt_dlp
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import logging

class VideoDownloader:
    def __init__(self, urls, input_dir):
        self.urls = urls
        self.input_dir = Path(input_dir)

    def download_videos(self):
        with ThreadPoolExecutor() as executor:
            for i, url in enumerate(self.urls):
                executor.submit(self.download_video, url, i)

    def download_video(self, url, i):
        input_dir = self.input_dir / f'input_video_{i}'
        input_dir.mkdir(parents=True, exist_ok=True)
        output_file = input_dir / 'input_video.%(ext)s'
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best', 
            'outtmpl': str(output_file),
            'socket_timeout': 60  # Increased timeout
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logging.error(f"Error downloading {url}: {e}")
