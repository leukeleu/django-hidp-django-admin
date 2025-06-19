#!/bin/bash

docker compose run --rm --no-deps --no-TTY --entrypoint make python lint
