import requests
import subprocess
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


class VideoDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path, ffmpeg_path, resolution='best', input_video_format='mp4', max_retries=3,
                 max_workers=5):
        self.urls = urls
        self.output_dir = Path(output_dir)
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path
        self.resolution = resolution
        self.input_video_format = input_video_format
        self.max_retries = max_retries
        self.max_workers = max_workers
        logging.basicConfig(level=logging.INFO)

    def download_content(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.download_url_content, url, i): url for i, url in enumerate(self.urls)}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error downloading {url}: {str(e)}")

    def download_url_content(self, url, i):
        url_dir = self.output_dir / f'input_video_{i}'
        url_dir.mkdir(parents=True, exist_ok=True)
        video_filename = url_dir / f'input_video.{self.input_video_format}'
        if not video_filename.exists():
            self.download_video_with_retries(url, video_filename)

    def download_video_with_retries(self, url, filename):
        for i in range(self.max_retries):
            try:
                self.download_video(url, filename)
                return
            except (requests.exceptions.RequestException, subprocess.CalledProcessError) as e:
                logging.error(f"Error in download_video: {str(e)}, retrying...")
                time.sleep(i * 2)
        logging.error(f"Failed to download video after {self.max_retries} attempts")

    def download_video(self, url, filename):
        command = [self.yt_dlp_path, url, '-f', f'{self.resolution}/{self.input_video_format}', '-o', str(filename)]
        subprocess.run(command, check=True)
