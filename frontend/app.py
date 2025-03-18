from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MEILISEARCH_URL = "http://localhost:7700"
MEILISEARCH_INDEX = "my_index"
# Use the same master key as in docker-compose.yml
# For production, use environment variables
MEILISEARCH_API_KEY = "master_key"

@app.route('/')
def hello():
    return "Hello!"


@app.route('/search')
def search():
    query = request.args.get('q')
    response = requests.get(f"{MEILISEARCH_URL}/indexes/{MEILISEARCH_INDEX}/search", params={'q': query}, headers={'Authorization': f'Bearer {MEILISEARCH_API_KEY}'})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)