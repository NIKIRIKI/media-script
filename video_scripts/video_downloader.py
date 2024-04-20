import os
import requests
import subprocess

class VideoDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path, ffmpeg_path, resolution='best', video_format='mp4'):
        self.urls = urls
        self.output_dir = output_dir
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path
        self.resolution = resolution
        self.video_format = video_format

    def download_content(self):
        try:
            for i, url in enumerate(self.urls):
                self.download_url_content(url, i)
        except Exception as e:
            print(f"Error in download_content: {str(e)}")

    def download_url_content(self, url, i):
        try:
            url_dir = os.path.join(self.output_dir, f'input_video_{i}')
            os.makedirs(url_dir, exist_ok=True)
            video_filename = os.path.join(url_dir, f'input_video.{self.video_format}')
            if not os.path.exists(video_filename):
                self.download_video(url, video_filename)
        except Exception as e:
            print(f"Error in download_url_content: {str(e)}")

    def download_video(self, url, filename):
        try:
            command = [self.yt_dlp_path, url, '-f', f'{self.resolution}/{self.video_format}', '-o', filename]
            subprocess.run(command, check=True)
        except Exception as e:
            print(f"Error in download_video: {str(e)}")
