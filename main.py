import argparse
import asyncio
from tools.audio_to_text import transcribe_audio
from tools.video_to_audio import convert_video_to_audio

def check_file_is_audio_or_video(input_file):
    video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
    audio_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".flac" , ".aac" , ".opus"]
    if input_file.endswith(tuple(audio_extensions)):
        return "audio"
    elif input_file.endswith(tuple(video_extensions)):
        return "video"
    else:
        return None
    
async def main(input_file):
    if not input_file:
        print("No input file provided.")
        return
    file_type = check_file_is_audio_or_video(input_file)
    if file_type == "audio":
        await transcribe_audio(input_file)
    elif file_type == "video":
        audio_path = input_file[:-4] + ".mp3"  # Define the output audio path
        await convert_video_to_audio(input_file, audio_path)  # Provide audio_path as argument
        await transcribe_audio(audio_path)
    else: 
        print("Invalid file format. Supported formats are: mp3, wav, ogg, m4a, flac, aac, opus, mp4, mov, avi, mkv, flv, wmv, webm")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default="", help="Path to input file")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.input_file))
