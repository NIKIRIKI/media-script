import os
import requests
import subprocess

class ThumbnailDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path):
        self.urls = urls
        self.output_dir = output_dir
        self.yt_dlp_path = yt_dlp_path

    def download_content(self):
        try:
            for i, url in enumerate(self.urls):
                self.download_url_content(url, i)
        except Exception as e:
            print(f"Error in download_content: {str(e)}")

    def download_url_content(self, url, i):
        try:
            url_dir = os.path.join(self.output_dir, f'input_preview_{i}')
            os.makedirs(url_dir, exist_ok=True)
            self.download_thumbnail(url, url_dir)
        except Exception as e:
            print(f"Error in download_url_content: {str(e)}")

    def download_thumbnail(self, url, url_dir):
        try:
            command = [self.yt_dlp_path, url, '--get-thumbnail']
            thumbnail_url = subprocess.check_output(command).decode().strip()
            response = requests.get(thumbnail_url)
            with open(os.path.join(url_dir, 'input_preview.jpg'), 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error in download_thumbnail: {str(e)}")
