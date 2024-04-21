import os
import subprocess
from pathlib import Path
import concurrent.futures
import logging


class AudioDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path, ffmpeg_path, audio_format='mp3', download_audio=True):
        self.urls = urls
        self.output_dir = Path(output_dir)
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path
        self.audio_format = audio_format
        self.download_audio_flag = download_audio

    def download_audio(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.process_url, self.urls, range(len(self.urls)))

    def process_url(self, url, i):
        audio_dir = self.output_dir / f'input_audio_{i}'
        audio_dir.mkdir(parents=True, exist_ok=True)
        filename = audio_dir / f'input_audio.{self.audio_format}'
        if not filename.exists():
            self.download_audio_from_url(url, filename)

    def download_audio_from_url(self, url, filename):
        command = [self.yt_dlp_path, url, '-x', '--audio-format', self.audio_format, '-o', str(filename)]
        try:
            subprocess.run(command, check=True)
            logging.info(f'Successfully downloaded {url} to {filename}')
        except Exception as e:
            logging.error(f'Error downloading {url} to {filename}: {e}', exc_info=True)
