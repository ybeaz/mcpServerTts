"""
This module provides a FastMCP server for Piper TTS.
"""

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

from services.piper_tts import piper_tts, VOICES_PIPER
from services.kokoro_tts import kokoro_tts, KOKORO_VOICES
from services.xtts_tts import xtts_tts

mcp: FastMCP = FastMCP("TTS MCP Server")


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

    if voice in VOICES_PIPER:
        # print(f"VOICES_PIPER: {voice}")
        path = piper_tts(text, voice, output_file=output_file_next, speed=speed)

    elif voice in KOKORO_VOICES:
        # print(f"KOKORO_VOICES: {voice}")
        path = kokoro_tts(text, voice, output_file=output_file_next, speed=speed)

    else:
        path = xtts_tts(
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
    Terminal > `python -m mcpServerTts test_piper`   # lext: 239. Execution time: 1.494135 seconds. Speed: 0.00625
    Terminal > `python -m mcpServerTts test_kokoro`  # lext: 239. Execution time: 8.604333 seconds. Speed: 0.03600
    Terminal > `python -m mcpServerTts test_xtts_v2` # lext: 239. Execution time: 62.11161 seconds. Speed: 0.2598



    @run
    !Important: after restarting the piper server, you need to main restart the mcp server
    √ Terminal > `python mcpServerTts.py`
    √ Terminal > `python -m mcpServerTts`
    """

    import sys

    TEXT = "This idea shows how one embedded element can serve several functions at the same time. It can both protect the system and support operations like access or disassembly. The key principle is combining multiple roles into a single component."
    VOICE = "am_adam"  # FOR kokoro "bm_george" # "af", "af_bella", "am_adam"
    SPEAKER_WAV = "./references/reference_chrp.wav"  # "./references/reference_chrp_3.wav" "./references/reference_chanr.wav"
    OUTPUT_FILE = "./__output__/output5.wav"

    text_len = len(TEXT)

    if len(sys.argv) > 1 and sys.argv[1] == "test_piper":
        start = time.perf_counter()

        output = piper_tts(text=TEXT, voice=VOICE, output_file=OUTPUT_FILE)

        end = time.perf_counter()
        duration = end - start
        print(
            f"✅ Saved to {output}. lext: {text_len}. Execution time: {duration:.6f} seconds. Speed: {duration/text_len}"
        )

    elif len(sys.argv) > 1 and sys.argv[1] == "test_kokoro":
        start = time.perf_counter()

        output = kokoro_tts(text=TEXT, voice=VOICE, output_file=OUTPUT_FILE, speed=1.0)

        end = time.perf_counter()
        duration = end - start
        print(
            f"✅ Saved to {output}. lext: {text_len}. Execution time: {duration:.6f} seconds. Speed: {duration/text_len}"
        )

    elif len(sys.argv) > 1 and sys.argv[1] == "test_xtts_v2":
        # Test XTTS — point to any clean 6+ second .wav on your machine

        start = time.perf_counter()

        output = xtts_tts(
            text=TEXT,
            output_file=OUTPUT_FILE,
            speaker_wav=SPEAKER_WAV,
            language="en",
        )

        end = time.perf_counter()
        duration = end - start

        print(
            f"✅ Saved to {output}. lext: {text_len}. Execution time: {duration:.6f} seconds. Speed: {duration/text_len}"
        )
    else:
        mcp.run(transport="sse", port=4001, host="127.0.0.1")
