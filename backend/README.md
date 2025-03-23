# OpenAI Responses API Demo Backend

This is a FastAPI backend for demonstrating the OpenAI Responses API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and add your OpenAI API key.

5. Run the server:
```bash
python run.py
```

The server will be available at http://localhost:8000.

## API Endpoints

- `GET /`: Home endpoint
- `POST /api/simple-prompt`: Simple text prompt
- `POST /api/continue-conversation`: Continue a conversation
- `POST /api/web-search`: Web search using OpenAI's web search tool
- `POST /api/multimodal`: Process multimodal inputs (text + image)
- `POST /api/upload-image`: Upload an image for multimodal processing

## Documentation

FastAPI automatically generates documentation for the API endpoints.
Access the documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc) 