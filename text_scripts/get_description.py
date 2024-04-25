import os
import yt_dlp

class VideoDescriptionDownloader:
    def __init__(self, urls, output_dir):
        self.urls = urls
        self.output_dir = output_dir

    def download_all_descriptions(self):
        try:
            for i, url in enumerate(self.urls):
                self.download_url_content(url, i)
        except Exception as e:
            print(f"Error in download_all_descriptions: {str(e)}")

    def download_url_content(self, url, i):
        try:
            url_dir = os.path.join(self.output_dir, f'input_description_{i}')
            os.makedirs(url_dir, exist_ok=True)
            self.download_description(url, url_dir)
            self.download_title(url, url_dir)
            self.download_subtitles(url, url_dir)
        except Exception as e:
            print(f"Error in download_url_content: {str(e)}")

    def download_description(self, url, url_dir):
        try:
            ydl_opts = {
                'skip_download': True,
                'outtmpl': os.path.join(url_dir, 'description.txt')
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                description = info_dict.get('description', None)
                with open(os.path.join(url_dir, 'description.txt'), 'w', encoding='utf-8') as f:
                    f.write(description)
        except Exception as e:
            print(f"Error in download_description: {str(e)}")

    def download_title(self, url, url_dir):
        try:
            ydl_opts = {
                'skip_download': True,
                'outtmpl': os.path.join(url_dir, 'title.txt')
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', None)
                with open(os.path.join(url_dir, 'title.txt'), 'w', encoding='utf-8') as f:
                    f.write(title)
        except Exception as e:
            print(f"Error in download_title: {str(e)}")

    def download_subtitles(self, url, url_dir):
        try:
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'subtitlesformat': 'vtt',
                'outtmpl': os.path.join(url_dir, 'subtitles.vtt')
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error in download_subtitles: {str(e)}")
