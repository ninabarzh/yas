from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from .meilisearch_client import add_documents, search
from meilisearch import Client
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize MeiliSearch client
try:
    meili_client = Client('http://meilisearch:7700', 'masterKey')
    logger.info("MeiliSearch client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize MeiliSearch client: {e}")
    raise


# Define search function
def search(index_name, query):
    try:
        index = meili_client.index(index_name)
        result = index.search(query)
        return result
    except Exception as e:
        logger.error(f"Error in search function: {e}")
        raise


# Define routes
async def add(request):
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
        index = meili_client.index(index_name)
        task_info = index.add_documents(documents)

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


async def search_docs(request):
    try:
        # Get query parameters
        index_name = request.query_params.get('index_name')
        query = request.query_params.get('query')

        # Validate query parameters
        if not index_name or not query:
            return JSONResponse(
                {"error": "index_name and query are required"},
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


async def homepage(request):
    return PlainTextResponse("Welcome to the Backend!")


async def health(request):
    return JSONResponse({"status": "ok"})


# Create a Router
routes = [
    Route("/", homepage, methods=["GET"]),  # Homepage route
    Route("/add", add, methods=["POST"]),
    Route("/search", search_docs, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
]

# Initialize the app
app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)