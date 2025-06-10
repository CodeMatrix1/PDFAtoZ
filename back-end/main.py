import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import PyPDF2
import io

app = FastAPI()

text=""

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def load_pdf(file: UploadFile = File(...)):
    text = ""
    contents = await file.read()
    reader = PyPDF2.PdfReader(io.BytesIO(contents))
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return {"text": text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)