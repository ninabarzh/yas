from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
import httpx

# Define routes
async def health(request):
    return JSONResponse({"status": "ok"})

async def homepage(request):
    return PlainTextResponse("Welcome to the Frontend!")

async def search(request):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'http://backend:8000/search',
            params=request.query_params
        )
        return JSONResponse(response.json())


# Create a Router
routes = [
    Route("/", homepage, methods=["GET"]),  # Homepage route
    Route("/search", search, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
]

# Initialize the app
app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
