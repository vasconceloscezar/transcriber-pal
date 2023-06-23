import os
import shutil
import subprocess
import whisper
import asyncio
import glob
import torch
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, Style
from pydub import AudioSegment
from tools.timer import Timer


class AudioTranscriber:
    def __init__(self, audio_path, model="small", delete_chunks=True):
        self.audio_path = audio_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cpu":
            print(Fore.RED + "No GPU detected. Using CPU instead." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Using GPU for process." + Style.RESET_ALL)
        self.model = whisper.load_model(model, device=self.device)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(self.script_dir, "temp")
        self.chunks_dir = os.path.join(self.temp_dir, "chunks")
        self.delete_chunks = delete_chunks
        self.include_timestamp = False
        self.output_with_and_without_timestamp = True

    def get_audio_duration(self):
        audio = AudioSegment.from_file(self.audio_path)
        duration_in_sec = len(audio) / 1000
        hours = int(duration_in_sec // 3600)
        minutes = int((duration_in_sec % 3600) // 60)
        seconds = int(duration_in_sec % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def divide_audio_into_chunks_of_seconds(self, seconds=30):
        print(Fore.GREEN + "Dividing audio into chunks..." + Style.RESET_ALL)
        os.makedirs(self.chunks_dir, exist_ok=True)
        command = f"ffmpeg -loglevel warning -hide_banner -i {self.audio_path} -f segment -segment_time {seconds} -c copy {self.chunks_dir}/{os.path.basename(self.audio_path)[:-4]}_%03d.mp3"
        subprocess.call(command, shell=True)

    def transcribe_audio_chunk(self, audio_chunk):
        result = self.model.transcribe(audio_chunk)
        return result["text"]

    def process_audio_chunks_sequentially(self, audio_chunks, output_file):
        include_timestamp = self.include_timestamp
        output_both = self.output_with_and_without_timestamp

        print(Fore.GREEN + "Processing audio chunks..." + Style.RESET_ALL)
        transcriptions = []
        for audio_chunk in tqdm(audio_chunks, ncols=70):
            transcription = self.transcribe_audio_chunk(audio_chunk)
            transcriptions.append(transcription)

        def write_transcriptions_to_file(file_path, include_timestamp):
            with open(file_path, "w", encoding="utf-8") as f:
                for index, transcription in enumerate(transcriptions):
                    chunk_start_time = index * 30
                    timestamp = f"{chunk_start_time // 3600:02d}:{(chunk_start_time % 3600) // 60:02d}:{chunk_start_time % 60:02d}"
                    if include_timestamp:
                        f.write(f"[{timestamp}] {transcription}\n")
                    else:
                        f.write(f"{transcription}\n")

        write_transcriptions_to_file(output_file, include_timestamp)

        if output_both and not include_timestamp:
            output_file_with_timestamp = output_file.replace(
                ".txt", "_with_timestamp.txt"
            )
            write_transcriptions_to_file(output_file_with_timestamp, True)

    async def transcribe_audio(self):
        print(
            Fore.GREEN
            + "Audio duration: "
            + self.get_audio_duration()
            + Style.RESET_ALL
        )
        timer = Timer()
        timer.start()
        output_file = os.path.join(
            "output", f"{os.path.basename(self.audio_path)[:-4]}.txt"
        )
        self.divide_audio_into_chunks_of_seconds()
        audio_chunks = sorted(
            glob.glob(os.path.join(self.chunks_dir, "*.mp3")),
            key=lambda x: int(x.split("_")[-1].split(".")[0]),
        )
        self.process_audio_chunks_sequentially(audio_chunks, output_file)

        if self.delete_chunks:
            shutil.rmtree(os.path.join(self.script_dir, "temp"))

        print(Fore.GREEN + "Transcription completed!" + Style.RESET_ALL)
        print(
            Fore.GREEN
            + "Total transcription processing time: "
            + timer.stop()
            + Style.RESET_ALL
        )


if __name__ == "__main__":
    audio_path = "data/meet_quivr.mp3"
    transcriber = AudioTranscriber(audio_path)
    asyncio.run(transcriber.transcribe_audio())
