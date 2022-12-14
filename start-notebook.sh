#!/usr/bin/env bash

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

exec jupyter notebook --no-browser --ip=0.0.0.0 --port=8888 --NotebookApp.token=''
