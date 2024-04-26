from moviepy.editor import VideoFileClip
from pathlib import Path
import logging
import concurrent.futures

class VideoConverter:
    def __init__(self, input_dir, output_video_format):
        self.input_dir = Path(input_dir)
        self.output_video_format = output_video_format

    def convert_video(self):
        subdirectories = [d for d in self.input_dir.iterdir() if d.is_dir()]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.process_subdir, subdirectories)

    def process_subdir(self, subdir):
        input_files = list(subdir.glob('input_video.*'))

        if not input_files:
            logging.error(f'No input video file found in {subdir}')
            return

        input_file = input_files[0]
        destination_dir = self.input_dir / f'{subdir.name}_conv'
        destination_dir.mkdir(exist_ok=True)
        output_file = destination_dir / f'converted_video.{self.output_video_format}'

        try:
            clip = VideoFileClip(str(input_file))
            clip.write_videofile(str(output_file), codec='libx264')
            logging.info(f'File {input_file} successfully converted to {output_file}')
        except Exception as e:
            logging.error(f'Error converting file {input_file}: {e}', exc_info=True)
