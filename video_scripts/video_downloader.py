import yt_dlp
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self, urls, output_dir):
        self.urls = urls
        self.output_dir = Path(output_dir)

    def download_videos(self):
        with ThreadPoolExecutor() as executor:
            for i, url in enumerate(self.urls):
                executor.submit(self.download_video, url, i)

    def download_video(self, url, i):
        output_dir = self.output_dir / f'input_video_{i}'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'input_video.%(ext)s'
        ydl_opts = {'outtmpl': str(output_file)}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
