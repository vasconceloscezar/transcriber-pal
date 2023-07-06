# from pytube import YouTube

import asyncio
import glob
import sys


async def download_youtube_video(url, path):
    import yt_dlp

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{path}%(title)s.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


if __name__ == "__main__":
    # Get argument from command line to download video from URL
    # if there's argument use url from arg, if not use default defined here
    if len(sys.argv) > 1:
        urls = sys.argv[1]
    else:
        urls = [
            "https://youtu.be/lohjN6av_Ns",
            "https://youtu.be/GXx4FWCwb2I",
            "https://youtu.be/taMTnqNBFSc",
            "https://youtu.be/k_PkjHX1SAM",
            "https://youtu.be/BqXuRlXCsQg",
            "https://youtu.be/CfTX1Nw-6XY",
            "https://youtu.be/PM5si7kbBDE",
            "https://youtu.be/fIsvW4VfkI0",
            "https://youtu.be/aoD3GhG8bk8",
            "https://youtu.be/7_HigF0v5aI",
            "https://youtu.be/zv-hXXeuSqw",
            "https://youtu.be/NSY3K72F64A",
            "https://youtu.be/MIDi1_d3V38",
            "https://youtu.be/CqVkm-IKZ1s",
            "https://youtu.be/wzsL24-gFmg",
            "https://youtu.be/0CkPUUmAw8g",
            "https://youtu.be/7TCVjGQ-JhE",
            "https://youtu.be/fvndrk3R2qI",
            "https://youtu.be/I2S9y0ZpHok",
            "https://youtu.be/kCOkDMMt4t4",
            "https://youtu.be/bgH59B4M5xg",
            "https://youtu.be/3PiIWtTvsEU",
            "https://youtu.be/unai5Qf_Hq8",
            "https://youtu.be/OVDR_6W4-i0",
            "https://youtu.be/LCF2lmF29Xs",
            "https://youtu.be/h9dz8sxCv3Y",
            "https://youtu.be/NkqAtn085dw",
            "https://youtu.be/F_AxPa-AJTM",
            "https://youtu.be/PyFbpBr4YXk",
            "https://youtu.be/toSHUaroRZc",
            "https://youtu.be/NEGTqRqtr2o",
            "https://youtu.be/vTIUOK4wzjw",
            "https://youtu.be/8cCU_rLhNFM",
            "https://youtu.be/dk69uFnwB8Q",
        ]

    # video_path = "data/teste_long.mp4"
    # audio_path = "data/audio.mp3"
    # asyncio.run(download_youtube_video(urls, "data/yt_downloaded/"))

    # read all videos downloaded and trim their title
    videos = glob.glob("data/yt_downloaded/*.mp4")
    videos = [video.replace("data/yt_downloaded\\", "") for video in videos]
    videos = [video.replace(".mp4", "") for video in videos]
    print(f"Videos: {videos}")
