#!/bin/bash
# Run nanobot simulation with proper Python path
cd "$(dirname "$0")"
export PYTHONPATH="${PWD}"
python3 main.py "$@"
