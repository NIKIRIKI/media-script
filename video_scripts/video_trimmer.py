import os
import subprocess
import ffmpeg

class VideoCutter:
    def __init__(self, input_dir, interval, video_format):
        self.input_dir = input_dir
        self.interval = self.converts_to_seconds(interval)
        self.video_format = video_format

    def converts_to_seconds(self, interval_str):
        h, m, s = map(int, interval_str.split(':'))
        return h * 3600 + m * 60 + s

    def get_video_duration(self, video_path):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", video_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return float(result.stdout)

    def cut_video(self):
        for i in range(10):
            video_dir = os.path.join(self.input_dir, f'input_video_{i}')
            video_path = os.path.join(video_dir, f'input_video.{self.video_format}')
            duration = self.get_video_duration(video_path)
            for j in range(0, int(duration), self.interval):
                output_path = os.path.join(video_dir, f'video_cut_{j}.{self.video_format}')
                ffmpeg.input(video_path).output(output_path, ss=j, t=self.interval, c='copy').run()
