import subprocess
import speech_recognition as sr
from tqdm import tqdm
from pathlib import Path
import concurrent.futures
import logging


class AudioToTextConverter:
    def __init__(self, output_dir, ffmpeg_path, audio_format):
        self.output_dir = Path(output_dir)
        self.ffmpeg_path = ffmpeg_path
        self.audio_format = audio_format

    def convert_audio_to_text(self):
        if not Path(self.ffmpeg_path).exists():
            logging.error(f"ffmpeg executable not found at {self.ffmpeg_path}. Please check the path.")
            return

        directories = [d for d in self.output_dir.iterdir() if d.is_dir() and d.name.startswith('input_audio_')]

        with tqdm(total=len(directories), ncols=70) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.process_directory, d): d for d in directories}
                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)

    def process_directory(self, directory):
        input_file = directory / f'input_audio.{self.audio_format}'
        if not input_file.exists():
            logging.error(f"File {input_file} does not exist. Skipping...")
            return

        if self.audio_format != 'wav':
            wav_file = input_file.with_suffix('.wav')
            command = [
                self.ffmpeg_path,
                '-i', str(input_file),
                '-ac', '2',
                '-ar', '44000',
                str(wav_file)
            ]
            try:
                subprocess.run(command, check=True)
                logging.info(f'File {input_file} successfully converted to {wav_file}')
            except subprocess.CalledProcessError as e:
                logging.error(f'Error converting file {input_file} to wav: {e}', exc_info=True)
                return
            input_file = wav_file

        recognizer = sr.Recognizer()
        with sr.AudioFile(str(input_file)) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='ru-RU')
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech Recognition service; {e}")
                return

        destination_dir = self.output_dir / f'input_text_transcribed_{directory.name.split("_")[-1]}'
        destination_dir.mkdir(parents=True, exist_ok=True)
        output_file = destination_dir / 'transcription.txt'

        with open(output_file, 'w') as f:
            f.write(text)

        logging.info(f'Transcription from {input_file} successfully saved to {output_file}')
