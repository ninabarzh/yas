import json
import logging
from meilisearch import Client
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

# Set up logging
logger = logging.getLogger(__name__)

# Initialize MeiliSearch client
try:
    meili_client = Client('http://meilisearch:7700', 'masterKey')
    logger.info("MeiliSearch client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize MeiliSearch client: {e}")
    raise

# Add documents to MeiliSearch
def add_documents(index_name, documents):
    """
    Add documents to a MeiliSearch index.
    """
    try:
        index = meili_client.index(index_name)
        task_info = index.add_documents(documents)
        logger.info(f"Documents added to index '{index_name}' successfully.")
        return task_info
    except Exception as e:
        logger.error(f"Error adding documents to index '{index_name}': {e}")
        raise

# Define search function
def search(index_name, query):
    """
    Search for documents in a MeiliSearch index.
    """
    try:
        index = meili_client.index(index_name)
        if not index:
            raise ValueError(f"Index '{index_name}' does not exist")
        result = index.search(query)
        logger.info(f"Search completed for query '{query}' in index '{index_name}'.")
        return result
    except Exception as e:
        logger.error(f"Error searching index '{index_name}' with query '{query}': {e}")
        raise

# Handle file upload
async def upload_file(request: Request):
    """
    Handle file upload and add documents to MeiliSearch.
    """
    try:
        # Parse the uploaded file
        form_data = await request.form()
        file = form_data["file"]
        content = await file.read()
        logger.debug("Uploaded file content: %s", content)  # Debugging
        documents = json.loads(content)

        # Add documents to the index
        task_info = add_documents("ossfinder", documents)

        # Return the task info
        return JSONResponse({
            "status": task_info.status,
            "taskUid": task_info.task_uid,
            "indexUid": task_info.index_uid,
            "type": task_info.type,
            "enqueuedAt": task_info.enqueued_at.isoformat() if task_info.enqueued_at else None,
        })
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON file: {e}")
        return JSONResponse({"error": "Invalid JSON file"}, status_code=400)
    except Exception as e:
        logger.error(f"Error in /upload endpoint: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# Add documents via JSON payload
async def add(request):
    """
    Add documents to MeiliSearch via JSON payload.
    """
    try:
        # Parse request data
        data = await request.json()
        index_name = data.get('index_name')
        documents = data.get('documents')

        # Validate request data
        if not index_name or not documents:
            return JSONResponse(
                {"error": "index_name and documents are required"},
                status_code=400,
            )

        # Add documents to MeiliSearch
        task_info = add_documents(index_name, documents)

        # Convert datetime to string
        enqueued_at_str = task_info.enqueued_at.isoformat() if task_info.enqueued_at else None

        # Extract relevant data from TaskInfo object
        response_data = {
            "status": task_info.status,
            "taskUid": task_info.task_uid,
            "indexUid": task_info.index_uid,
            "type": task_info.type,
            "enqueuedAt": enqueued_at_str,  # Use the string representation
        }

        return JSONResponse(response_data)
    except Exception as e:
        logger.error(f"Error in /add endpoint: {e}")
        return JSONResponse(
            {"error": "Internal Server Error", "details": str(e)},
            status_code=500,
        )

# Search documents
async def search_docs(request):
    """
    Search for documents in a MeiliSearch index.
    """
    try:
        # Get query parameters
        # index_name = request.query_params.get('index_name')
        # query = request.query_params.get('query')
        # temp solution: small steps, first with a default index of ossfinder
        query = request.query_params.get('query')
        index_name = request.query_params.get('index_name', 'ossfinder')  # Default index

        # # Validate query parameters
        # if not index_name or not query or not query.strip():
        #     return JSONResponse(
        #         {"error": "index_name and query are required and query cannot be empty"},
        #         status_code=400,
        #     )

        # Validate query parameters
        if not query or not query.strip():
            return JSONResponse(
                {"error": "query is required and cannot be empty"},
                status_code=400,
            )

        # Perform search
        result = search(index_name, query)

        # Return search results
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"Error in /search endpoint: {e}")
        return JSONResponse(
            {"error": "Internal Server Error", "details": str(e)},
            status_code=500,
        )


# Homepage route
async def homepage(request):
    return PlainTextResponse("Welcome to the Backend!")

# Health check route
async def health(request):
    return JSONResponse({"status": "ok"})

# Create a Router
routes = [
    Route("/", homepage, methods=["GET"]),  # Homepage route
    Route("/upload", upload_file, methods=["POST"]),
    Route("/add", add, methods=["POST"]),
    Route("/search", search_docs, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
]

# Initialize the app
app = Starlette(routes=routes)

# Add CORS middleware
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # Allow requests from the frontend
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)