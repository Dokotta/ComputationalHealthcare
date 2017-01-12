#!/usr/bin/env bash
set -xe
docker run -p 127.0.0.1:8888:8888 -p 127.0.0.1:8111:8000 -d -t computationalhealthcare