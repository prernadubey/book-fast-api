#!/bin/bash -ex

docker build -t app --target app .

docker run --rm -it -p 8000:8000 -v test_api:/database app
