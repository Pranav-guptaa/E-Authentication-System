import sounddevice as sd
from scipy.io.wavfile import write

def recording_voice():
    # Sampling frequency
    freq = 44100

    # Recording duration (in seconds)
    duration = 5

    # Record audio
    print("Recording started...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    print("Recording finished.")

    # Save audio as WAV file

    file_name = "E:\\RevisedEAuthenticationSystem\\recordedVoices\\recording.wav"
    write(file_name, freq, recording)

    print(f"Audio file saved as {file_name}")
