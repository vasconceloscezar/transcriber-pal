import os
from faster_whisper import WhisperModel

model_size = "large-v2"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

root_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(root_folder, "../data")
file_path = os.path.join(data_folder, "analise_requirements_transcriber.mp3")

segments, info = model.transcribe(file_path, beam_size=5)

print(
    "Detected language '%s' with probability %f"
    % (info.language, info.language_probability)
)


transcripts = []
transcripts_without_timestamp = []

for segment in segments:
    transcript_with_timestamp = "[%.2fs -> %.2fs] %s" % (
        segment.start,
        segment.end,
        segment.text,
    )
    transcript_without_timestamp = segment.text

    transcripts.append(transcript_with_timestamp)
    transcripts_without_timestamp.append(transcript_without_timestamp)

    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    # save all into a


with open("transcript.txt", "w", encoding="utf-8") as f:
    for transcript in transcripts:
        f.write(transcript + "\n")


with open("transcript_without_timestamp.txt", "w", encoding="utf-8") as f:
    for transcript in transcripts_without_timestamp:
        f.write(transcript + "\n")
