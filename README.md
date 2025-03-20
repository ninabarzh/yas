# YAS (Under Construction)

Yet Another Search engine: a project with [MeiliSearch](https://www.meilisearch.com/) as the backend, 
[Starlette](https://www.starlette.io/) with [Jinja2 templates](https://jinja.palletsprojects.com/en/stable/) as the 
frontend, and [Docker](https://www.docker.com/) for containerization, to be deployed to 
[Hetzner](https://www.hetzner.com/) using [Sliplane](https://sliplane.io/).

And because meilisearch volumes did not persist 
([ongoing since version 0.23](https://github.com/meilisearch/meilisearch/issues/1969), so years now), we decided to use 
PostgreSQL to store Meilisearch’s metadata for data persistence in production. Other solutions did not seem clean enough
for production. As `root` it works. Not doing that in production, thank you.

The postgres volume did not persist either, not with a named volume, and not even with a bind mount solution, which is
not a good choice for production anyway. This suggests that the issue might not be related to Docker volumes or bind 
mounts but rather to how Meilisearch is handling the data internally, possibly to drive projects to their cloud 
solution, which supports BigTech. 

Something we vowed not to contribute to. We keep this repo for later, and start a new repo [trying out another search 
engine, Typesense](https://github.com/ninabarzh/pers).

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

## Deployment
We're living in this insane technologically caused cognitive dissonance, hence we are keeping it as light as possible 
and to avoid BigTech clouds, we are using Hetzner ([Finland](https://app.electricitymaps.com/map/72h/hourly) has a 
low carbon impact). And pricing is transparent and straightforward, making estimates on cost easy.