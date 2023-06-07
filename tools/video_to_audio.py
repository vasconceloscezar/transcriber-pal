import os
import subprocess
import asyncio


async def convert_video_to_audio(video_path, audio_path):
    command = f"ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    video_path = "data/yt_test.3gpp"
    audio_path = "data/audio.mp3"
    asyncio.run(convert_video_to_audio(video_path, audio_path))
