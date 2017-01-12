#!/usr/bin/env bash
set -xe
./start_container.sh.sh
./prepare_nrd.sh
./start_ui.sh &
