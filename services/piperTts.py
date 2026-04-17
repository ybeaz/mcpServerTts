from pprint import pprint
from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT
from piper.voice import PiperVoice
import wave
import subprocess, json

from shared.getItPrinted import getItPrinted as PRINT, comment, EXIT


raw_output = subprocess.check_output(
    ["node", "../yourails_common/dist/shared/getCli.js"]
)
lib_const = json.loads(raw_output.decode("utf-8"))

VOICES_PIPER = lib_const["VoicesPiperConst"]


### See README_HOW_TO.md: How to change/ add Piper voices
def piperTts(text: str, voice: str = "alan", output_file: str = "output.wav") -> str:

    voiceModel = PiperVoice.load(VOICES_PIPER[voice])

    chunks = []
    sample_rate = 22050  # fallback

    for i, chunk in enumerate(voiceModel.synthesize(text)):
        chunks.append(chunk.audio_int16_bytes)

        if i == 0:
            sample_rate = chunk.sample_rate  # ✅ correct source

    audio = b"".join(chunks)

    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

    return output_file


if __name__ == "__main__":
    """
    Terminal > `python -m services.piperTts`
    """
    PRINT(VOICES_PIPER, comment())
