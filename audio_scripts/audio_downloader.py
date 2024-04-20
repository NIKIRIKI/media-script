import os
import subprocess
import requests

class AudioDownloader:
    def __init__(self, urls, output_dir, yt_dlp_path, ffmpeg_path, audio_format='mp3', download_audio=True):
        self.urls = urls
        self.output_dir = output_dir
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path
        self.audio_format = audio_format
        self.download_audio_flag = download_audio

    def download_audio(self):
        for i, url in enumerate(self.urls):
            audio_dir = os.path.join(self.output_dir, f'input_audio_{i}')
            os.makedirs(audio_dir, exist_ok=True)
            filename = os.path.join(audio_dir, f'input_audio' + '.' + self.audio_format)
            try:
                command = [self.yt_dlp_path, url, '-x', '--audio-format', self.audio_format, '-o', filename]
                subprocess.run(command, check=True)
            except Exception as e:
                print(f"Error in download_audio: {str(e)}")
