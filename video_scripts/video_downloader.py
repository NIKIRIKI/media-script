import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path="yt-dlp-master/yt-dlp.exe"):
        self.urls = urls
        self.output_dir = Path(output_dir)
        self.yt_dlp_path = yt_dlp_path

    def download_videos(self):
        with ThreadPoolExecutor() as executor:
            for i, url in enumerate(self.urls):
                executor.submit(self.download_video, url, i)

    def download_video(self, url, i):
        output_dir = self.output_dir / f'input_video_{i}'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'input_video.%(ext)s'
        command = [self.yt_dlp_path, url, '-o', str(output_file)]
        subprocess.run(command, check=True)
