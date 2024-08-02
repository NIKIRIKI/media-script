import os
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from ffmpeg import input, output

class AudioConverter:
    def __init__(self, input_dir, output_audio_format, audio_bitrate='128k'):
        self.input_dir = Path(input_dir)
        self.output_audio_format = output_audio_format
        self.audio_bitrate = audio_bitrate

    def get_subdirectories(self):
        try:
            for d in self.input_dir.iterdir():
                if d.is_dir():
                    yield d
        except FileNotFoundError as e:
            logging.error(f"Directory not found: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")

    def convert_audio(self):
        try:
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                for i, subdir in enumerate(self.get_subdirectories()):
                    input_file = next(subdir.glob('*.*'), None)
                    if not input_file:
                        logging.error(f"No input file found in directory: {subdir}")
                        continue

                    destination_dir = self.input_dir / f'input_converted_audio_{i}'
                    destination_dir.mkdir(parents=True, exist_ok=True)
                    output_file = destination_dir / f'converted_audio.{self.output_audio_format}'

                    logging.info(f'Starting conversion of {input_file} to {output_file}')
                    executor.submit(self.run_ffmpeg, input_file, output_file)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def run_ffmpeg(self, input_file, output_file):
        try:
            (
                input(str(input_file))
                .output(str(output_file), b=self.audio_bitrate)
                .run()
            )
            logging.info(f'File {input_file} successfully converted to {output_file}')
        except Exception as e:
            logging.error(f'Error converting file {input_file}: {e}')
