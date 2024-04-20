import os
import subprocess

class VideoTrimmer:
    def __init__(self, urls, output_dir, ffmpeg_path, yt_dlp_path, interval=None, start_time=None, end_time=None, video_format='mp4'):
        self.urls = urls
        self.output_dir = output_dir
        self.interval = self.convert_to_seconds(interval) if interval else None
        self.start_time = self.convert_to_seconds(start_time) if start_time else None
        self.end_time = self.convert_to_seconds(end_time) if end_time else None
        self.ffmpeg_path = ffmpeg_path
        self.yt_dlp_path = yt_dlp_path
        self.video_format = video_format

    @staticmethod
    def convert_to_seconds(time_str):
        try:
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

    def trim_videos(self):
        try:
            for i, url in enumerate(self.urls):
                url_dir = os.path.join(self.output_dir, f'input_video_{i}')
                filename = os.path.join(url_dir, f'input_video.{self.video_format}')
                if os.path.exists(filename):
                    self.trim_video(filename, url)
        except Exception as e:
            print(f"Error in trim_videos: {str(e)}")


    def trim_video(self, filename, url):
        try:
            command = [self.yt_dlp_path, url, '--get-duration']
            video_length = subprocess.check_output(command).decode().strip()
            video_length = self.convert_to_seconds(video_length)

            if self.interval:
                for i in range(0, video_length, self.interval):
                    start_time = i
                    end_time = min(i + self.interval, video_length)
                    self.edit_video(filename, start_time, end_time, i // self.interval)
            elif self.start_time is not None and self.end_time is not None:
                self.edit_video(filename, self.start_time, self.end_time, 0)
        except Exception as e:
            print(f"Error in trim_video: {str(e)}")

    def edit_video(self, filename, start_time, end_time, i):
        try:
            url_dir = os.path.dirname(filename)
            output_filename = os.path.join(url_dir, f"output_{i}.{self.video_format}")
            if self.video_format == 'webm':
                command = [self.ffmpeg_path, '-i', filename, '-ss', str(start_time), '-to', str(end_time), '-c:v', 'libvpx-vp9', '-c:a', 'libopus', '-map_metadata', '-1', output_filename]
            else:
                command = [self.ffmpeg_path, '-i', filename, '-ss', str(start_time), '-to', str(end_time), '-c', 'copy', '-map_metadata', '-1', output_filename]
            subprocess.run(command, check=True)
        except Exception as e:
            print(f"Error in edit_video: {str(e)}")
