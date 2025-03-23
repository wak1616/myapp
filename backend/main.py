from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union, Literal
import json
import base64

# Load environment variables
load_dotenv()

app = FastAPI(title="OpenAI Responses API Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Models
class SimplePromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"

class ContinueConversationRequest(BaseModel):
    prompt: str
    response_id: str
    model: str = "gpt-4o-mini"

class WebSearchRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o"

class FileSearchRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o"
    file_ids: List[str]

class MultimodalRequest(BaseModel):
    prompt: str
    image_url: str
    model: str = "gpt-4o"
    use_web_search: bool = False

# Routes
@app.get("/")
async def root():
    return {"message": "OpenAI Responses API Demo"}

@app.post("/api/simple-prompt")
async def simple_prompt(request: SimplePromptRequest):
    try:
        response = client.responses.create(
            model=request.model,
            input=request.prompt,
        )
        
        # Extract text from response
        response_text = ""
        if response.output and len(response.output) > 0:
            for content in response.output:
                if hasattr(content, "content") and content.content:
                    for item in content.content:
                        if hasattr(item, "text"):
                            response_text += item.text
        
        return {
            "id": response.id,
            "text": response_text,
            "full_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/continue-conversation")
async def continue_conversation(request: ContinueConversationRequest):
    try:
        response = client.responses.create(
            model=request.model,
            input=request.prompt,
            previous_response_id=request.response_id
        )
        
        # Extract text from response
        response_text = ""
        if response.output and len(response.output) > 0:
            for content in response.output:
                if hasattr(content, "content") and content.content:
                    for item in content.content:
                        if hasattr(item, "text"):
                            response_text += item.text
        
        return {
            "id": response.id,
            "text": response_text,
            "full_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/web-search")
async def web_search(request: WebSearchRequest):
    try:
        response = client.responses.create(
            model=request.model,
            input=request.prompt,
            tools=[
                {
                    "type": "web_search"
                }
            ]
        )
        
        # Extract text and web search results
        response_text = ""
        web_search_results = []
        
        if response.output and len(response.output) > 0:
            for output in response.output:
                if output.type == "web_search_call":
                    web_search_results.append(output)
                elif hasattr(output, "content") and output.content:
                    for item in output.content:
                        if hasattr(item, "text"):
                            response_text += item.text
                        if hasattr(item, "annotations"):
                            web_search_results.extend(item.annotations)
        
        return {
            "id": response.id,
            "text": response_text,
            "web_search_results": web_search_results,
            "full_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/multimodal")
async def multimodal(request: MultimodalRequest):
    try:
        tools = []
        if request.use_web_search:
            tools.append({"type": "web_search"})
        
        # Handle either direct URLs or base64 data URLs
        image_content = request.image_url
        
        response = client.responses.create(
            model=request.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": request.prompt},
                        {"type": "input_image", "image_url": image_content}
                    ]
                }
            ],
            tools=tools if tools else None
        )
        
        # Extract text and results
        response_text = ""
        annotations = []
        
        if response.output and len(response.output) > 0:
            for output in response.output:
                if hasattr(output, "content") and output.content:
                    for item in output.content:
                        if hasattr(item, "text"):
                            response_text += item.text
                        if hasattr(item, "annotations"):
                            annotations.extend(item.annotations)
        
        return {
            "id": response.id,
            "text": response_text,
            "annotations": annotations,
            "full_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the file content
        contents = await file.read()
        
        # Convert to base64
        encoded_string = base64.b64encode(contents).decode("utf-8")
        
        # You might want to save the image temporarily or send it directly
        # Here we'll just return the base64 string
        return {"filename": file.filename, "base64": encoded_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 