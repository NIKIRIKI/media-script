import os
import webbrowser

import video_scripts.video_downloader
import video_scripts.video_downloader_2
import video_scripts.video_converter
import video_scripts.video_converter_2
import audio_scripts.audio_downloader
import audio_scripts.audio_transcribed
import audio_scripts.audio_transcribed_2
import audio_scripts.audio_converter
import audio_scripts.audio_trimmer
import image_scripts.get_preview
import text_scripts.get_description
import video_scripts.video_trimmer


def main():
    start_time = None
    end_time = None
    interval = "00:00:20"
    output_dir = "..."
    urls = ["...", "..."]

    model_path = "..."

    # video_downloader = video_scripts.video_downloader.VideoDownloader(urls=urls, output_dir=output_dir)
    # video_downloader.download_videos()

    # video_trimmer = video_scripts.video_trimmer.VideoCutter(input_dir=output_dir, interval=interval)
    # video_trimmer.process_videos()

    # video_converter = video_scripts.video_converter.VideoConverter(output_dir=output_dir, output_video_format="mp4")
    # video_converter.convert_video()

    # video_converter = video_scripts.video_converter_2.VideoConverter(output_dir=output_dir, output_video_format="mp4")
    # video_converter.convert_video()

    audio_downloader = audio_scripts.audio_downloader.AudioDownloader(output_dir=output_dir, urls=urls)
    audio_downloader.download_audio()

    audio_trimmer = audio_scripts.audio_trimmer.AudioCutter(input_dir=output_dir, interval=interval, start_time="00:00:00", end_time="00:00:10")
    audio_trimmer.process_audios()

    # audio_transcribed = audio_scripts.audio_transcribed.AudioToTextConverter(output_dir=output_dir)
    # audio_transcribed.convert_audio_to_text()

    # text_description = text_scripts.get_description.VideoDescriptionDownloader(output_dir=output_dir, urls=urls)
    # text_description.download_all_descriptions()

    # image_preview = image_scripts.get_preview.ThumbnailDownloader(output_dir=output_dir, urls=urls)
    # image_preview.download_content()

    


if __name__ == "__main__":
    main()

