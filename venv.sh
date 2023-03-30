#/bin/sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
VENVPATH="$SCRIPTPATH/.venv"

if [ ! -d "$VENVPATH" ]; then
    /usr/bin/env python3 -m venv "$VENVPATH"
fi

$VENVPATH/bin/pip3 install -r "$SCRIPTPATH/requirements.txt"