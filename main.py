import argparse
import asyncio
from tools.audio_to_text import convert_audio_to_text
from tools.video_to_audio import convert_video_to_audio

async def main(input_file):
    if not input_file:
        print("No input file provided.")
        return

    if input_file.endswith(".mp3") or input_file.endswith(".wav"):
        await convert_audio_to_text(input_file)
    elif input_file.endswith(".mp4"):
        audio_path = f"{input_file[:-4]}.mp3"
        await convert_video_to_audio(input_file, audio_path)
        await convert_audio_to_text(audio_path)
    else:
        print("Invalid file format. Supported formats are .mp3, .wav, and .mp4.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default="", help="Path to input file")
    args = parser.parse_args()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.input_file))
