This repo contains analytics performed on metrics we gather via SNMP.

```
LibreNMS --> RRD databases --> rrdtool fetch --> python graphing libraries
```

Essentially, we extract data from RRD databases, and plot using not `rrdtool` but mainstream graphing libraries.

## First-time setup

```sh
# Ensure we don't commit notebooks' outputs.
git config --local include.path ../.gitconfig

# The git hook we added above runs a `jupyter` command. We need to install it.
# First, install a python version manager, e.g. pyenv.
# (make sure you follow the directions from the pyenv installer to modify your shell's .rc file)
curl https://pyenv.run | bash
# Install python with version specified in `.python-version`.
pyenv install --skip-existing
# It's ok to install notebook globally (rather than in a venv).
pip install notebook

cp ./.env.example ./.env
# Then modify `.env` with correct values.
```

## Connection setup

1. Connect to the SCN management VPN (the main one).
1. Some devices have flaky ssh connectivity. To work around it, change your local computer's OpenVPN interface's MTU.
    1. `ip address` --> determine the OpenVPN interface. It should be named `utun0` or similar.
    1. `sudo ip link set dev utun0 mtu 1300`
    - You might have to set this every time your local computer's OpenVPN process is restarted.
    - These `iproute2` commands work on MacOS after `brew install iproute2mac`.

## Runing the notebook server

### Option A: Running in Docker

Bringup:
1. `docker compose up --build -d`
1. Optionally, to use a shell inside the container (without going through a notebook),
    `docker compose exec -it main bash`
1. Go to http://localhost:8888/

Teardown:
1. `docker compose down`

### Option B: Running in venv

First-time setup:
```sh
sudo apt update
sudo apt install -y rrdtool librrd-dev libsqlite3-dev libbz2-dev sshpass

pip install ipykernel
python -m ipykernel install --user --name="${PWD##*/}"
python -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt
deactivate
```

Bringup:
1. `source ./venv/bin/activate`
1. `./start-notebook.sh &`
1. Go to http://localhost:8888/
1. Select the kernel that's named same as this dir.

Teardown:
1. Kill jupyter notebook: `kill %1`
1. `deactivate`

Caveat: On MacOS, it is unknown whether `brew install rrdtool` installs the headers required by the python package `rrdtool`. For consistency, MacOS users are recommended to use Docker.

### Option C: Running on Colab

Running on Colab is not supported, for now. To run there, we should
- dedicate a Google Drive to storing RRD files as their snapshots
- adapt our utils to scp from production to this Google Drive
