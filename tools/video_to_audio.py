import os
import subprocess


async def convert_video_to_audio(video_path, audio_path):
    command = f"ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    video_path = 'data/video.mp4'
    audio_path = 'data/audio.mp3'
    convert_video_to_audio(video_path, audio_path)
