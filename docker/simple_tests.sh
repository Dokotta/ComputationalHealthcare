#!/usr/bin/env bash
set -xe
./start.sh
./prepare_nrd.sh
./start_ui.sh &
sleep 50
