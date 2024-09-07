from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from inference import model_fn, input_fn, predict_fn, output_fn
from pydantic import BaseModel
import sys
    sys.path.append('code')
import base64
from w2l_decoder import  infer
class UserCreate(BaseModel):
    # filename: str
    data: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def read_root(data: UserCreate):
    
    # encode_string = base64.b64encode(open("1.mp3", "rb").read()).decode()
    
    out = infer(data,'/mnt/External/8TBHDD/Keyur/IndicWav2vecHindiInference/code/config.yaml')
    return out