import json
from vosk import Model, KaldiRecognizer
from tqdm import tqdm
from pathlib import Path
import concurrent.futures
import logging
import ffmpeg


class AudioToTextConverter:
    def __init__(self, input_dir, model_path):
        self.input_dir = Path(input_dir)
        self.model_path = model_path

    def convert_audio_to_text(self):
        if not Path(self.model_path).exists():
            logging.error(f"Vosk model not found at {self.model_path}. Please check the path.")
            return
        model = Model(self.model_path)

        directories = [d for d in self.input_dir.iterdir() if d.is_dir() and d.name.startswith('input_audio_')]

        with tqdm(total=len(directories), ncols=70) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.process_directory, d, model): d for d in directories}
                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)

    def process_directory(self, directory, model):
        input_file = next(directory.glob('input_audio.*'))
        if not input_file.exists():
            logging.error(f"File {input_file} does not exist. Skipping...")
            return

        if input_file.suffix != '.wav':
            wav_file = input_file.with_suffix('.wav')
            try:
                ffmpeg.input(str(input_file)).output(str(wav_file), ac=1, ar='44000').run()
                logging.info(f'File {input_file} successfully converted to {wav_file}')
            except ffmpeg.Error as e:
                logging.error(f'Error converting file {input_file} to wav: {e}', exc_info=True)
                return
            input_file = wav_file

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

        destination_dir = self.input_dir / f'input_text_transcribed_{directory.name.split("_")[-1]}'
        destination_dir.mkdir(parents=True, exist_ok=True)

        output_file = destination_dir / 'transcription.txt'

        with open(output_file, 'w') as f:
            f.write(text)

        logging.info(f'Transcription from {input_file} successfully saved to {output_file}')
