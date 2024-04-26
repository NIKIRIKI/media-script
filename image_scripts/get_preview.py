import os
import yt_dlp

class ThumbnailDownloader:
    def __init__(self, urls, input_dir):
        self.urls = urls
        self.input_dir = input_dir

    def download_content(self):
        try:
            for i, url in enumerate(self.urls):
                self.download_url_content(url, i)
        except Exception as e:
            print(f"Error in download_content: {str(e)}")

    def download_url_content(self, url, i):
        try:
            url_dir = os.path.join(self.input_dir, f'input_preview_{i}')
            os.makedirs(url_dir, exist_ok=True)
            self.download_thumbnail(url, url_dir)
        except Exception as e:
            print(f"Error in download_url_content: {str(e)}")

    def download_thumbnail(self, url, url_dir):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(url_dir, 'input_preview.jpg'),
                'writethumbnail': True,
                'skip_download': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error in download_thumbnail: {str(e)}")
