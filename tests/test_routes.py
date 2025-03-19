import pytest
from backend.main import app  # Import your Starlette app
from meilisearch.models.task import TaskInfo
from datetime import datetime
from starlette.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

# Mock MeiliSearch client
class MockMeiliSearchClient:
    def __init__(self):
        self.indexes = {}

    def index(self, index_name):
        if index_name not in self.indexes:
            self.indexes[index_name] = MockIndex(index_name)
        return self.indexes[index_name]

class MockIndex:
    def __init__(self, index_name):
        self.index_name = index_name
        self.documents = []

    def add_documents(self, documents):
        self.documents.extend(documents)
        return TaskInfo(
            status="enqueued",
            task_uid=1,
            index_uid=self.index_name,
            type="documentAddition",
            enqueued_at=datetime.now(),
        )

    def search(self, query):
        return {
            "hits": [doc for doc in self.documents if query.lower() in doc.get("title", "").lower()],
            "offset": 0,
            "limit": 20,
            "nbHits": len(self.documents),
            "exhaustiveNbHits": False,
            "processingTimeMs": 1,
            "query": query,
        }

# Fixture to mock the MeiliSearch client
@pytest.fixture
def mock_meilisearch_client(monkeypatch):
    mock_client = MockMeiliSearchClient()
    monkeypatch.setattr("backend.main.meili_client", mock_client)
    return mock_client

# Fixture to create a test client
@pytest.fixture
def client():
    return TestClient(app)

# Test cases
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Welcome to the Backend!"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Test /add endpoint
@pytest.mark.asyncio
async def test_add_documents(client, mock_meilisearch_client):
    # Test valid request
    response = client.post(
        "/add",
        json={
            "index_name": "movies",
            "documents": [
                {"id": 1, "title": "Inception", "genre": "Sci-Fi"},
                {"id": 2, "title": "Interstellar", "genre": "Sci-Fi"},
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "enqueued",
        "taskUid": 1,
        "indexUid": "movies",
        "type": "documentAddition",
        "enqueuedAt": response.json()["enqueuedAt"],  # Check that it exists
    }

    # Test missing index_name
    response = client.post(
        "/add",
        json={
            "documents": [
                {"id": 1, "title": "Inception", "genre": "Sci-Fi"},
            ],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"error": "index_name and documents are required"}

    # Test missing documents
    response = client.post(
        "/add",
        json={
            "index_name": "movies",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"error": "index_name and documents are required"}

# Test /search endpoint
@pytest.mark.asyncio
async def test_search_documents(client, mock_meilisearch_client):
    # Add documents first
    client.post(
        "/add",
        json={
            "index_name": "movies",
            "documents": [
                {"id": 1, "title": "Inception", "genre": "Sci-Fi"},
                {"id": 2, "title": "Interstellar", "genre": "Sci-Fi"},
            ],
        },
    )

    # Test valid search
    response = client.get("/search?index_name=movies&query=Inception")
    assert response.status_code == 200
    assert response.json() == {
        "hits": [{"id": 1, "title": "Inception", "genre": "Sci-Fi"}],
        "offset": 0,
        "limit": 20,
        "nbHits": 2,
        "exhaustiveNbHits": False,
        "processingTimeMs": 1,
        "query": "Inception",
    }

    # Test missing index_name
    response = client.get("/search?query=Inception")
    assert response.status_code == 400
    assert response.json() == {"error": "index_name and query are required"}

    # Test missing query
    response = client.get("/search?index_name=movies")
    assert response.status_code == 400
    assert response.json() == {"error": "index_name and query are required"}

    # Test invalid index
    response = client.get("/search?index_name=invalid&query=Inception")
    assert response.status_code == 200  # Mock returns empty results for invalid index
    assert response.json() == {
        "hits": [],
        "offset": 0,
        "limit": 20,
        "nbHits": 0,
        "exhaustiveNbHits": False,
        "processingTimeMs": 1,
        "query": "Inception",
    }