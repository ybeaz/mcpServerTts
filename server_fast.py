"""
This module provides a FastMCP server for Piper TTS.
"""

import uvicorn
from fastmcp import FastMCP
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
import logging
from services.logic_tts import logic_tts
from services.defaults_tts import DEFAULT_VOICE, DEFAULT_OUTPUT_FILE, DEFAULT_SPEED

app = FastAPI()
mcp: FastMCP = FastMCP("TTS MCP Server")

app.mount("/mcp", mcp.sse_app())

logger = logging.getLogger(__name__)
speed: Annotated[float, Field(ge=0.5, le=2.0)] = DEFAULT_SPEED


class TTSRequest(BaseModel):
    text: str
    voice: str = DEFAULT_VOICE
    output_file: str = DEFAULT_OUTPUT_FILE
    speed: float = Field(default=DEFAULT_SPEED, ge=0.5, le=2.0)


@mcp.tool()
def tool_tts(
    text: str,
    voice: str = DEFAULT_VOICE,
    output_file: str = DEFAULT_OUTPUT_FILE,
    speed: float = Field(default=DEFAULT_SPEED, ge=0.5, le=2.0),
) -> dict:

    logger.info(
        "MCP TTS", extra={"voice": voice, "text_length": len(text), "source": "mcp"}
    )

    try:
        path = logic_tts(text, voice, output_file, speed)
        return {"path": path}
    except Exception as e:
        logger.exception("MCP TTS failed")
        return {"error": str(e)}


@app.post("/tts")
def http_tts(req: TTSRequest):

    logger.info(
        "TTS request",
        extra={"voice": req.voice, "text_length": len(req.text), "source": "rest"},
    )

    try:
        path = logic_tts(req.text, req.voice, req.output_file, req.speed)
        return {"path": path}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal TTS error")


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


    @run
    !Important: after restarting the piper server, you need to main restart the mcp server
    √ Terminal > `python -m server_fast`
    """

    mcp.run(transport="sse", port=4001, host="127.0.0.1")
    # uvicorn.run("server_fast:app", reload=True)
