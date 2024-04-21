import os
import subprocess
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


class VideoConverter:
    def __init__(self, output_dir, ffmpeg_path, output_video_format, input_video_format='mp4', video_bitrate='1000k'):
        self.output_dir = Path(output_dir)
        self.ffmpeg_path = ffmpeg_path
        self.input_video_format = input_video_format
        self.output_video_format = output_video_format
        self.video_bitrate = video_bitrate

    def get_subdirectories(self):
        try:
            for d in self.output_dir.iterdir():
                if d.is_dir():
                    yield d
        except FileNotFoundError as e:
            logging.error(f"Directory not found: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")

    def convert_video(self):
        try:
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                for i, subdir in enumerate(self.get_subdirectories()):
                    input_file = self.output_dir / f'input_video_{i}' / f'input_video.{self.input_video_format}'
                    if not input_file.exists():
                        logging.error(f"Input file does not exist: {input_file}")
                        continue

                    destination_dir = self.output_dir / f'input_converted_video_{i}'
                    destination_dir.mkdir(parents=True, exist_ok=True)
                    output_file = destination_dir / f'converted_video.{self.output_video_format}'

                    command = [
                        self.ffmpeg_path,
                        '-i', str(input_file),
                        '-b:v', self.video_bitrate,
                        str(output_file)
                    ]

                    logging.info(f'Starting conversion of {input_file} to {output_file}')
                    executor.submit(self.run_command, command, input_file, output_file)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    @staticmethod
    def run_command(command, input_file, output_file):
        try:
            subprocess.run(command, check=True)
            logging.info(f'File {input_file} successfully converted to {output_file}')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error converting file {input_file}: {e}')
        except PermissionError as e:
            logging.error(f'Permission denied: {e}')
