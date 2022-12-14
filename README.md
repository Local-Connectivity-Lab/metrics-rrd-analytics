## Initial setup

Run this command. This ensures that we don't commit notebooks' outputs.

```sh
git config --local include.path ../.gitconfig
```

## Runing the notebook server

Choose one of below options.

### Running in Docker

Bringup:
1. `docker compose up --build -d`
1. Optionally, if you want to use a shell inside the container, then
    `docker compose exec -it main bash`

Teardown:
1. `docker compose down`

### Running on Linux without Docker

Setup:
1. [Install pyenv](https://github.com/pyenv/pyenv#installation)
1. `python -m venv ./venv`

Bringup:
1. `source ./venv/bin/activate`
1. `./start-notebook.sh &`

Teardown:
1. Kill jupyter notebook: `kill %1`
1. `deactivate`

### Running on Colab

Running on Colab is not supported, for now. To run there, we should
- dedicate a Google Drive to storing RRD files as their snapshots
- adapt our utils to scp from production to this Google Drive

1. Go to https://colab.research.google.com/github/
1. Enter the github url of this repo.
