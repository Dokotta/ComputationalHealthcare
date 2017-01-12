#!/usr/bin/env bash
docker exec -u="root" -it $(docker ps -l -q)  bash start_server.sh
