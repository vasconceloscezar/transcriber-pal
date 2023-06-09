import asyncio
import shutil
from tools.constants import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
from tools.folder_monitor import FolderMonitor
from tools.terminal_operations import clear_terminal, print_blue, print_cyan, print_red
from tools.transcriptor_manager import TranscriptionManager


async def main():
    FILE_PATTERNS = AUDIO_EXTENSIONS + VIDEO_EXTENSIONS
    FOLDER_TO_MONITOR = r"Z:\files_to_transcript"

    clear_terminal()
    print_cyan(f"Monitoring folder: {FOLDER_TO_MONITOR}")

    folder_monitor = FolderMonitor(FOLDER_TO_MONITOR, FILE_PATTERNS)
    transcription_manager = TranscriptionManager(folder_monitor.queue)

    monitor_task = asyncio.create_task(folder_monitor.monitor_folder())
    transcriber_task = asyncio.create_task(transcription_manager.run_transcriber())

    tasks = [monitor_task, transcriber_task]

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print_red("Program stopped by user.")
        for task in tasks:
            task.cancel()
        await asyncio.gather(
            *tasks, return_exceptions=True
        )  # Gather the cancel calls, ignoring exceptions
        # Here, add your cleanup routine
        TEMP_FOLDER = "tools/temp"  # Replace with your actual temp folder path
        shutil.rmtree(TEMP_FOLDER, ignore_errors=True)

        print_red("Temp folder cleared.")
        print_blue("Bye!")
    finally:
        await transcription_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
