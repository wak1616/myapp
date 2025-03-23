# OpenAI Responses API Demo

This application demonstrates how to use the OpenAI Responses API with its various functions, including stateful conversations, web search, and multimodal capabilities.

## Project Structure

- **Frontend**: Vue.js with Vuetify for the UI
- **Backend**: Python with FastAPI

## Features

The application demonstrates the following features of the OpenAI Responses API:

1. **Simple Prompt**: Send a basic text prompt and get a response
2. **Continue Conversation**: Maintain a conversation state and continue the conversation
3. **Web Search**: Use OpenAI's web search tool to search the internet
4. **Multimodal**: Process both text and images in a single request

## Setup

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install the dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file based on `.env.example` and add your OpenAI API key.

6. Start the backend server:
```bash
python run.py
```

The backend will run on http://localhost:8000.

### Frontend

1. In the root directory, install the dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will run on http://localhost:5173 (or another port if 5173 is in use).

## Usage

1. Open your browser and navigate to http://localhost:5173
2. Use the different tabs to try out the various features of the Responses API:
   - **Simple Prompt**: Send a single prompt and get a response
   - **Continue Conversation**: Continue the conversation with follow-up messages
   - **Web Search**: Ask questions that require searching the web
   - **Multimodal**: Upload an image and ask questions about it

## Documentation

For more information about the OpenAI Responses API, see the [official documentation](https://platform.openai.com/docs). 