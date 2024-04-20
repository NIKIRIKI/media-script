from moviepy.editor import VideoFileClip
import os

class VideoConverter:
    def __init__(self, output_dir, video_format, output_video_format):
        self.output_dir = output_dir
        self.video_format = video_format
        self.output_video_format = output_video_format

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

            try:
                clip = VideoFileClip(input_file)
                clip.write_videofile(output_file, codec='libx264')
                print(f'File {input_file} successfully converted to {output_file}')
            except Exception as e:
                print(f'Error converting file {input_file}: {e}')
