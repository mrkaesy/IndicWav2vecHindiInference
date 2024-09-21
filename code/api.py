from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys

import base64
from w2l_decoder import  infer

    
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import zipfile
import os
import shutil
import base64


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# Ensure the directory exists for saving files
os.makedirs("temp", exist_ok=True)
os.makedirs("unzipped_files", exist_ok=True)

@app.post("/upload-audio-zip/")
async def upload_and_process_zip(file: UploadFile = File(...)):
    try:
        # Check if the file is a ZIP file
        if file.content_type != 'application/zip':
            raise HTTPException(status_code=400, detail={"code": "ERROR", "message": "Invalid file type. Only ZIP files are allowed."})

        # Save the uploaded ZIP file to a temporary location
        zip_file_location = f"temp/{file.filename}"
        with open(zip_file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check if the ZIP file is corrupted
        try:
            with zipfile.ZipFile(zip_file_location, 'r') as zip_ref:
                # Check if the ZIP file is empty
                if len(zip_ref.namelist()) == 0:
                    raise HTTPException(status_code=400, detail={"code": "ERROR", "message": "The ZIP file is empty."})

                # Unzip the file
                unzip_location = f"unzipped_files/{file.filename.split('.')[0]}"
                os.makedirs(unzip_location, exist_ok=True)
                zip_ref.extractall(unzip_location)
        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail={"code": "ERROR", "message": "The ZIP file is corrupted."})

        # Check the extracted files for audio
        extracted_files = os.listdir(unzip_location)
        audio_files = [f for f in extracted_files if f.endswith(('.wav', '.mp3', '.aac'))]

        if len(audio_files) == 0:
            raise HTTPException(status_code=400, detail={"code": "ERROR", "message": "No audio files found in the ZIP."})

        # Process each audio file
        for audio_file in audio_files:
            audio_file_path = os.path.join(unzip_location, audio_file)

            # Check if the audio file is empty
            if os.path.getsize(audio_file_path) == 0:
                raise HTTPException(status_code=400, detail={"code": "ERROR", "message": f"The audio file {audio_file} is empty."})

            # Convert the audio file to base64
            with open(audio_file_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
                out = infer(audio_base64,'config.yaml')
                print(out)
    

        # Return a dummy text along with the audio file base64
        return JSONResponse(content={"code": "OK", "message": "Processing complete", "Result": out}, status_code=200)

    except HTTPException as e:
        raise e  # Propagate the HTTPException with error details
    finally:
        # Cleanup: remove temporary files and directories
        if os.path.exists(zip_file_location):
            os.remove(zip_file_location)
        if os.path.exists(unzip_location):
            shutil.rmtree(unzip_location)
            
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)    