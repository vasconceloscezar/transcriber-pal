# from pytube import YouTube

import asyncio
import sys


async def download_youtube_video(url, path):
    import yt_dlp

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{path}%(title)s.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    # Get argument from command line to download video from URL
    # if there's argument use url from arg, if not use default defined here
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.youtube.com/watch?v=8cCU_rLhNFM"

    # video_path = "data/teste_long.mp4"
    # audio_path = "data/audio.mp3"
    asyncio.run(download_youtube_video(url, "data/temp/"))
