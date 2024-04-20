import os
import subprocess

class VideoDescriptionDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path):
        self.urls = urls
        self.output_dir = output_dir
        self.yt_dlp_path = yt_dlp_path

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
        except Exception as e:
            print(f"Error in download_url_content: {str(e)}")

    def download_description(self, url, url_dir):
        try:
            command = [self.yt_dlp_path, url, '--get-description']
            description = subprocess.check_output(command).decode('utf-8', 'ignore').strip()
            with open(os.path.join(url_dir, 'input_description.txt'), 'w', encoding='utf-8') as f:
                f.write(description)
        except Exception as e:
            print(f"Error in download_description: {str(e)}")
