import os
import subprocess
import speech_recognition as sr
from tqdm import tqdm

class AudioToTextConverter:
    def __init__(self, output_dir, ffmpeg_path, audio_format):
        self.output_dir = output_dir
        self.ffmpeg_path = ffmpeg_path
        self.audio_format = audio_format

    def convert_audio_to_text(self):
        if not os.path.exists(self.ffmpeg_path):
            print(f"ffmpeg executable not found at {self.ffmpeg_path}. Please check the path.")
            return

        directories = [d for d in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, d)) and d.startswith('input_audio_')]
        pbar = tqdm(total=len(directories), ncols=70)

        for directory in directories:
            input_file = os.path.join(self.output_dir, directory, f'input_audio.{self.audio_format}')
            
            if not os.path.exists(input_file):
                print(f"File {input_file} does not exist. Skipping...")
                continue

            if self.audio_format != 'wav':
                wav_file = input_file.rsplit('.', 1)[0] + '.wav'
                command = [
                    self.ffmpeg_path,
                    '-i', input_file,
                    '-ac', '2',
                    '-ar', '44000',
                    wav_file
                ]
                try:
                    subprocess.run(command, check=True)
                    print(f'File {input_file} successfully converted to {wav_file}')
                except subprocess.CalledProcessError as e:
                    print(f'Error converting file {input_file} to wav: {e}')
                    continue
                input_file = wav_file

            recognizer = sr.Recognizer()
            with sr.AudioFile(input_file) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='ru-RU')
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    continue

            destination_dir = os.path.join(self.output_dir, f'input_text_transcribed_{directory.split("_")[-1]}')
            os.makedirs(destination_dir, exist_ok=True)
            output_file = os.path.join(destination_dir, 'transcription.txt')

            with open(output_file, 'w') as f:
                f.write(text)

            print(f'Transcription from {input_file} successfully saved to {output_file}')
            pbar.update(1)

        pbar.close()
