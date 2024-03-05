from fastapi import FastAPI, Body
from pydantic import BaseModel
from fastapi.responses import FileResponse
from melo.api import TTS

DEFAULT_SPEED = 1.0
DEFAULT_LANGUAGE = 'EN'
DEFAULT_SPEAKER = 'EN-Default'
device = 'auto'  # Will automatically use GPU if available

class TextModel(BaseModel):
    text: str
    speaker: str = DEFAULT_SPEAKER
    language: str = DEFAULT_LANGUAGE
    speed: float = DEFAULT_SPEED

app = FastAPI()

@app.post("/tts")
async def create_upload_file(body: TextModel = Body(...)):
    # Retrieve parameters from the request
    text = body.text
    speaker = body.speaker
    language = body.language
    speed = body.speed
    
    model = TTS(language=language, device=device)
    speaker_id = model.hps.data.spk2id.get(speaker)

    if speaker_id is None:
        return {"error": "Invalid speaker ID"}

    output_path = f"{language}-{speaker}-{speed}.wav"
    model.tts_to_file(text, speaker_id, output_path, speed=speed)

    # Return the audio file
    return FileResponse(output_path, media_type="audio/mpeg", filename=output_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
