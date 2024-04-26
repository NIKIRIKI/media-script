import speech_recognition as sr
from tqdm import tqdm
from pathlib import Path
import concurrent.futures
import logging
import ffmpeg

class AudioToTextConverter:
    def __init__(self, input_dir):
        self.input_dir = Path(input_dir)

    def convert_audio_to_text(self):
        directories = [d for d in self.input_dir.iterdir() if d.is_dir() and d.name.startswith('input_audio_')]

        with tqdm(total=len(directories), ncols=70) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.process_directory, d): d for d in directories}
                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)

    def process_directory(self, directory):
        input_file = next(directory.glob('input_audio.*'))
        if not input_file.exists():
            logging.error(f"File {input_file} does not exist. Skipping...")
            return

        audio_format = input_file.suffix.lstrip('.')
        if audio_format != 'wav':
            wav_file = input_file.with_suffix('.wav')
            try:
                ffmpeg.input(str(input_file)).output(str(wav_file), ac=2, ar='44000').run()
                logging.info(f'File {input_file} successfully converted to {wav_file}')
            except ffmpeg.Error as e:
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

        destination_dir = self.input_dir / f'input_text_transcribed_{directory.name.split("_")[-1]}'
        destination_dir.mkdir(parents=True, exist_ok=True)
        output_file = destination_dir / 'transcription.txt'

        with open(output_file, 'w') as f:
            f.write(text)

        logging.info(f'Transcription from {input_file} successfully saved to {output_file}')
