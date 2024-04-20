import os
import requests
import subprocess

class AudioTrimmer:
    def __init__(self, urls, yt_dlp_path, ffmpeg_path, output_dir, audio_format = 'mp3', interval=None, start_time=None, end_time=None):
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path
        self.urls = urls
        self.audio_format = audio_format
        self.output_dir = output_dir
        self.interval = self.convert_to_seconds(interval) if interval else None
        self.start_time = self.convert_to_seconds(start_time) if start_time else None
        self.end_time = self.convert_to_seconds(end_time) if end_time else None

    @staticmethod
    def convert_to_seconds(time_str):
        try:
            if isinstance(time_str, int):
                return time_str
            time_parts = list(map(int, time_str.split(':')))
            if len(time_parts) == 3:
                h, m, s = time_parts
            elif len(time_parts) == 2:
                h = 0
                m, s = time_parts
            else:
                raise ValueError("Invalid time format")
            return h * 3600 + m * 60 + s
        except Exception as e:
            print(f"Error in convert_to_seconds: {str(e)}")
            return None

    def trim_audios(self):
        try:
            for i, url in enumerate(self.urls):
                url_dir = os.path.join(self.output_dir, f'input_audio_{i}')
                if not os.path.exists(url_dir):
                    os.makedirs(url_dir)
                filename = os.path.join(url_dir, f'input_audio.{self.audio_format}')
                if os.path.exists(filename):
                    self.trim_audio(filename, url, self.interval, self.start_time, self.end_time)
        except Exception as e:
            print(f"Error in trim_audios: {str(e)}")

    def trim_audio(self, filename, url, interval=None, start_time=None, end_time=None):
        try:
            command = [self.yt_dlp_path, url, '--get-duration']
            audio_length = subprocess.check_output(command).decode().strip()
            audio_length = self.convert_to_seconds(audio_length)

            if interval:
                for i in range(0, audio_length, self.convert_to_seconds(interval)):
                    start_time = i
                    end_time = min(i + self.convert_to_seconds(interval), audio_length)
                    self.edit_audio(filename, start_time, end_time, i // self.convert_to_seconds(interval))
            elif start_time is not None and end_time is not None:
                self.edit_audio(filename, self.convert_to_seconds(start_time), self.convert_to_seconds(end_time), 0)
        except Exception as e:
            print(f"Error in trim_audio: {str(e)}")

    def edit_audio(self, filename, start_time, end_time, i):
        try:
            url_dir = os.path.dirname(filename)
            output_filename = os.path.join(url_dir, f"output_{i}.{self.audio_format}")
            command = [self.ffmpeg_path, '-i', filename, '-ss', str(start_time), '-to', str(end_time), '-c', 'copy', '-map_metadata', '-1', output_filename]
            subprocess.run(command, check=True)
        except Exception as e:
            print(f"Error in edit_audio: {str(e)}")
