from video_scripts.video_downloader import VideoDownloader as vd1
from video_scripts.video_downloader_2 import VideoDownloader as vd2
from video_scripts.video_converter import VideoConverter as vc1
from video_scripts.video_converter_2 import VideoConverter as vc2
from video_scripts.video_trimmer import VideoCutter as vcut
from audio_scripts.audio_downloader import AudioDownloader as ad
from audio_scripts.audio_transcribed import AudioToTextConverter as atc1
from audio_scripts.audio_transcribed_2 import AudioToTextConverter as atc2
from audio_scripts.audio_converter import AudioConverter as ac
from audio_scripts.audio_trimmer import AudioCutter as acut
from image_scripts.get_preview import ThumbnailDownloader as td
from image_scripts.image_converter import ImageConverter as ic
from image_scripts.image_downloader import ImageDownloader as id
from text_scripts.get_description import VideoDescriptionDownloader as vdd
from text_scripts.subtitles_translate import SubtitleTranslator as st



def main():
    interval = "03:00:00" # Интервал для обрезки аудио/видео в формате "hh:mm:ss".(Обрезает целое видео на несколько маленьких кусочков).
    input_dir = "C:/Users/user/Videos/course/test" # Путь к директории для сохранения результатов.
    input_dir2 = "..." # Путь к директории изображений
    # The variable `input_dir3` is storing the directory path where the text descriptions of the videos
    # will be saved. In this case, it is set to `"C:/Users/user/Videos/course/test/input_description_0"`.
    # This directory will be used by the `VideoDescriptionDownloader` class to save the text information
    # about the videos downloaded from the specified URLs.
    input_dir3 = "C:/Users/user/Videos/course/test/input_description_0"
    urls = ["https://www.youtube.com/watch?v=gSUdv8n1q4A"] # Ссылки на видео.
    urls2 = ["...", "..."] # Ссылки на изображения

    model_path = "..." # Путь к языковым моделям vosk для работы аудио транскрибатора (atc2).""

    # Загрузчик видео vd1. Принимает параметры urls - ссылки на видео и input_dir - директория для сохранения видео.
    # Если не работает первый загрузчик видео, то поменяйте vd1 на vd2.
    # video_downloader = vd1(urls=urls, input_dir=input_dir)
    # video_downloader.download_videos()

    # Триммер видео vcut. Принимает параметры input_dir - директория для обрезки видео, interval - интервал для обрезки аудио/видео в формате "hh:mm:ss".
    # Если нужен только 1 кусок видео, то добавьте в класс vcut параметры start_time = "hh:mm:ss" (начало кадра для обрезки видео) и end_time = "hh:mm:ss" (конец кадра для обрезки видео).
    # Для работы нужно предварительно скачать видеоматериал через загрузчик видео vd1 или vd2.
    # video_trimmer = vcut(input_dir=input_dir, interval=interval)
    # video_trimmer.process_videos()

    # Конвертер видео vc1. Принимает параметры input_dir - директория для конвертации видео, output_video_format - формат для конвертации видео. 
    # Для работы нужно предварительно скачать видеоматериал через загрузчик видео vd1 или vd2.
    # Если не работает первый загрузчик видео, то поменяйте vc1 на vc2.
    # video_converter = vc1(input_dir=input_dir, output_video_format="mp4")
    # video_converter.convert_video()

    # Загрузчик аудио ad. Принимает параметры urls - ссылки на аудио и input_dir - директория для сохранения аудио.
    # audio_downloader = ad(input_dir=input_dir, urls=urls)
    # audio_downloader.download_audio()

    # Триммер аудио acut. Принимает параметры input_dir - директория для обрезки аудио, interval - интервал для обрезки аудио/видео в формате "hh:mm:ss".
    # Если нужен только 1 кусок аудио, то добавьте в класс acut параметры start_time = "hh:mm:ss" (начало кадра для обрезки аудио) и end_time = "hh:mm:ss" (конец кадра для обрезки аудио).
    # Для работы нужно предварительно скачать аудиоматериал через загрузчик аудио ad.
    # audio_trimmer = acut(input_dir=input_dir, interval=interval)
    # audio_trimmer.process_audios()

    # Конвертер аудио ac. Принимает параметры input_dir - директория для конвертации аудио, output_audio_format - формат для конвертации аудио.
    # Для работы нужно предварительно скачать аудиоматериал через загрузчик видео ad.
    # audio_converter = ac(input_dir=input_dir, output_audio_format = "wav")
    # audio_converter.convert_audio()

    # Транскрибатор аудио atc1. Принимает параметры input_dir - директория для транскрибации аудио.
    # Для работы нужно предварительно скачать аудиоматериал через загрузчик аудио ad.
    # Если не работает первый транскрибатор аудио, то поменяйте atc1 на atc2. Также в классе atc2 добавьте параметр model_path - Путь к языковым моделям vosk для работы аудио транскрибатора (atc2).
    # audio_transcribed = atc1(input_dir=input_dir)
    # audio_transcribed.convert_audio_to_text()

    # Загрузчик текста vdd. Принимает параметры input_dir - директория для сохранения текстовой информации о видео, urls - ссылки на видеоматериалы.
    # text_description = vdd(input_dir=input_dir, urls=urls)
    # text_description.download_all_descriptions()

    # Переводчик субтитров st. Принимает параметры input_dir - директория для сохранения текстовой информации о видео, to_lang = Выбор языка.
    # subtitles_translate = st(input_dir=input_dir3, to_lang="ru")
    # subtitles_translate.translate_all_subtitles()

    # Загрузчик превью td. Принимает параметры input_dir - директория для сохранения изображения, urls - ссылки на видеоматериалы.
    # image_preview = td(input_dir=input_dir, urls=urls)
    # image_preview.download_content()

    # Загрузчик изображений id. Принимает параметры urls - ссылки на изображения и input_dir - директория для сохранения изображения.
    # image_downloader = id(urls=urls2, input_dir=input_dir)
    # image_downloader.download_images()

    # Конвертер изображений ic. Принимает параметры input_dir - директория для конвертации изображений, output_image_format - формат для конвертации изображения. 
    # image_converter = ic(input_dir=input_dir2, output_image_format="png")
    # image_converter.convert_image()

if __name__ == "__main__":
    main()
