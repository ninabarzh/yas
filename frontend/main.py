from starlette.applications import Starlette
from starlette.responses import HTMLResponse, FileResponse, JSONResponse
from starlette.routing import Route
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

# Configure Jinja2 environment
templates = Environment(
    loader=FileSystemLoader("templates"),  # Load templates from the "templates" directory
    autoescape=select_autoescape(["html", "xml"]),
)

# Frontend routes
async def search_page(request):
    template = templates.get_template("search.html")
    return HTMLResponse(template.render(title="Search Data"))

async def upload_page(request):
    template = templates.get_template("upload.html")  # Use the new upload template
    return HTMLResponse(template.render(title="Upload Data"))


app = Starlette(
    routes=[
        Route("/", search_page),  # Home page (search)
        Route("/upload", upload_page),  # Upload data to index
    ],
)
