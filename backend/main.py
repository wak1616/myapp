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
import tempfile
import uuid
import logging

# Load environment variables
load_dotenv()

app = FastAPI(title="OpenAI Responses API Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://derojas.info", "http://derojas.info", 
                  "https://www.derojas.info", "http://www.derojas.info",
                  "http://localhost:5173", "http://127.0.0.1:5173"],  # Added localhost URLs
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
    vector_store_id: str
    model: str = "gpt-4o"

class VectorStoreRequest(BaseModel):
    name: str = "user_files_store"

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

@app.post("/api/create-vector-store")
async def create_vector_store(request: VectorStoreRequest):
    try:
        vector_store = client.vector_stores.create(name=request.name)
        
        return {
            "id": vector_store.id,
            "name": vector_store.name,
            "created_at": vector_store.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    vector_store_id: str = Form(...)
):
    try:
        # Create a temporary file with a safe name to avoid path traversal
        import tempfile
        import uuid
        import os
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        logger.info(f"Received file: {file.filename}, size: {file.size}, vector_store_id: {vector_store_id}")
        
        # Generate a safe filename with UUID while preserving the file extension
        file_ext = os.path.splitext(file.filename)[1].lower()  # Get the file extension including the dot, convert to lowercase
        
        # List of supported file extensions for OpenAI vector stores
        supported_extensions = [".pdf", ".doc", ".docx", ".txt", ".csv", ".json", ".html", ".md"]
        
        if not file_ext or file_ext not in supported_extensions:
            # Try to guess extension from content type or default to .pdf
            content_type = file.content_type
            logger.info(f"Content type: {content_type}")
            
            if "pdf" in content_type:
                file_ext = ".pdf"
            elif "word" in content_type or "docx" in content_type or "doc" in content_type:
                file_ext = ".docx"
            elif "text" in content_type:
                file_ext = ".txt"
            else:
                # Default to PDF if we can't determine
                file_ext = ".pdf"
                
            logger.info(f"File had no extension, setting to: {file_ext} based on content type")
            
        safe_filename = f"{uuid.uuid4()}_{file.filename.replace('/', '_')}"
        
        # Create a temporary file with the extension preserved
        suffix = file_ext  # Use the file extension as the suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            # Read and write the file contents
            contents = await file.read()
            temp_file.write(contents)
            temp_path = temp_file.name
            logger.info(f"Created temporary file at: {temp_path} with extension {file_ext}")
        
        try:
            # Upload file to OpenAI
            logger.info("Uploading file to OpenAI...")
            with open(temp_path, "rb") as f:
                file_response = client.files.create(file=f, purpose="assistants")
            
            logger.info(f"File uploaded successfully with ID: {file_response.id}")
            
            # Attach file to vector store
            logger.info(f"Attaching file to vector store: {vector_store_id}")
            attach_response = client.vector_stores.files.create(
                vector_store_id=vector_store_id,
                file_id=file_response.id
            )
            
            logger.info("File successfully attached to vector store")
            
            return {
                "file_id": file_response.id,
                "filename": file.filename,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error during OpenAI API operations: {str(e)}")
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.info(f"Temporary file removed: {temp_path}")
    except Exception as e:
        import traceback
        logging.error(f"Error in upload_pdf: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/file-search")
async def file_search(request: FileSearchRequest):
    try:
        logger = logging.getLogger(__name__)
        logger.info(f"File search request: prompt='{request.prompt}', vector_store_id='{request.vector_store_id}'")
        
        response = client.responses.create(
            model=request.model,
            input=request.prompt,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [request.vector_store_id]
                }
            ]
        )
        
        logger.info(f"OpenAI response received with ID: {response.id}")
        
        # Extract text and retrieved files
        response_text = ""
        retrieved_files = []
        
        # Safely process response with multiple checks to handle different API response structures
        if hasattr(response, "output") and response.output:
            for output in response.output:
                # Handle file search results
                if hasattr(output, "type") and output.type == "file_search_call":
                    logger.info("Found file_search_call output")
                    if hasattr(output, "file_search"):
                        file_search = output.file_search
                        if hasattr(file_search, "results") and file_search.results:
                            for result in file_search.results:
                                retrieved_files.append({
                                    "filename": getattr(result, "filename", "Unknown"),
                                    "text": getattr(result, "text", ""),
                                    "score": getattr(result, "relevance_score", None)
                                })
                
                # Handle text content
                if hasattr(output, "content") and output.content:
                    for item in output.content:
                        # Check if it's a text type
                        if hasattr(item, "type") and item.type == "text":
                            if hasattr(item, "text"):
                                response_text += item.text
                        # Direct text access (older API versions)
                        elif hasattr(item, "text"):
                            response_text += item.text
        
        logger.info(f"Extracted response text (first 100 chars): {response_text[:100] if response_text else 'No text found'}")
        logger.info(f"Retrieved {len(retrieved_files)} files")
        
        # Return a simplified response that's easier to serialize
        return {
            "id": response.id,
            "text": response_text,
            "retrieved_files": retrieved_files
        }
    except Exception as e:
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error in file_search: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 