#!/usr/bin/env python3

import argparse
import io
import requests

from pydub import AudioSegment
from pydub.playback import play

import sys
from pathlib import Path

# Add the parent directory of the current file to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from configdict import ConfigDict

# Define the API endpoint default
DEFAULT_TTS_URL = "http://localhost:5000/tts"

# init config
config = ConfigDict("config-client.json")
config.default("mode", "play_audio")


def handle_audio(audio_segment):
    if config.mode == "play_audio":
        play(audio_segment)


def send_text_get_audio(text, tts_url):
    # Send the text to the TTS service
    response = requests.post(tts_url, data=text, stream=True)

    # Ensure the request was successful
    if response.status_code == 200:
        # Load the audio stream into an audio segment
        # Assuming the response content is an MP3 file
        audio_segment = AudioSegment.from_file(
            io.BytesIO(response.content), format="mp3"
        )

        # Play the audio segment
        handle_audio(audio_segment)
    else:
        print("Failed to get audio from server:", response.status_code)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Send text to TTS service and play audio"
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_TTS_URL,
        help="Host connection string (default: %(default)s)",
    )
    parser.add_argument(
        "--file", type=argparse.FileType("r"), help="File path to read text from"
    )
    parser.add_argument("--text", help="Text to input directly")

    args = parser.parse_args()

    # Determine the source of text
    if args.file:
        text = args.file.read()
    elif args.text:
        text = args.text
    else:
        raise ValueError("Either --file or --text must be provided.")

    # Send text to the TTS service and play the audio
    send_text_get_audio(text, args.host)


if __name__ == "__main__":
    main()
