# AskAurora

AskAurora is a FastAPI-based application designed to handle natural language queries and provide intelligent answers using a combination of FAISS indexing and a large language model (LLM).

## Features
- **Data Ingestion**: Automatically pulls and processes raw data to build a FAISS index.
- **Query Handling**: Accepts user queries and retrieves relevant data using FAISS.
- **LLM Integration**: Uses a large language model to generate answers based on the retrieved data.
- **REST API**: Provides a `/ask` endpoint for querying the system.

## Requirements
- Python 3.10
- `uvicorn` for running the FastAPI application
- Dependencies listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sg6428/AskAurora.git
   cd AskAurora
   ```

2. Set up a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API at `http://127.0.0.1:8000`.

3. Use the `/ask` endpoint to send queries. Example:
   ```bash
   curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "How many cars does Vikram Desai have?"}'
   ```

## Docker
1. Build the Docker image:
   ```bash
   docker build -t askaurora .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 askaurora
   ```

## Docker Compose
1. Build and start the services:
   ```bash
   docker-compose up
   ```

2. The application will be available at `http://127.0.0.1:8000`.

3. To stop the services:
   ```bash
   docker-compose down
   ```

## Testing
Run the test suite to ensure everything is working correctly:
```bash
python test/test_api.py
```

## Configuration
The application uses environment variables for configuration. Key settings include:
- `RAW_DATA_DIR`: Directory for raw data storage (default: `data/raw_data`).
- `API_URL`: URL for external API integration (default: `https://november7-730026606190.europe-west1.run.app/messages`).
- `PAGE_LIMIT`: Pagination limit for data (default: `500`).
- `MODEL`: LLM model identifier (default: `gpt-oss:20b-cloud`).