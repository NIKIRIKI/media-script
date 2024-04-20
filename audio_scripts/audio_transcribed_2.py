import os
import subprocess
import json
from vosk import Model, KaldiRecognizer
from tqdm import tqdm

class AudioToTextConverter:
    def __init__(self, output_dir, ffmpeg_path, audio_format, model_path):
        self.output_dir = output_dir
        self.ffmpeg_path = ffmpeg_path
        self.audio_format = audio_format
        self.model_path = model_path

    def convert_audio_to_text(self):
        # Check if the ffmpeg executable exists
        if not os.path.exists(self.ffmpeg_path):
            print(f"ffmpeg executable not found at {self.ffmpeg_path}. Please check the path.")
            return

        # Load Vosk model
        if not os.path.exists(self.model_path):
            print(f"Vosk model not found at {self.model_path}. Please check the path.")
            return
        model = Model(self.model_path)

        # Get a list of all directories in the output directory
        directories = [d for d in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, d)) and d.startswith('input_audio_')]

        # Initialize progress bar
        pbar = tqdm(total=len(directories), ncols=70)

        for directory in directories:
            # Full path to the source audio file
            input_file = os.path.join(self.output_dir, directory, f'input_audio.{self.audio_format}')
            
            # Check if the input file exists
            if not os.path.exists(input_file):
                print(f"File {input_file} does not exist. Skipping...")
                continue

            # If the audio is not in wav format, convert it to wav
            if self.audio_format != 'wav':
                wav_file = input_file.rsplit('.', 1)[0] + '.wav'
                command = [
                    self.ffmpeg_path,
                    '-i', input_file,
                    '-ac', '1',  # Make it mono channel
                    '-ar', '44000',  # Set sample rate to 16000 Hz
                    wav_file
                ]
                try:
                    subprocess.run(command, check=True)
                    print(f'File {input_file} successfully converted to {wav_file}')
                except subprocess.CalledProcessError as e:
                    print(f'Error converting file {input_file} to wav: {e}')
                    continue
                input_file = wav_file

            # Convert audio to text using Vosk
            recognizer = KaldiRecognizer(model, 16000)
            text = ""
            with open(input_file, 'rb') as f:
                while True:
                    data = f.read(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text += result['text'] + " "
                result = json.loads(recognizer.FinalResult())
                text += result['text']

            # Create the destination directory
            destination_dir = os.path.join(self.output_dir, f'input_text_transcribed_{directory.split("_")[-1]}')
            os.makedirs(destination_dir, exist_ok=True)

            # Full path to the destination file
            output_file = os.path.join(destination_dir, 'transcription.txt')

            # Save the transcribed text to the output file
            with open(output_file, 'w') as f:
                f.write(text)

            print(f'Transcription from {input_file} successfully saved to {output_file}')

            # Update progress bar
            pbar.update(1)

        # Close progress bar
        pbar.close()
