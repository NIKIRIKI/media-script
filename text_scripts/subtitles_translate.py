import os
from googletrans import Translator
from langdetect import detect, DetectorFactory
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Ensure consistent results from language detection
DetectorFactory.seed = 0

class SubtitleTranslator:
    def __init__(self, input_dir, to_lang):
        self.input_dir = input_dir
        self.output_dir = os.path.join(input_dir, 'translated_subtitles')
        os.makedirs(self.output_dir, exist_ok=True)
        self.to_lang = to_lang
        self.translator = Translator()

    def translate_all_subtitles(self):
        try:
            files = [f for f in os.listdir(self.input_dir) if f.endswith('.vtt')]
            if not files:
                print("No subtitle files found in the input directory.")
                return
            
            with ThreadPoolExecutor() as executor:
                futures = []
                for file in files:
                    futures.append(executor.submit(self.translate_subtitles, file))
                    
                for _ in tqdm(as_completed(futures), total=len(futures), desc="Translating subtitles"):
                    pass
        except Exception as e:
            print(f"Error in translate_all_subtitles: {str(e)}")

    def translate_subtitles(self, filename):
        try:
            input_file = os.path.join(self.input_dir, filename)
            output_file = os.path.join(self.output_dir, f'translated_{filename}')
            
            with open(input_file, 'r', encoding='utf-8') as f_in:
                lines = f_in.readlines()
            
            # Detect language from non-empty lines
            non_empty_lines = [line for line in lines if line.strip()]
            if not non_empty_lines:
                print(f"No content to translate in file: {filename}")
                return
            
            # Try to detect language from the first non-empty line
            from_lang = 'auto'
            try:
                from_lang = detect(non_empty_lines[0])
            except Exception as e:
                print(f"Error detecting language in file {filename}: {str(e)}")
            
            # Translate line by line
            translated_lines = []
            for line in lines:
                if line.strip():
                    try:
                        translated_line = self.translator.translate(line, src=from_lang, dest=self.to_lang).text
                        translated_lines.append(translated_line)
                    except Exception as e:
                        print(f"Error translating line '{line}': {str(e)}")
                        translated_lines.append(line)  # Fallback to original line in case of error
                else:
                    translated_lines.append(line)
            
            # Write the translated text to the output file
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.writelines(translated_lines)
        
        except Exception as e:
            print(f"Error in translate_subtitles: {str(e)}")

