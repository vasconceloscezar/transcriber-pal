import os
import subprocess
import asyncio
from colorama import Fore, Style
from tools.timer import Timer


async def convert_video_to_audio(video_path, audio_path):
    if os.path.isfile(audio_path):
        print(
            Fore.YELLOW
            + "Output file already exists. Skipping conversion."
            + Style.RESET_ALL
        )
        return
    timer = Timer()
    timer.start()
    print(Fore.GREEN + "Converting video to audio..." + Style.RESET_ALL)
    command = f"ffmpeg -loglevel warning -hide_banner -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
    subprocess.call(command, shell=True)
    print(Fore.GREEN + "Audio conversion took " + timer.stop() + Style.RESET_ALL)


if __name__ == "__main__":
    video_path = "data/2023_06_27_Namastex-JoshXT.mp4"
    audio_path = "data/2023_06_27_Namastex-JoshXT.mp3"
    asyncio.run(convert_video_to_audio(video_path, audio_path))
