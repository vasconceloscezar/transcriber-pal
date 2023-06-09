import argparse
import asyncio
from tools.audio_to_text import AudioTranscriber
from tools.video_to_audio import convert_video_to_audio


def need_to_convert_file(input_file):
    video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
    # audio_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".opus"]
    if input_file.endswith(tuple(video_extensions)):
        return True
    return False


async def main(input_file):
    if not input_file:
        print("No input file provided.")
        return

    # file_type = check_file_is_audio_or_video(input_file)
    audio_path = input_file
    if need_to_convert_file(input_file):
        audio_path = input_file[:-4] + ".mp3"
        await convert_video_to_audio(input_file, audio_path)
    else:
        print(
            "Invalid file format. Supported formats are: mp3, wav, ogg, m4a, flac, aac, opus, mp4, mov, avi, mkv, flv, wmv, webm"
        )

    transcriber = AudioTranscriber(audio_path)
    await transcriber.transcribe_audio()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default="", help="Path to input file")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.input_file))
