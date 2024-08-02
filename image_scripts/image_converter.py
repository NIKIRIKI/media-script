import os
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image


class ImageConverter:
    def __init__(self, input_dir, output_image_format):
        self.input_dir = Path(input_dir)
        self.output_image_format = output_image_format

    def get_files(self):
        try:
            for f in self.input_dir.iterdir():
                if f.is_file():
                    yield f
        except FileNotFoundError as e:
            logging.error(f"Directory not found: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")

    def convert_image(self):
        try:
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                for i, input_file in enumerate(self.get_files()):
                    destination_dir = self.input_dir / f'input_converted_image_{i}'
                    destination_dir.mkdir(parents=True, exist_ok=True)
                    output_file = destination_dir / f'converted_image.{self.output_image_format}'

                    logging.info(f'Starting conversion of {input_file} to {output_file}')
                    executor.submit(self.run_pil, input_file, output_file)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def run_pil(self, input_file, output_file):
        try:
            with Image.open(str(input_file)) as img:
                img.save(str(output_file))
            logging.info(f'File {input_file} successfully converted to {output_file}')
        except Exception as e:
            logging.error(f'Error converting file {input_file}: {e}')
