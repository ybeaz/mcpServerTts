from shared.getItPrinted import getItPrinted as PRINT, comment, EXIT

import json
import numpy as np
import onnxruntime
from ttstokenizer import IPATokenizer
import soundfile as sf


KOKORO_MODEL_PATH = "./assets/kokoro/kokoro-v0_19.onnx"
KOKORO_VOICES_PATH = "./assets/kokoro/voices.json"

with open(KOKORO_VOICES_PATH, "r", encoding="utf-8") as f:
    _kokoro_voices = json.load(f)

_kokoro_model = onnxruntime.InferenceSession(
    KOKORO_MODEL_PATH, providers=["CPUExecutionProvider"]
)
_kokoro_tokenizer = IPATokenizer()

KOKORO_VOICES = set(_kokoro_voices.keys())  # "af", "af_bella", "am_adam", …


def kokoroTts(text: str, voice: str, output_file: str, speed: float = 1.0) -> str:
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


if __name__ == "__main__":
    """
    Terminal > `python -m services.kokoroTts`
    """
    PRINT(KOKORO_VOICES, comment(), edgeItems=10000)
