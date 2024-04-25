import os
import subprocess
import ffmpeg
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class AudioCutter:
    def __init__(self, input_dir, interval, start_time=None, end_time=None):
        self.input_dir = Path(input_dir)
        self.interval = self.converts_to_seconds(interval)
        self.start_time = self.converts_to_seconds(start_time) if start_time else None
        self.end_time = self.converts_to_seconds(end_time) if end_time else None

    def converts_to_seconds(self, interval_str):
        try:
            h, m, s = map(int, interval_str.split(':'))
            return h * 3600 + m * 60 + s
        except ValueError:
            logging.error(f"Invalid interval format: {interval_str}. Expected format: HH:MM:SS")

    def get_audio_duration(self, audio_path):
        try:
            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                     "format=duration", "-of",
                                     "default=noprint_wrappers=1:nokey=1", str(audio_path)],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            return float(result.stdout)
        except Exception as e:
            logging.error(f"Error occurred while getting audio duration for {audio_path}: {e}")

    def cut_audio(self, audio_path, audio_dir):
        if not audio_path.exists():
            logging.error(f"Audio path does not exist: {audio_path}")
            return
        duration = self.get_audio_duration(audio_path)
        if duration is None:
            return
        audio_format = audio_path.suffix.lstrip('.')
        if self.start_time is not None and self.end_time is not None:
            output_path = audio_dir / f'audio_cut_{self.start_time}_{self.end_time}{audio_path.suffix}'
            try:
                ffmpeg.input(str(audio_path)).output(str(output_path), ss=self.start_time, t=self.end_time-self.start_time, c='copy').run()
                logging.info(f"Audio cut from {self.start_time} to {self.end_time} seconds saved as {output_path}")
            except ffmpeg.Error as e:
                logging.error(f"Error occurred while cutting audio {audio_path} from {self.start_time} to {self.end_time} seconds: {e}")
        else:
            for j in range(0, int(duration), self.interval):
                output_path = audio_dir / f'audio_cut_{j}{audio_path.suffix}'
                try:
                    ffmpeg.input(str(audio_path)).output(str(output_path), ss=j, t=self.interval, c='copy').run()
                    logging.info(f"Audio cut from {j} to {j+self.interval} seconds saved as {output_path}")
                except ffmpeg.Error as e:
                    logging.error(f"Error occurred while cutting audio {audio_path} from {j} to {j+self.interval} seconds: {e}")

    def process_audios(self):
        with ThreadPoolExecutor() as executor:
            for i in range(10):
                audio_dir = self.input_dir / f'input_audio_{i}'
                audio_path = next(audio_dir.glob('*'))  # Get the first file in the directory
                executor.submit(self.cut_audio, audio_path, audio_dir)
