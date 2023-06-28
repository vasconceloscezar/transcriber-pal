import asyncio
import os
import glob
import shutil
from datetime import datetime
from tools.audio_to_text import AudioTranscriber
from tools.video_to_audio import convert_video_to_audio


VIDEO_EXTENSIONS = [
    "*.mp4",
    "*.mov",
    "*.avi",
    "*.mkv",
    "*.flv",
    "*.wmv",
    "*.webm",
]

AUDIO_EXTENSIONS = [
    "*.mp3",
    "*.wav",
    "*.ogg",
    "*.txt",
    "*.m4a",
    "*.flac",
    "*.aac",
    "*.opus",
]


def need_to_convert_file(input_file):
    file_extension = os.path.splitext(input_file)[1]
    video_extensions_stripped = [
        extension.replace("*", "") for extension in VIDEO_EXTENSIONS
    ]
    if file_extension in video_extensions_stripped:
        return True
    return False


async def monitor_folder(folder, file_patterns):
    # Create a queue for new files
    queue = asyncio.Queue()

    existing_files = set()
    for pattern in file_patterns:
        existing_files.update(glob.glob(os.path.join(folder, pattern)))
    print(f"Found {len(existing_files)} existing files")

    # Add the initial existing files to the queue
    for file in existing_files:
        await queue.put(file)

    print("Starting monitoring...")
    while True:
        await asyncio.sleep(1)
        current_files = set()
        for pattern in file_patterns:
            current_files.update(glob.glob(os.path.join(folder, pattern)))

        new_files = current_files - existing_files

        for new_file in new_files:
            print(f"New file found: {new_file}")
            # Add new files to the queue
            await queue.put(new_file)

        existing_files = current_files

        # If there are items in the queue, start transcribing
        if not queue.empty():
            print("Starting transcription tasks...")
            # Get an item from the queue and start transcribing
            asyncio.create_task(run_transcriber(queue))


async def run_transcriber(queue):
    while True:
        try:
            # Get a file from the queue
            input_file = await queue.get()

            print(f"Starting transcription for file: {input_file}")

            if not input_file:
                print("No input file provided.")
                return

            # Get the current date in YYYY-MM-DD format
            date_str = datetime.now().strftime("%Y-%m-%d")

            # Get the basename of the file without extension
            base_name = os.path.splitext(os.path.basename(input_file))[0]

            # Construct the output directory name
            output_dir = os.path.join(
                r"Z:/files_to_transcript/transcriptions", f"{date_str}-{base_name}"
            )

            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            audio_path = input_file
            print(f"Input file: {input_file}")
            if need_to_convert_file(input_file):
                audio_path = input_file[:-4] + ".mp3"
                await convert_video_to_audio(input_file, audio_path)
            else:
                print(
                    "Invalid file format. Supported formats are: mp3, wav, ogg, m4a, flac, aac, opus, mp4, mov, avi, mkv, flv, wmv, webm"
                )

            transcriber = AudioTranscriber(audio_path)
            await transcriber.transcribe_audio(output_dir)

            # Move the files to the output directory only after the transcription is complete
            if need_to_convert_file(input_file):
                # Move the original video file to the output directory
                shutil.move(input_file, output_dir)

                # Also move the converted .mp3 file to the output directory
                shutil.move(audio_path, output_dir)
            else:
                # Move the input file (which is an audio file) to the output directory
                shutil.move(input_file, output_dir)

            queue.task_done()
        except Exception as ex:
            print(f"Error transcribing file: {ex}")


if __name__ == "__main__":
    FILE_PATTERNS = AUDIO_EXTENSIONS + VIDEO_EXTENSIONS

    FOLDER_TO_MONITOR = r"Z:\files_to_transcript"
    print(f"Monitoring folder: {FOLDER_TO_MONITOR}")
    asyncio.run(monitor_folder(FOLDER_TO_MONITOR, FILE_PATTERNS))
