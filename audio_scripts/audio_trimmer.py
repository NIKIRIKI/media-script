import os
import subprocess
import ffmpeg

class AudioCutter:
    def __init__(self, input_dir, interval, audio_format):
        self.input_dir = input_dir
        self.interval = self.converts_to_seconds(interval)
        self.audio_format = audio_format

    def converts_to_seconds(self, interval_str):
        h, m, s = map(int, interval_str.split(':'))
        return h * 3600 + m * 60 + s

    def get_audio_duration(self, audio_path):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", audio_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return float(result.stdout)

    def cut_audio(self):
        for i in range(10):
            audio_dir = os.path.join(self.input_dir, f'input_audio_{i}')
            audio_path = os.path.join(audio_dir, f'input_audio.{self.audio_format}')
            duration = self.get_audio_duration(audio_path)
            for j in range(0, int(duration), self.interval):
                output_path = os.path.join(audio_dir, f'audio_cut_{j}.{self.audio_format}')
                ffmpeg.input(audio_path).output(output_path, ss=j, t=self.interval, c='copy').run()
