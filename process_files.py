import asyncio
from tools.constants import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
from tools.folder_monitor import FolderMonitor
from tools.terminal_operations import clear_terminal, print_cyan
from tools.transcriptor_manager import TranscriptionManager


if __name__ == "__main__":
    FILE_PATTERNS = AUDIO_EXTENSIONS + VIDEO_EXTENSIONS
    FOLDER_TO_MONITOR = r"Z:\files_to_transcript"

    clear_terminal()
    print_cyan(f"Monitoring folder: {FOLDER_TO_MONITOR}")

    folder_monitor = FolderMonitor(FOLDER_TO_MONITOR, FILE_PATTERNS)
    transcription_manager = TranscriptionManager(folder_monitor.queue)

    # Run both coroutines concurrently
    asyncio.run(
        asyncio.gather(
            folder_monitor.monitor_folder(), transcription_manager.run_transcriber()
        )
    )
