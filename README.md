# YAS (Under Construction)

Yet Another Search engine: a project with MeiliSearch as the backend, Starlette as the frontend, and Docker for 
containerization, to be deployed to Hetzner using Sliplane.

## Build and run the containers

Up:
```commandline
docker-compose up --build
```

Down (and remove):
```commandline
docker-compose down
```

## Access the services:

* MeiliSearch: http://localhost:7700
* Backend: http://localhost:8000
* Frontend: http://localhost:8001
