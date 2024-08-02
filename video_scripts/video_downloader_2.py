import requests
from pathlib import Path
import concurrent.futures
import logging


class VideoDownloader:
    def __init__(self, urls, input_dir, video_format='mp4'):
        self.urls = urls
        self.input_dir = Path(input_dir)
        self.video_format = video_format

    def download_content(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.download_url_content, self.urls, range(len(self.urls)))

    def download_url_content(self, url, i):
        url_dir = self.input_dir / f'input_video_{i}'
        url_dir.mkdir(parents=True, exist_ok=True)
        video_filename = url_dir / f'input_video.{self.video_format}'
        if not video_filename.exists():
            self.download_video(url, video_filename)

    def download_video(self, url, filename):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            logging.info(f'Successfully downloaded {url} to {filename}')
        except Exception as e:
            logging.error(f'Error downloading {url} to {filename}: {e}', exc_info=True)
