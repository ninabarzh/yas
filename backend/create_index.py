import requests

MEILISEARCH_URL = "http://localhost:7700"
MASTER_KEY = "masterKey"
INDEX_NAME = "ossfinder"

# Create the index
response = requests.post(
    f"{MEILISEARCH_URL}/indexes",
    headers={"Authorization": f"Bearer {MASTER_KEY}"},
    json={"uid": INDEX_NAME}
)
print("Create index response:", response.json())

# Upload documents
with open("data.json", "rb") as file:
    response = requests.post(
        f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/documents",
        headers={
            "Authorization": f"Bearer {MASTER_KEY}",
            "Content-Type": "application/json"  # Add the Content-Type header
        },
        data=file
    )
    print("Upload documents response:", response.json())
