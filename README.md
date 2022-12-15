This repo contains analytics performed on metrics we gather via SNMP.

```
LibreNMS --> rrd databases --> rrdtool fetch --> python graphing libraries
```

Essentially, we extract data from RRD databases, and plot using not `rrdtool` but mainstream graphing libraries.

## First-time setup

Run this command. This ensures that we don't commit notebooks' outputs.

```sh
git config --local include.path ../.gitconfig
```

Install jupyter notebook on the host where you'll be executing `git commit`:

1. `pip install notebook`
    (This installs a notebook globally to your python installation. If you prefer to isolate its installation to this project, see instructions on `venv` below.)

## Runing the notebook server

### Option A: Running in Docker

Bringup:
1. `docker compose up --build -d`
1. Optionally, to use a shell inside the container (without going through a notebook), then
    `docker compose exec -it main bash`

Teardown:
1. `docker compose down`

### Option B: Running without Docker

First-time setup:
1. [Install pyenv](https://github.com/pyenv/pyenv#installation)
1. `python -m venv ./venv`

Bringup:
1. `source ./venv/bin/activate`
1. `./start-notebook.sh &`

Teardown:
1. Kill jupyter notebook: `kill %1`
1. `deactivate`

Caveat: On MacOS, it is unknown whether `brew rrdtool` installs the headers required by python package `rrdtool`. For consistency, MacOS users are recommended to use Docker.

### Option C: Running on Colab

Running on Colab is not supported, for now. To run there, we should
- dedicate a Google Drive to storing RRD files as their snapshots
- adapt our utils to scp from production to this Google Drive

1. Go to https://colab.research.google.com/github/
1. Enter the github url of this repo.

## Accessing the notebook server

http://localhost:8888/
