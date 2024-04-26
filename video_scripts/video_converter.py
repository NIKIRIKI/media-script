import os
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from ffmpeg import input, output


class VideoConverter:
    def __init__(self, input_dir, output_video_format, video_bitrate='1000k'):
        self.input_dir = Path(input_dir)
        self.output_video_format = output_video_format
        self.video_bitrate = video_bitrate

    def get_subdirectories(self):
        try:
            for d in self.input_dir.iterdir():
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
                    input_file = next(subdir.glob('*.*'), None)
                    if not input_file:
                        logging.error(f"No input file found in directory: {subdir}")
                        continue

                    destination_dir = self.input_dir / f'input_converted_video_{i}'
                    destination_dir.mkdir(parents=True, exist_ok=True)
                    output_file = destination_dir / f'converted_video.{self.output_video_format}'

                    logging.info(f'Starting conversion of {input_file} to {output_file}')
                    executor.submit(self.run_ffmpeg, input_file, output_file)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def run_ffmpeg(self, input_file, output_file):
        try:
            (
                input(str(input_file))
                .output(str(output_file), b=self.video_bitrate)
                .run()
            )
            logging.info(f'File {input_file} successfully converted to {output_file}')
        except Exception as e:
            logging.error(f'Error converting file {input_file}: {e}')
