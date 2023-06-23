import os
import dotenv
import whisperx
import gc

dotenv.load_dotenv()

device = "cuda"

audio_file_name = "analise_requirements_transcriber.mp3"
root_folder = os.path.dirname(os.path.realpath(__file__))
audio_path = os.path.join(root_folder, f"../data/{audio_file_name}")

batch_size = 8  # reduce if low on GPU mem
compute_type = "int8"  # change to "float16" if low on GPU mem (may reduce accuracy)

HF_TOKEN = os.environ.get("HUGGING_FACE_API_TOKEN")

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("small", device, compute_type=compute_type, language="en")

audio = whisperx.load_audio(audio_path)
result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"])  # before alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)
result = whisperx.align(
    result["segments"], model_a, metadata, audio, device, return_char_alignments=False
)

print(result["segments"])  # after alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

print(f"Hugging Face API Token: {HF_TOKEN}")

# 3. Assign speaker labels
diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN)
if diarize_model is not None:
    diarize_model = diarize_model.to(device)
else:
    raise RuntimeError("Failed to load the diarization pipeline.")

# add min/max number of speakers if known
diarize_segments = diarize_model(audio_path)
# diarize_model(audio_file, min_speakers=min_speakers, max_speakers=max_speakers)

result = whisperx.assign_word_speakers(diarize_segments, result)
print(diarize_segments)
print(result["segments"])  # segments are now assigned speaker IDs

# save each to txt files
with open("whisperx.txt", "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        f.write(f"{segment['speaker_id']}: {segment['text']}\n")
