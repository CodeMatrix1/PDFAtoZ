import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import PyPDF2
import io

from mcqgen import excecute  # Make sure this is the correct import

app = FastAPI()

text = ""
mcqs= ""

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
    global text
    contents = await file.read()
    reader = PyPDF2.PdfReader(io.BytesIO(contents))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return {"msg": "successful"}

@app.get("/results")
async def get_results():
    global text
    mcqs = excecute(text)
    return {"mcqs": mcqs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)