import os
from datetime import datetime
from terminal_operations import (
    print_blue,
    print_red,
    print_green,
    print_magenta,
    print_yellow,
)
from file_operations import move_file, is_file_audio, is_file_video
from tools.audio_transcription import AudioTranscription
from tools.audio_video_converter import AudioVideoConverter


class TranscriptionManager:
    def __init__(self, queue):
        self.queue = queue

    async def run_transcriber(self):
        while True:
            try:
                # Get a file from the queue
                input_file = await self.queue.get()

                print_blue(f"Starting transcription for file: {input_file}")

                if not input_file:
                    print_red("No input file provided.")
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
                print_green(f"Input file: {input_file}")
                if is_file_video(input_file):
                    audio_path = input_file[:-4] + ".mp3"
                    await AudioVideoConverter.convert_video_to_audio(
                        input_file, audio_path
                    )
                elif not is_file_audio(input_file):
                    self.queue.task_done()
                    print_yellow(f"File type not supported: {input_file}")
                    continue

                await AudioTranscription.transcribe_audio(audio_path, output_dir)

                if is_file_video(input_file):
                    move_file(input_file, output_dir)
                    move_file(audio_path, output_dir)
                else:
                    move_file(input_file, output_dir)

                self.queue.task_done()
                print_magenta("Checking for files...")

            except Exception as ex:
                print_red(f"Error transcribing file: {ex}")
