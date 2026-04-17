"""
This module provides a FastMCP server for Piper TTS.
"""

# import os
# import sys

# sys.stderr = open(os.devnull, "w")

from pprint import pprint
from pathlib import Path
import json
import time
from pydoc import text
import wave
from fastmcp import FastMCP
from piper.voice import PiperVoice

import numpy as np
import onnxruntime
import soundfile as sf
from ttstokenizer import IPATokenizer
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

PIPER_VOICES = {
    "en_US-amy-low": "assets/piper/en/en_US/amy/low/en_US-amy-low.onnx",
    "en_US-amy-medium": "assets/piper/en/en_US/amy/medium/en_US-amy-medium.onnx",
    "en_US-arctic-medium": "assets/piper/en/en_US/arctic/medium/en_US-arctic-medium.onnx",
    "en_US-bryce-medium": "assets/piper/en/en_US/bryce/medium/en_US-bryce-medium.onnx",
    "en_US-danny-low": "assets/piper/en/en_US/danny/low/en_US-danny-low.onnx",
    "en_US-hfc_female-medium": "assets/piper/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx",
    "en_US-hfc_male-medium": "assets/piper/en/en_US/hfc_male/medium/en_US-hfc_male-medium.onnx",
    "en_US-joe-medium": "assets/piper/en/en_US/joe/medium/en_US-joe-medium.onnx",
    "en_US-john-medium": "assets/piper/en/en_US/john/medium/en_US-john-medium.onnx",
    "en_US-kathleen-low": "assets/piper/en/en_US/kathleen/low/en_US-kathleen-low.onnx",
    "en_US-kristin-medium": "assets/piper/en/en_US/kristin/medium/en_US-kristin-medium.onnx",
    "en_US-kusal-medium": "assets/piper/en/en_US/kusal/medium/en_US-kusal-medium.onnx",
    "en_US-l2arctic-medium": "assets/piper/en/en_US/l2arctic/medium/en_US-l2arctic-medium.onnx",
    "en_US-lessac-high": "assets/piper/en/en_US/lessac/high/en_US-lessac-high.onnx",
    "en_US-lessac-low": "assets/piper/en/en_US/lessac/low/en_US-lessac-low.onnx",
    "en_US-lessac-medium": "assets/piper/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
    "en_US-libritts-high": "assets/piper/en/en_US/libritts/high/en_US-libritts-high.onnx",
    "en_US-libritts_r-medium": "assets/piper/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx",
    "en_US-ljspeech-high": "assets/piper/en/en_US/ljspeech/high/en_US-ljspeech-high.onnx",
    "en_US-ljspeech-medium": "assets/piper/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx",
    "en_US-norman-medium": "assets/piper/en/en_US/norman/medium/en_US-norman-medium.onnx",
    "en_US-reza_ibrahim-medium": "assets/piper/en/en_US/reza_ibrahim/medium/en_US-reza_ibrahim-medium.onnx",
    "en_US-ryan-high": "assets/piper/en/en_US/ryan/high/en_US-ryan-high.onnx",
    "en_US-ryan-low": "assets/piper/en/en_US/ryan/low/en_US-ryan-low.onnx",
    "en_US-ryan-medium": "assets/piper/en/en_US/ryan/medium/en_US-ryan-medium.onnx",
    "en_US-sam-medium": "assets/piper/en/en_US/sam/medium/en_US-sam-medium.onnx",
    "en_GB-amy-low": "assets/piper/en/en_US/amy/low/en_US-amy-low.onnx",
    "en_GB-amy-medium": "assets/piper/en/en_US/amy/medium/en_US-amy-medium.onnx",
    "en_GB-arctic-medium": "assets/piper/en/en_US/arctic/medium/en_US-arctic-medium.onnx",
    "en_GB-bryce-medium": "assets/piper/en/en_US/bryce/medium/en_US-bryce-medium.onnx",
    "en_GB-danny-low": "assets/piper/en/en_US/danny/low/en_US-danny-low.onnx",
    "en_GB-hfc_female-medium": "assets/piper/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx",
    "en_GB-hfc_male-medium": "assets/piper/en/en_US/hfc_male/medium/en_US-hfc_male-medium.onnx",
    "en_GB-joe-medium": "assets/piper/en/en_US/joe/medium/en_US-joe-medium.onnx",
    "en_GB-john-medium": "assets/piper/en/en_US/john/medium/en_US-john-medium.onnx",
    "en_GB-kathleen-low": "assets/piper/en/en_US/kathleen/low/en_US-kathleen-low.onnx",
    "en_GB-kristin-medium": "assets/piper/en/en_US/kristin/medium/en_US-kristin-medium.onnx",
    "en_GB-kusal-medium": "assets/piper/en/en_US/kusal/medium/en_US-kusal-medium.onnx",
    "en_GB-l2arctic-medium": "assets/piper/en/en_US/l2arctic/medium/en_US-l2arctic-medium.onnx",
    "en_GB-lessac-high": "assets/piper/en/en_US/lessac/high/en_US-lessac-high.onnx",
    "en_GB-lessac-low": "assets/piper/en/en_US/lessac/low/en_US-lessac-low.onnx",
    "en_GB-lessac-medium": "assets/piper/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
    "en_GB-libritts-high": "assets/piper/en/en_US/libritts/high/en_US-libritts-high.onnx",
    "en_GB-libritts_r-medium": "assets/piper/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx",
    "en_GB-ljspeech-high": "assets/piper/en/en_US/ljspeech/high/en_US-ljspeech-high.onnx",
    "en_GB-ljspeech-medium": "assets/piper/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx",
    "en_GB-norman-medium": "assets/piper/en/en_US/norman/medium/en_US-norman-medium.onnx",
    "en_GB-reza_ibrahim-medium": "assets/piper/en/en_US/reza_ibrahim/medium/en_US-reza_ibrahim-medium.onnx",
    "en_GB-ryan-high": "assets/piper/en/en_US/ryan/high/en_US-ryan-high.onnx",
    "en_GB-ryan-low": "assets/piper/en/en_US/ryan/low/en_US-ryan-low.onnx",
    "en_GB-ryan-medium": "assets/piper/en/en_US/ryan/medium/en_US-ryan-medium.onnx",
    "en_GB-sam-medium": "assets/piper/en/en_US/sam/medium/en_US-sam-medium.onnx",
}

mcp: FastMCP = FastMCP("Piper TTS MCP Server")


### See README_HOW_TO.md: How to change/ add Piper voices
def _piper_tts(text: str, voice: str = "alan", output_file: str = "output.wav") -> str:

    voiceModel = PiperVoice.load(PIPER_VOICES[voice])

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


# ── Kokoro voices ─────────────────────────────────────────────────────────────

KOKORO_MODEL_PATH = "./assets/kokoro/kokoro-v0_19.onnx"
KOKORO_VOICES_PATH = "./assets/kokoro/voices.json"

with open(KOKORO_VOICES_PATH, "r", encoding="utf-8") as f:
    _kokoro_voices = json.load(f)

_kokoro_model = onnxruntime.InferenceSession(
    KOKORO_MODEL_PATH, providers=["CPUExecutionProvider"]
)
_kokoro_tokenizer = IPATokenizer()

KOKORO_VOICES = set(_kokoro_voices.keys())  # "af", "af_bella", "am_adam", …


def _kokoro_tts(text: str, voice: str, output_file: str, speed: float = 1.0) -> str:
    inputs = _kokoro_tokenizer(text)
    speaker = np.array(_kokoro_voices[voice], dtype=np.float32)

    outputs = _kokoro_model.run(
        None,
        {
            "tokens": [[0, *inputs, 0]],
            "style": speaker[len(inputs)],
            "speed": np.ones(1, dtype=np.float32) * speed,
        },
    )

    sf.write(output_file, outputs[0], 24000)
    return output_file


# ── XTTS v2 ───────────────────────────────────────────────────────────────────
XTTS_MODEL_DIR = "./assets/xtts_v2"

# Optional: named reference clips for convenience
# Drop any clean 6+ sec .wav files here and give them a name
XTTS_VOICES = {
    # "emma": "/Users/admin/.local/share/tts/references/emma.wav",
    # "john": "/Users/admin/.local/share/tts/references/john.wav",
}

_xtts_model = None  # lazy-loaded on first use


def _get_xtts_model():
    """Load XTTS v2 from local directory — no internet needed."""
    global _xtts_model
    if _xtts_model is None:
        print("⏳ Loading XTTS v2 from local files...")
        config = XttsConfig()
        config.load_json(f"{XTTS_MODEL_DIR}/config.json")
        _xtts_model = Xtts.init_from_config(config)
        _xtts_model.load_checkpoint(
            config,
            checkpoint_dir=XTTS_MODEL_DIR,
            eval=True,
        )
        # Use CPU — change to .cuda() if you have a GPU
        _xtts_model.cpu()
        print("✅ XTTS v2 ready")
    return _xtts_model


def _xtts_tts(
    text: str,
    output_file: str,
    speaker_wav: str,
    language: str = "en",
    speed: float = 1.0,
) -> str:
    model = _get_xtts_model()

    outputs = model.synthesize(
        text,
        model.config,
        speaker_wav=speaker_wav,
        gpt_cond_len=6,
        language=language,
        speed=speed,
    )

    sf.write(output_file, outputs["wav"], 24000)
    return output_file


@mcp.tool()
def tool_tts(
    text: str,
    voice: str = "en_US-amy-medium",
    output_file: str = "output.wav",
    speed: float = 1.0,
) -> str:

    SPEAKER_WAV = "./references/reference_chrp_3.wav"
    OUTPUT_DIR = Path("__output__")

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file_next = str(OUTPUT_DIR / output_file)
    path = ""

    print("mcpServerTts [200] 🔥 MCP CALL RECEIVED:", text)

    if voice in PIPER_VOICES:
        # print(f"PIPER_VOICES: {voice}")
        path = _piper_tts(text, voice, output_file=output_file_next)

    elif voice in KOKORO_VOICES:
        # print(f"KOKORO_VOICES: {voice}")
        path = _kokoro_tts(text, voice, output_file=output_file_next, speed=speed)

    else:
        path = _xtts_tts(
            text,
            output_file=output_file_next,
            speaker_wav=SPEAKER_WAV,
            language="en",
            speed=speed,
        )

    return f"Audio saved to {path}"


"""
# To upload kokoro_assets
Browser > `https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files` > download manually
"""

if __name__ == "__main__":
    """
    Terminal > `conda activate py3108`
    √ Terminal > python -c "from fastmcp import FastMCP; print(FastMCP)"
    @test piper_tts_impl function
    √ Terminal > `print(piper_tts_impl("Hello world", "hello_world2.wav"))`
    √ print(KOKORO_VOICES) # {'bf_emma', 'af_bella', 'af_nicole', 'bm_george', 'bm_lewis', 'bf_isabella', 'am_adam', 'am_michael', 'af_sky', 'af_sarah', 'af'}
    Terminal > `python mcpServerTts.py test_piper`   # lext: 239. Execution time: 1.494135 seconds. Speed: 0.00625
    Terminal > `python mcpServerTts.py test_kokoro`  # lext: 239. Execution time: 8.604333 seconds. Speed: 0.03600
    Terminal > `python mcpServerTts.py test_xtts_v2` # lext: 239. Execution time: 62.11161 seconds. Speed: 0.2598



    @run
    !Important: after restarting the piper server, you need to main restart the mcp server
    √ Terminal > `python mcpServerTts.py`
    """

    import sys

    TEXT = "This idea shows how one embedded element can serve several functions at the same time. It can both protect the system and support operations like access or disassembly. The key principle is combining multiple roles into a single component."
    VOICE = "en_US-kusal-medium"  # FOR kokoro "bm_george"
    SPEAKER_WAV = "./references/reference_chrp.wav"  # "./references/reference_chrp_3.wav" "./references/reference_chanr.wav"
    OUTPUT_FILE = "./__output__/output9.wav"

    text_len = len(TEXT)

    if len(sys.argv) > 1 and sys.argv[1] == "test_piper":
        start = time.perf_counter()

        out = _piper_tts(text=TEXT, voice=VOICE, output_file=OUTPUT_FILE)

        end = time.perf_counter()
        duration = end - start
        print(
            f"✅ Saved to {out}. lext: {text_len}. Execution time: {duration:.6f} seconds. Speed: {duration/text_len}"
        )

    elif len(sys.argv) > 1 and sys.argv[1] == "test_kokoro":
        start = time.perf_counter()

        out = _kokoro_tts(text=TEXT, voice=VOICE, output_file=OUTPUT_FILE, speed=1.0)

        end = time.perf_counter()
        duration = end - start
        print(
            f"✅ Saved to {out}. lext: {text_len}. Execution time: {duration:.6f} seconds. Speed: {duration/text_len}"
        )

    elif len(sys.argv) > 1 and sys.argv[1] == "test_xtts_v2":
        # Test XTTS — point to any clean 6+ second .wav on your machine

        start = time.perf_counter()

        out = _xtts_tts(
            text=TEXT,
            output_file=OUTPUT_FILE,
            speaker_wav=SPEAKER_WAV,
            language="en",
        )

        end = time.perf_counter()
        duration = end - start

        print(
            f"✅ Saved to {out}. lext: {text_len}. Execution time: {duration:.6f} seconds. Speed: {duration/text_len}"
        )
    else:
        mcp.run(transport="sse", port=4001, host="127.0.0.1")
