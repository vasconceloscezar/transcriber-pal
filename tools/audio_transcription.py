from tools.audio_to_text import AudioTranscriber
from tools.terminal_operations import print_red


class AudioTranscription:
    @staticmethod
    async def transcribe_audio(input_file, output_dir):
        try:
            transcriber = AudioTranscriber(input_file)
            await transcriber.transcribe_audio(output_dir)
        except Exception as ex:
            print_red(f"Error transcribing file: {ex}")
