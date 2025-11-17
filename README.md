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

# Basic Message Data Analysis

The table below summarizes the contribution of the top 5 most active members to the total message volume, followed by a complete list of all users.

#### Total Messages by User (Top 5)

| Rank | User Name | Total Messages | Percentage of Total |
| :--- | :--- | :--- | :--- |
| 1 | Lily O'Sullivan | 71 | 12.20% |
| 2 | Amina Van Den Berg | 70 | 12.03% |
| 3 | Layla Kawaguchi | 69 | 11.86% |
| 4 | Fatima El-Tahir | 68 | 11.68% |
| 5 | Armand Dupont | 63 | 10.82% |

| Total Unique Users | Total Messages |
| :--- | :--- |
| 10 | 582 |

#### Complete Message Breakdown

| User Name | Total Messages | Percentage of Total |
| :--- | :--- | :--- |
| **Lily O'Sullivan** | **71** | **12.20%** |
| **Amina Van Den Berg** | **70** | **12.03%** |
| **Layla Kawaguchi** | **69** | **11.86%** |
| **Fatima El-Tahir** | **68** | **11.68%** |
| **Armand Dupont** | **63** | **10.82%** |
| Hans Müller | 63 | 10.82% |
| Thiago Monteiro | 61 | 10.48% |
| Sophia Al-Farsi | 60 | 10.31% |
| Lorenzo Cavalli | 58 | 9.97% |
| Vikram Desai | 59 | 10.14% |

## Anamolies in Data
- Few users (e.g. Sophia Al-Farsi) appear multiple times in the data with different User IDs

## Design Choices

### Alternate Approaches

- Simpler approach: create a document DB sharded by `user_id` to improve relevance from a user's message history. When a question contains a user name, confine retrieval to that user's message history and send the asked question plus only that user's data to the LLM for answering.

### Future Scope

1. Currently using a sentences list for message lookup after vector search; a better approach is to use a key-value cache or an in-memory DB such as Redis for scalability.
2. Use batch processing at regular intervals to pull data from the API and update the index.
3. Currently using an in-memory vector index with limited data; consider using a dedicated vector DB service for larger scale and persistence.

### Used Optimizations

1. Use of ThreadPoolExecutor for pulling raw data in parallel with multiple workers.
2. Vector index building strategy: concatenating `user_name + message` so semantic vector lookup is more accurate for user-scoped queries.
