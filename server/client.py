import requests
from pydub import AudioSegment
from pydub.playback import play
import io

# Define the API endpoint
TTS_URL = "http://localhost:5000/tts"


def send_text_get_audio(text):
    # Send the text to the TTS service
    response = requests.post(TTS_URL, data=text, stream=True)

    # Ensure the request was successful
    if response.status_code == 200:
        # Load the audio stream into an audio segment
        # Assuming the response content is an MP3 file
        audio_segment = AudioSegment.from_file(
            io.BytesIO(response.content), format="mp3"
        )

        # Play the audio segment
        play(audio_segment)
    else:
        print("Failed to get audio from server:", response.status_code)


if __name__ == "__main__":
    text = "Hello, this is a test text to synthesize."
    send_text_get_audio(text)
