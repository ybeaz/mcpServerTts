from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import soundfile as sf

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


def xtts_tts(
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
