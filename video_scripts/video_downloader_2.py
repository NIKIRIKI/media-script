import os
import requests

class VideoDownloader:
    def __init__(self, urls, output_dir, video_format='mp4'):
        self.urls = urls
        self.output_dir = output_dir
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
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, stream=True, headers=headers)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            print(f"Error in download_video: {str(e)}")

