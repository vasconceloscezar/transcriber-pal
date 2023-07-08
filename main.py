import argparse
import asyncio
from tools.audio_to_text import AudioTranscriber
from tools.audio_video_converter import AudioVideoConverter
from tools.file_operations import get_file_basename, is_file_video


async def transcribe_file(input_file: str):
    if not input_file:
        print("No input file provided.")
        return

    # check if the file needs to be converted to audio
    if is_file_video(input_file):
        audio_path = get_file_basename(input_file)
        await AudioVideoConverter().convert_video_to_audio(input_file, audio_path)
    else:
        audio_path = input_file

    # Transcribe the audio file
    transcriber = AudioTranscriber(audio_path)
    await transcriber.transcribe_audio()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default="", help="Path to input file")
    args = parser.parse_args()

    asyncio.run(transcribe_file(args.input_file))
