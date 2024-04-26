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
from text_scripts.get_description import VideoDescriptionDownloader as vdd


def main():
    start_time = None
    end_time = None
    interval = "00:00:20"
    output_dir = "..."
    urls = ["...", "..."]

    model_path = "..."

    # Загрузчик видео. Принимает параметры urls - ссылки на видео и output_dir - директория для сохранения видео
    # video_downloader = vd1(urls=urls, output_dir=output_dir)
    # video_downloader.download_videos()

    # video_trimmer = vcut(input_dir=output_dir, interval=interval)
    # video_trimmer.process_videos()

    # video_converter = vc1(output_dir=output_dir, output_video_format="mp4")
    # video_converter.convert_video()

    # video_converter = vc2(output_dir=output_dir, output_video_format="mp4")
    # video_converter.convert_video()

    audio_downloader = ad(output_dir=output_dir, urls=urls)
    audio_downloader.download_audio()

    audio_trimmer = acut(input_dir=output_dir, interval=interval, start_time="00:00:00", end_time="00:00:10")
    audio_trimmer.process_audios()

    # audio_transcribed = atc1(output_dir=output_dir)
    # audio_transcribed.convert_audio_to_text()

    # text_description = vdd(output_dir=output_dir, urls=urls)
    # text_description.download_all_descriptions()

    # image_preview = td(output_dir=output_dir, urls=urls)
    # image_preview.download_content()

    


if __name__ == "__main__":
    main()
