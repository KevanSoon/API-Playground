# To Remove

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Access the API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/chartdata")
def read_chart():
    data = [
         {"name": "T2-R2AW1", "Median": 40, "Minimum": 40},
         {"name": "T2-R1AW2", "Median": 39.31, "Minimum": 39.31},
         {"name": "T1-R1AW1", "Median": 39.23, "Minimum": 12.59},
         {"name": "T1-R1W1", "Median": 38.89, "Minimum": 35.05},

    ]
    return {"chart_data": data}

@app.post("/process_text") 
async def process_text(input: UserInput):
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input.text}
            ]
        )
        return {"result": response.choices[0].message.content.strip()}
    
    except Exception as e:
        return {"result": f"Error: {str(e)}"}