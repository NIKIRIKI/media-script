from translate import Translator
from langdetect import detect
import os

class SubtitleTranslator:
    def __init__(self, input_dir, to_lang):
        self.input_dir = input_dir
        self.output_dir = os.path.join(input_dir, 'translated_subtitles')
        os.makedirs(self.output_dir, exist_ok=True)
        self.to_lang = to_lang

    def translate_all_subtitles(self):
        try:
            for i in range(len(os.listdir(self.input_dir))):
                self.translate_subtitles(i)
        except Exception as e:
            print(f"Error in translate_all_subtitles: {str(e)}")

    def translate_subtitles(self, i):
        try:
            input_file = os.path.join(self.input_dir, f'subtitles_{i}.vtt')
            output_file = os.path.join(self.output_dir, f'translated_subtitles_{i}.vtt')
            with open(input_file, 'r', encoding='utf-8') as f_in:
                with open(output_file, 'w', encoding='utf-8') as f_out:
                    for line in f_in:
                        for line in f_in:
                            line = line.strip()  # Удалить пробелы в начале и конце строки
                            if line:  # Проверить, не является ли строка пустой
                                from_lang = detect(line)
                                translator = Translator(from_lang=from_lang, to_lang=self.to_lang)
                                translation = translator.translate(line)
                                f_out.write(translation + '\n')

        except Exception as e:
            print(f"Error in translate_subtitles: {str(e)}")
