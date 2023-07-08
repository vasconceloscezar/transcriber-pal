import asyncio
import os
import subprocess
from tools.terminal_operations import print_green, print_yellow
from tools.timer import Timer


class AudioVideoConverter:
    @staticmethod
    async def convert_video_to_audio(video_path, audio_path):
        if os.path.isfile(audio_path):
            print_yellow("Output file already exists. Skipping conversion.")
            return
        timer = Timer()
        timer.start()
        print_green("Converting video to audio...")
        command = f"ffmpeg -loglevel warning -hide_banner -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
        process = await asyncio.create_subprocess_shell(command)
        await process.communicate()
        print_green("Audio conversion took " + timer.stop())
