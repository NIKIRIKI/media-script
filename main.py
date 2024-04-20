import os
import requests
import subprocess
import video_scripts.video_downloader
import video_scripts.video_downloader_2
import video_scripts.video_converter
import video_scripts.video_converter_2
import video_scripts.video_trimmer
import audio_scripts.audio_downloader
import audio_scripts.audio_trimmer
import audio_scripts.audio_transcribed
import audio_scripts.audio_transcribed_2
import audio_scripts.audio_converter
import image_scripts.get_preview
import text_scripts.get_description

def get_user_input(prompt, conversion_func=str):
    try:
        return conversion_func(input(prompt))
    except ValueError:
        print("Invalid input. Please try again.")
        return get_user_input(prompt, conversion_func)

def main():
    start_time = None
    end_time = None
    interval = "00:02:00"
    output_dir = "C:/Users/user/Videos/course/video_2"
    urls = ["https://www.youtube.com/shorts/PWeFx2IpIbY"]
    resolution = "best"
    video_format = "mp4"
    audio_format = "mp3"
    output_audio_format = "wav"
    output_video_format = "mkv"
    download_audio = True
    download_video = True
    clean_audio = False

    yt_dlp_path = "yt-dlp-master/yt-dlp.exe"
    ffmpeg_path = "ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"
    model_path = "vosk_model/model-ru"

    video_downloader = video_scripts.video_downloader.VideoDownloader(urls=urls, output_dir=output_dir, yt_dlp_path=yt_dlp_path, ffmpeg_path=ffmpeg_path, resolution=resolution, video_format=video_format)
    video_downloader.download_content()

    # video_downloader_2 = video_scripts.video_downloader_2.VideoDownloader(urls=urls, output_dir=output_dir, video_format=video_format)
    # video_downloader_2.download_content()

    # video_trimmer = video_scripts.video_trimmer.VideoTrimmer(urls=urls, output_dir=output_dir, ffmpeg_path=ffmpeg_path, yt_dlp_path=yt_dlp_path, interval=interval, start_time=start_time, end_time=end_time, video_format=video_format)
    # video_trimmer.trim_videos()

    # video_converter = video_scripts.video_converter.VideoConverter(output_dir=output_dir, ffmpeg_path=ffmpeg_path, video_format = video_format, output_video_format = output_video_format)
    # video_converter.convert_video()

    # video_converter = video_scripts.video_converter_2.VideoConverter(output_dir=output_dir, video_format = video_format, output_video_format = output_video_format)
    # video_converter.convert_video()

    audio_downloader = audio_scripts.audio_downloader.AudioDownloader(urls = urls, output_dir = output_dir, yt_dlp_path = yt_dlp_path, ffmpeg_path = ffmpeg_path, audio_format=audio_format, download_audio=download_audio)
    audio_downloader.download_audio()

    # audio_trimmer = audio_scripts.audio_trimmer.AudioTrimmer(urls=urls, audio_format=audio_format, output_dir=output_dir, ffmpeg_path=ffmpeg_path, yt_dlp_path=yt_dlp_path, interval=interval, start_time=start_time, end_time=end_time)
    # audio_trimmer.trim_audios()

    # audio_converter = audio_scripts.audio_converter.AudioConverter(output_dir=output_dir, ffmpeg_path=ffmpeg_path, audio_format = audio_format, output_audio_format = output_audio_format)
    # audio_converter.convert_audio()

    # audio_transcribed = audio_scripts.audio_transcribed.AudioToTextConverter(output_dir=output_dir, audio_format=audio_format, ffmpeg_path=ffmpeg_path)
    # audio_transcribed.convert_audio_to_text()

    audio_transcribed = audio_scripts.audio_transcribed_2.AudioToTextConverter(output_dir=output_dir, audio_format=audio_format, ffmpeg_path=ffmpeg_path, model_path=model_path)
    audio_transcribed.convert_audio_to_text()

    # text_description = text_scripts.get_description.VideoDescriptionDownloader(urls=urls, output_dir=output_dir, yt_dlp_path=yt_dlp_path)
    # text_description.download_all_descriptions()

    # image_preview = image_scripts.get_preview.ThumbnailDownloader(urls=urls, output_dir=output_dir, yt_dlp_path=yt_dlp_path)
    # image_preview.download_content()

if __name__ == "__main__":
    main()
