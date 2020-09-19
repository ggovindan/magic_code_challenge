#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
export PYTHONPATH=${SCRIPT_DIR}/src:${SCRIPT_DIR}/test

pytest -v test/
