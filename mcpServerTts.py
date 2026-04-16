"""
This module provides a FastMCP server for Piper TTS.
"""

from pydoc import text
import wave
from fastmcp import FastMCP
from piper.voice import PiperVoice

MODEL_VOICES_PATHS = {
    "alan": "/Users/admin/.local/share/piper-tts/piper-voices/en_GB-alan-medium.onnx",
    "arctic": "/Users/admin/.local/share/piper-tts/piper-voices/en_US-arctic-medium.onnx",
}

mcp: FastMCP = FastMCP("Piper TTS MCP Server")


### See README_HOW_TO.md: How to change/ add Piper voices
def piper_tts_impl(
    text: str, voice: str = "alan", output_file: str = "output.wav"
) -> str:

    voiceModel = PiperVoice.load(MODEL_VOICES_PATHS[voice])

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


@mcp.tool()
def piper_tts(text: str, voice: str = "alan", output_file: str = "output.wav") -> str:
    print("mcpServerTts [45] 🔥 MCP CALL RECEIVED:", text)

    path = piper_tts_impl(text, voice, output_file)

    return f"Audio saved to {path}"


if __name__ == "__main__":
    # Terminal > `conda activate py3108`
    # √ Terminal > python -c "from fastmcp import FastMCP; print(FastMCP)"
    # @test piper_tts_impl function
    # √ Terminal > `print(piper_tts_impl("Hello world", "hello_world.wav"))`
    # @run
    # !Important: after restarting the piper server, you need to main restart the mcp server
    # √ Terminal > `python mcpServerTts.py`

    mcp.run(transport="sse", port=4001, host="127.0.0.1")
