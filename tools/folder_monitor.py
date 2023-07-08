import asyncio
import glob
import os
from tools.terminal_operations import print_blue, print_magenta, print_green


class FolderMonitor:
    def __init__(self, folder, file_patterns):
        self.folder = folder
        self.file_patterns = file_patterns
        self.queue = asyncio.PriorityQueue()  # Changed from Queue to PriorityQueue

    async def monitor_folder(self):
        existing_files = await self._get_files_with_priority()
        print_blue(f"Found {len(existing_files)} existing files")

        for file in existing_files:
            await self.queue.put(file)

        print_magenta("Checking for files...")
        while True:
            await asyncio.sleep(1)
            current_files = await self._get_files_with_priority()

            new_files = current_files - existing_files

            for new_file in new_files:
                print_green(f"New file found: {new_file}")
                await self.queue.put(new_file)

            existing_files = current_files

    async def _get_files_with_priority(self):
        current_files = set()
        for pattern in self.file_patterns:
            for file in glob.glob(os.path.join(self.folder, pattern)):
                # Get file modification time as priority
                priority = os.path.getmtime(file)
                # Add to set as (priority, file) tuple
                current_files.add((priority, file))
        return current_files
