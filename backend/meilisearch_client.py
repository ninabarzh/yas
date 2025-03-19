from meilisearch import Client

# Initialize MeiliSearch client
meili_client = Client('http://localhost:7700', 'masterKey')

def add_documents(index_name, documents):
    index = meili_client.index(index_name)
    return index.add_documents(documents)

def search(index_name, query):
    index = meili_client.index(index_name)
    return index.search(query)