from pprint import pprint
from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT
from piper.voice import PiperVoice
import wave
import subprocess, json
from pathlib import Path

from shared.getItPrinted import getItPrinted as PRINT, comment, EXIT
from shared.timeout import timeout
from shared.get_duration_seconds import get_duration_seconds
from shared.get_built_atempo import get_built_atempo

raw_output = subprocess.check_output(
    ["node", "../yourails_common/dist/shared/getCli.js"]
)
lib_const = json.loads(raw_output.decode("utf-8"))

VOICES_PIPER = lib_const["VoicesPiperConst"]


### See README_HOW_TO.md: How to change/ add Piper voices
def piper_tts(
    text: str, voice: str = "alan", output_file: str = "output.wav", speed: float = 1
) -> str:

    voiceModel = PiperVoice.load(VOICES_PIPER[voice])

    chunks = []
    sample_rate = 22050  # fallback

    for i, chunk in enumerate(voiceModel.synthesize(text)):
        chunks.append(chunk.audio_int16_bytes)

        if i == 0:
            sample_rate = chunk.sample_rate  # ✅ correct source

    audio = b"".join(chunks)

    p = Path(output_file)
    tmp_wav = p.with_name(p.stem + "_temp" + p.suffix)
    tmp_out = None

    try:
        # 1. write WAV
        with wave.open(str(tmp_wav), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio)

        # 2. no processing case
        if speed == 1:
            tmp_wav.replace(output_file)
            return output_file

        # 3. ffmpeg case
        durationSeconds = get_duration_seconds(str(tmp_wav))
        timeout = durationSeconds * 2 + 3

        tmp_out = p.with_name(p.stem + "_out" + p.suffix)

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(tmp_wav),
            "-filter:a",
            get_built_atempo(speed),
            str(tmp_out),
        ]

        subprocess.run(cmd, timeout=timeout, check=True)

        tmp_out.replace(output_file)
        return output_file

    finally:
        # cleanup
        for f in [tmp_wav, tmp_out]:
            if f:
                Path(f).unlink(missing_ok=True)


if __name__ == "__main__":
    """
    Terminal > `python -m services.piperTts`
    """
    PRINT(VOICES_PIPER, comment())
