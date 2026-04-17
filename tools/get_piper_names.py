from pathlib import Path
from pprint import pprint

BASE_DIR = Path("assets/piper/en/en_US")

MODEL_VOICES_PATHS = {}

for voice_dir in BASE_DIR.iterdir():
    if not voice_dir.is_dir():
        continue

    for quality_dir in voice_dir.iterdir():
        if not quality_dir.is_dir():
            continue

        onnx_files = list(quality_dir.glob("*.onnx"))
        if not onnx_files:
            continue

        model_name = f"en_GB-{voice_dir.name}-{quality_dir.name}"
        MODEL_VOICES_PATHS[model_name] = str(onnx_files[0])

pprint(MODEL_VOICES_PATHS)

if __name__ == "__main__":
    """
    Terminal > `python tools/get_piper_names.py`
    """
