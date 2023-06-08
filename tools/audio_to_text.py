import os
import shutil
import subprocess
import time
import whisper
import asyncio
import glob

model = whisper.load_model("small") # Model to use for transcription

script_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(script_dir, "temp")
chunks_dir = os.path.join(temp_dir, "chunks")


def divide_audio_into_chunks_of_seconds(audio_path, seconds=30):
    os.makedirs(chunks_dir, exist_ok=True)
    command = f"ffmpeg -i {audio_path} -f segment -segment_time {seconds} -c copy {chunks_dir}/{os.path.basename(audio_path)[:-4]}_%03d.mp3"
    subprocess.call(command, shell=True)


async def transcribe_audio(audio_path):
    output_file = os.path.join("output", f"{os.path.basename(audio_path)[:-4]}.txt")
    divide_audio_into_chunks_of_seconds(audio_path)

    audio_chunks = sorted(
        [
            os.path.join(
                temp_dir, "chunks", f"{os.path.basename(audio_path)[:-4]}_{i:03d}.mp3"
            )
            for i in range(len(glob.glob(os.path.join(chunks_dir, "*.mp3"))))
        ],
        key=lambda x: int(x.split("_")[-1].split(".")[0]),
    )

    print("Processing chunks:")
    
    total_time = 0  # variable to store total time
    chunk_count = 0  # variable to store the number of chunks processed
    total_chunks = len(audio_chunks)  # total number of chunks

    with open(output_file, "w", encoding="utf-8") as f:
        for index, audio_chunk in enumerate(audio_chunks):
            if os.path.isfile(audio_chunk):
                start_time = time.time()
                result = model.transcribe(audio_chunk)
                elapsed_time = time.time() - start_time
                total_time += elapsed_time  # accumulate time
                chunk_count += 1  # increment chunk count
                
                chunk_start_time = index * 30
                timestamp = f"{chunk_start_time // 3600:02d}:{(chunk_start_time % 3600) // 60:02d}:{chunk_start_time % 60:02d}"
                
                avg_time_per_chunk = total_time / chunk_count  # calculate average time
                estimated_remaining_time = avg_time_per_chunk * (total_chunks - chunk_count)  # estimate remaining time
                
                print(f"Processed {chunk_count} out of {total_chunks} chunks. Estimated time remaining: {estimated_remaining_time:.2f} seconds.")
                f.write(f"[{timestamp}] {result['text']}\n")

    # Remove temp directory
    shutil.rmtree(os.path.join(script_dir, "temp"))


if __name__ == "__main__":
    audio_path = "data/meet_quivr.mp3"
    asyncio.run(transcribe_audio(audio_path))
