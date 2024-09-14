from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys

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
    
    out = infer(data,'config.yaml')
    return out