#!/bin/bash

cd "$(dirname "$0")/.."
source venv/bin/activate
#python -m app.main
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8010
