import os
import subprocess
from tqdm import tqdm

class AudioConverter:
    def __init__(self, output_dir, ffmpeg_path, audio_format, output_audio_format):
        self.output_dir = output_dir
        self.ffmpeg_path = ffmpeg_path
        self.audio_format = audio_format
        self.output_audio_format = output_audio_format
        self.target_format = output_audio_format
        self.sample_rate = 44100
        self.bit_depth = 16

    def convert_audio(self):
        # Check if the ffmpeg executable exists
        if not os.path.exists(self.ffmpeg_path):
            print(f"ffmpeg executable not found at {self.ffmpeg_path}. Please check the path.")
            return

        # Get a list of all directories in the output directory
        directories = [d for d in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, d))]

        # Initialize progress bar
        pbar = tqdm(total=len(directories), ncols=70)

        for i in range(len(directories)):
            # Full path to the source audio file
            input_dir = os.path.join(self.output_dir, f'input_audio_{i}')
            input_file = os.path.join(input_dir, f'input_audio.{self.audio_format}')
            # Check if the input file exists
            if not os.path.exists(input_file):
                print(f"File {input_file} does not exist. Skipping...")
                continue
            # Create the destination directory
            destination_dir = os.path.join(self.output_dir, f'input_conv_audio_{i}')
            os.makedirs(destination_dir, exist_ok=True)
            # Full path to the destination file
            output_file = os.path.join(destination_dir, f'input_conv_audio.{self.output_audio_format}')
            
            # Conversion command
            command = [
                self.ffmpeg_path,
                '-i', input_file,
                '-ar', str(self.sample_rate),
                '-ac', '2',  # Number of audio channels
                '-sample_fmt', f's{self.bit_depth}',  # Sample depth
                output_file
            ]
            try:
                subprocess.run(command, check=True)
                print(f'File {input_file} successfully converted to {output_file}')
            except subprocess.CalledProcessError as e:
                print(f'Error converting file {input_file}: {e}')

            # Update progress bar
            pbar.update(1)

        # Close progress bar
        pbar.close()
