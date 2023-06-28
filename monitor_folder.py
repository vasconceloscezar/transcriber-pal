import os
import glob
import time
import argparse
import asyncio

from tools.audio_to_text import AudioTranscriber
from tools.video_to_audio import convert_video_to_audio


def need_to_convert_file(input_file):
    VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
    # audio_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".opus"]
    if input_file.endswith(tuple(VIDEO_EXTENSIONS)):
        return True
    return False


def monitor_folder(folder, file_patterns):
    existing_files = set()
    for pattern in file_patterns:
        existing_files.update(glob.glob(os.path.join(folder, pattern)))
    print(f"Found {len(existing_files)} existing files")
    print("Starting monitoring...")
    while True:
        time.sleep(1)
        current_files = set()
        for pattern in file_patterns:
            current_files.update(glob.glob(os.path.join(folder, pattern)))

        new_files = current_files - existing_files

        for new_file in new_files:
            print(f"New file found: {new_file}")
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(run_transcriber(new_file))

        existing_files = current_files


async def run_transcriber(input_file):
    print(f"Starting transcription for file: {input_file}")
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


video_extensions = [
    "*.mp4",
    "*.mov",
    "*.avi",
    "*.mkv",
    "*.flv",
    "*.wmv",
    "*.webm",
]
audio_extensions = [
    "*.mp3",
    "*.wav",
    "*.ogg",
    "*.txt",
    "*.m4a",
    "*.flac",
    "*.aac",
    "*.opus",
]
FILE_PATTERNS = audio_extensions + video_extensions
FOLDER_TO_MONITOR = r"Z:\files_to_transcript"
print(f"Monitoring folder: {FOLDER_TO_MONITOR}")
monitor_folder(FOLDER_TO_MONITOR, FILE_PATTERNS)
