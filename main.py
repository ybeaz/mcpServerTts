"""
This module provides a FastMCP server for Piper TTS.
"""

import asyncio
from contextlib import asynccontextmanager
import threading
import uvicorn
from fastmcp import FastMCP
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
import logging
from services.logic_tts import logic_tts
from services.defaults_tts import DEFAULT_VOICE, DEFAULT_OUTPUT_FILE, DEFAULT_SPEED

logger = logging.getLogger(__name__)

mcp: FastMCP = FastMCP("TTS MCP Server")


def run_mcp():
    logger.info("Starting MCP server...")
    mcp.run(transport="sse", port=4001, host="127.0.0.1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=run_mcp, daemon=True)
    thread.start()
    yield


app = FastAPI(lifespan=lifespan)
semaphore = asyncio.Semaphore(2)


class TTSRequest(BaseModel):
    text: str = Field(min_length=6, max_length=1000_000)
    voice: str = Field(default=DEFAULT_VOICE, min_length=2, max_length=124)
    output_file: str = Field(default=DEFAULT_OUTPUT_FILE, min_length=6, max_length=512)
    speed: float = Field(default=DEFAULT_SPEED, ge=0.5, le=2.0)


@mcp.tool()
async def tool_tts(
    text: str,
    voice: str = DEFAULT_VOICE,
    output_file: str = DEFAULT_OUTPUT_FILE,
    speed: float = DEFAULT_SPEED,
) -> dict:

    logger.info(
        "MCP TTS request",
        extra={"voice": voice, "text_length": len(text), "source": "mcp:/sse"},
    )

    try:
        async with semaphore:
            path = await asyncio.to_thread(logic_tts, text, voice, output_file, speed)
            return {"path": path}
    except Exception as e:
        logger.exception("MCP TTS failed")
        return {"error": str(e)}


@app.post("/tts")
async def http_tts(req: TTSRequest):

    logger.info(
        "POST TTS request",
        extra={
            "voice": req.voice,
            "text_length": len(req.text),
            "source": "rest:post:/tts",
        },
    )

    try:
        async with semaphore:
            path = await asyncio.to_thread(
                logic_tts, req.text, req.voice, req.output_file, req.speed
            )
            return {"path": path}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal TTS error")


if __name__ == "__main__":

    # mcp.run(transport="sse", port=4001, host="127.0.0.1") # To run with Terminal > `python -m server_fast`
    # Redundant: uvicorn.run("server_fast:app", host="127.0.0.1", port=4001, reload=False)

    """
    Terminal > `conda activate py3108`
    √ Terminal > python -c "from fastmcp import FastMCP; print(FastMCP)"
    @test piper_tts_impl function
    √ Terminal > `print(piper_tts_impl("Hello world", "hello_world2.wav"))`
    √ print(KOKORO_VOICES) # {'bf_emma', 'af_bella', 'af_nicole', 'bm_george', 'bm_lewis', 'bf_isabella', 'am_adam', 'am_michael', 'af_sky', 'af_sarah', 'af'}


    @run
    !Important: after restarting the piper server, you need to main restart the mcp server
    √ Terminal > `python -m main`
    √ Terminal > `uvicorn main:app --host 127.0.0.1 --port 4002 --reload`
    """

    """
    # To upload kokoro_assets
    Browser > `https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files` > download manually
    """
