# Transcriber Pal

Transcriber Pal is a Python command-line application that transcribes audio and video files to text using artificial intelligence. It uses the [Whisper](https://github.com/openai/whisper) library for speech recognition and the FFmpeg library for audio and video processing.


## Requirements
- Python 3.9 or higher
- FFmpeg

You mostly just need to follow the instructions here on the [Whisper Doc](https://github.com/openai/whisper/edit/main/README.md#setup)

You can install the Python dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage
To transcribe an audio or video file, run the main.py script and pass the path to the input file as a command-line argument:

```bash
python main.py input_file.mp3
```

The time it takes to finish the transcript is roughly half the time of the audio, it can be a bit longer if there's a need to convert the video to audio. 

The output text will be saved to a file in the output directory with the same name as the input file.

If the input file is a video file, the script will first convert it to an audio file using FFmpeg before transcribing it.

If no input file is provided, the script will display an error message.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.