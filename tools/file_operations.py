import os
import shutil

from tools.constants import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS


def get_file_extension(input_file):
    return os.path.splitext(input_file)[1]


def is_file_type(input_file, file_types):
    file_extension = get_file_extension(input_file)
    file_types_stripped = [extension.replace("*", "") for extension in file_types]
    return file_extension in file_types_stripped


def is_file_video(input_file):
    return is_file_type(input_file, VIDEO_EXTENSIONS)


def is_file_audio(input_file):
    return is_file_type(input_file, AUDIO_EXTENSIONS)


def move_file(input_file, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
    destination_file = os.path.join(destination_dir, os.path.basename(input_file))
    os.rename(input_file, destination_file)
    return destination_file


def get_file_basename(input_file):
    return os.path.splitext(os.path.basename(input_file))[0]
