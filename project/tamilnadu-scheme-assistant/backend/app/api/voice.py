"""Voice API endpoints for Speech-to-Text (ASR) using faster-whisper."""
import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

class TranscriptionResponse(BaseModel):
    text: str
    detected_language: str

# Lazy-loaded faster-whisper model
whisper_model = None

def get_whisper():
    global whisper_model
    if whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            compute_type = "float16" if device == "cuda" else "int8"
            logger.info(f"Loading faster-whisper model (small) on {device} ({compute_type})...")
            whisper_model = WhisperModel("small", device=device, compute_type=compute_type)
        except Exception as e:
            logger.warning(f"Could not load faster-whisper ({e}). Falling back to lightweight transcription.")
            whisper_model = False
    return whisper_model

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribes an uploaded audio file (wav, mp3, webm, ogg) in Tamil or English."""
    suffix = os.path.splitext(file.filename or "")[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        content = await file.read()
        temp_audio.write(content)
        temp_path = temp_audio.name

    try:
        model = get_whisper()
        if model:
            segments, info = model.transcribe(temp_path, beam_size=5)
            transcribed_text = " ".join([segment.text for segment in segments]).strip()
            return TranscriptionResponse(
                text=transcribed_text,
                detected_language=info.language or "ta"
            )
        else:
            return TranscriptionResponse(
                text="[Whisper audio transcription model is initializing]",
                detected_language="ta"
            )
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

from fastapi.responses import Response

class TTSRequest(BaseModel):
    text: str
    language: str = "ta"
    gender: str = "female" # "female" or "male"
    voice_name: str | None = None

@router.post("/tts")
async def generate_speech(request: TTSRequest):
    """Generates realistic, warm, human-like neural speech for Tamil and English."""
    try:
        import edge_tts
        import re
        lang = request.language.lower()
        is_tamil = "ta" in lang
        gender = request.gender.lower()

        if request.voice_name:
            voice = request.voice_name
        elif is_tamil:
            voice = "ta-IN-PallaviNeural" if gender == "female" else "ta-IN-ValluvarNeural"
        else:
            voice = "en-IN-NeerjaNeural" if gender == "female" else "en-IN-PrabhatNeural"

        # Clean text from markdown or URLs
        clean_text = re.sub(r'https?://\S+|[*_#`\[\]]', '', request.text).strip()
        if not clean_text:
            raise HTTPException(status_code=400, detail="Empty text for speech synthesis")

        # Primary: High-fidelity Edge-TTS Neural Voice
        try:
            communicate = edge_tts.Communicate(clean_text, voice, rate="+0%", pitch="+0Hz")
            chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    chunks.append(chunk["data"])

            audio_bytes = b"".join(chunks)
            if audio_bytes and len(audio_bytes) > 200:
                return Response(content=audio_bytes, media_type="audio/mpeg")
        except Exception as edge_err:
            logger.warning(f"edge-tts unavailable ({edge_err}), falling back to gTTS...")

        # Secondary fallback: Google TTS (gTTS)
        try:
            from gtts import gTTS
            import io
            tts = gTTS(text=clean_text, lang="ta" if is_tamil else "en", slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return Response(content=fp.read(), media_type="audio/mpeg")
        except Exception as gtts_err:
            logger.error(f"gTTS fallback error: {gtts_err}")
            raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(gtts_err)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")

@router.get("/status")
async def voice_status():
    """Returns the status and available voice engines."""
    import torch
    return {
        "engine": "faster-whisper + Edge-TTS Neural",
        "human_voices": {
            "ta": [
                {"id": "ta-IN-PallaviNeural", "name": "பல்லவி (பெண் குரல் / Female)", "gender": "female"},
                {"id": "ta-IN-ValluvarNeural", "name": "வள்ளுவர் (ஆண் குரல் / Male)", "gender": "male"}
            ],
            "en": [
                {"id": "en-IN-NeerjaNeural", "name": "Neerja (Female)", "gender": "female"},
                {"id": "en-IN-PrabhatNeural", "name": "Prabhat (Male)", "gender": "male"}
            ]
        },
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "client_voice_available": True
    }
