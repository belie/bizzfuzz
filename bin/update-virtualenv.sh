#!/usr/bin/env bash

if [ "$#" -lt "2" ]; then
    echo "USAGE: $0 <project_dir> <virtual_env_dir>"
    exit 1
fi
PROJECT_DIR=$1
VENV=$2

# Create a virtualenv if it doesn't exist.
#VENV="${PROJECT_DIR}/$PROJECT_ENV"
PYTHON="${VENV}/bin/python"
if [ ! -f "${PYTHON}" ]; then
    echo "creating python virtualenv ${VENV}"
    virtualenv-2.7 $VENV
fi

echo "updating python dependencies."

${VENV}/bin/pip install -r "${PROJECT_DIR}/requirements.txt"

if [ "x$?" != "x0" ]; then
    echo "unable to install python dependencies.  check your network and try again."
    exit 1
fi
