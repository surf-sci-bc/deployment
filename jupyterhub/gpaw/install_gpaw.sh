#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GPAW_PATH=$(sed 's/.*0, '\''\(.*\)'\'')/\1/' "${SCRIPT_DIR}/rc.py")

echo -e "make sure that the potentials are installed to \"${GPAW_PATH}\" from each single user home path"

for hp in /home/jupyter-*; do
    mkdir -p "${hp}/.gpaw"
    cp rc.py "${hp}/.gpaw/"
done
