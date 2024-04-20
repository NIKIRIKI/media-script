import os
import subprocess

class VideoConverter:
    def __init__(self, output_dir, ffmpeg_path, video_format, output_video_format):
        self.output_dir = output_dir
        self.ffmpeg_path = ffmpeg_path
        self.video_format = video_format
        self.output_video_format = output_video_format
        self.target_format = output_video_format
        self.video_bitrate = '1000k'

    def convert_video(self):
        # Get a list of all subdirectories in the output directory
        subdirectories = [d for d in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, d))]

        for i, subdir in enumerate(subdirectories):
            # Full path to the source video file
            input_file = os.path.join(self.output_dir, f'input_video_{i}/input_video.{self.video_format}')
            # Create a directory for the converted file
            destination_dir = os.path.join(self.output_dir, f'input_conv_video_{i}')
            os.makedirs(destination_dir, exist_ok=True)
            # Full path to the output file
            output_file = os.path.join(destination_dir, f'converted_video.{self.output_video_format}')

            # Command for conversion
            command = [
                self.ffmpeg_path,
                '-i', input_file,
                '-b:v', self.video_bitrate,
                output_file
            ]

            try:
                subprocess.run(command, check=True)
                print(f'File {input_file} successfully converted to {output_file}')
            except subprocess.CalledProcessError as e:
                print(f'Error converting file {input_file}: {e}')