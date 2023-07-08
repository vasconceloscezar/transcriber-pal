import asyncio
import glob
import os
from terminal_operations import print_blue, print_magenta, print_green


class FolderMonitor:
    def __init__(self, folder, file_patterns):
        self.folder = folder
        self.file_patterns = file_patterns
        self.queue = asyncio.Queue()

    async def monitor_folder(self):
        existing_files = self._get_files()
        print_blue(f"Found {len(existing_files)} existing files")

        for file in existing_files:
            await self.queue.put(file)

        print_magenta("Checking for files...")
        while True:
            await asyncio.sleep(1)
            current_files = self._get_files()

            new_files = current_files - existing_files

            for new_file in new_files:
                print_green(f"New file found: {new_file}")
                await self.queue.put(new_file)

            existing_files = current_files

    def _get_files(self):
        current_files = set()
        for pattern in self.file_patterns:
            current_files.update(glob.glob(os.path.join(self.folder, pattern)))
        return current_files
