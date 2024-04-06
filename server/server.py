import io

import requests
import torchaudio
import numpy as np
from flask import Flask, request, Response
from pydub import AudioSegment
from tortoise import api

from configdict import ConfigDict


app = Flask(__name__)


config = ConfigDict("server_config.json")

tort_tts = api.TextToSpeech(kv_cache=True)


def _tts(text):
    wav_list = tort_tts.tts_with_preset(text, preset="fast")

    pcm_audio = np.array(wav_list, dtype=np.float32)
    pcm_audio_int16 = (pcm_audio * (2**15 - 1)).astype(np.int16)
    audio_segment = AudioSegment(
        pcm_audio_int16.tobytes(), frame_rate=22050, sample_width=2, channels=1
    )

    return audio_segment


@app.route("/tts", methods=["POST"])
def tts():
    text = request.data.decode("utf-8")

    # Generate audio tensor from text (your TTS logic here)
    audio_segment = _tts(
        text
    )  # This function should return a tensor and its sample rate

    mp3_buffer = io.BytesIO()
    audio_segment.export(
        mp3_buffer, format="mp3", bitrate="192k", parameters=["-ar", "24000"]
    )
    mp3_buffer.seek(0)  # Rewind the buffer to the beginning

    # Stream the MP3 data
    return Response(mp3_buffer.getvalue(), mimetype="audio/mp3")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
