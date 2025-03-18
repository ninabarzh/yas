# YAS

Yet Another Searchengine: A MeiliSearch backend with a Python Flask frontend and an Nginx reverse proxy.

## Build and Run the Docker Containers

Navigate to the directory containing the docker-compose.yml file and run:

```commandline
docker-compose up --build
```
This will build the Python frontend image and start the MeiliSearch, Python frontend, and Nginx containers.

## Interacting with MeiliSearch

### Temporary

* https://www.meilisearch.com/docs/guides/misc/docker

Copy the `data.json` file into the MeiliSearch container:

```commandline
docker cp data.json meilisearch:/data.json
```

Use curl to load the data into MeiliSearch:

```commandline
curl -X POST 'http://localhost:7700/indexes/ossfinder/documents' \
     -H 'Authorization: Bearer master_key' \
     -H 'Content-Type: application/json' \
     --data-binary @data.json
```

Replace your_master_key_here with the actual master key. 

## Access the application

* MeiliSearch: Access the MeiliSearch dashboard at http://localhost:7700/.
* Python Frontend Search page: Access the application at http://localhost:5000/search.
