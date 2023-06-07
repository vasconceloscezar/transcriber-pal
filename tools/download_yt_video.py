from pytube import YouTube
import asyncio


async def download_youtube_video(url, path):
    try:
        yt = YouTube(url)
        yt.streams.first().download(path)
        print(f"Video downloaded successfully")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # video_path = "data/teste_long.mp4"
    # audio_path = "data/audio.mp3"
    asyncio.run(
        download_youtube_video(
            "https://www.youtube.com/watch?v=rLG68k2blOc", "data/temp"
        )
    )
