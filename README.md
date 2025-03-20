# YAS (Under Construction)

Yet Another Search engine: a project with [MeiliSearch](https://www.meilisearch.com/) as the backend, 
[Starlette](https://www.starlette.io/) with [Jinja2 templates](https://jinja.palletsprojects.com/en/stable/) as the 
frontend, and [Docker](https://www.docker.com/) for containerization, to be deployed to 
[Hetzner](https://www.hetzner.com/) using [Sliplane](https://sliplane.io/).

We're living in this insane technologically caused cognitive dissonance, hence we are keeping it as light as possible 
and to avoid BigTech clouds, we are using Hetzner ([Finland](https://app.electricitymaps.com/map/72h/hourly) has a 
low carbon impact). And pricing is transparent and straightforward, making estimates on cost easy.

## Build and run the containers

Up:
```commandline
docker-compose up --build
```

Down (and remove):
```commandline
docker-compose down
```

## Access the services (development):

* MeiliSearch: http://localhost:7700
* Backend: http://localhost:8000
* Frontend: http://localhost:8001/upload
