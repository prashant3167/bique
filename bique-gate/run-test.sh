#! /bin/bash

set -xueo pipefail

CMD="${@}"


if [[ $CMD == '--login' ]]; then
    docker-compose --file docker_images/bique-gate/docker-compose.yml run -e BRANCH_TOKEN=TOKEN_KEY -e CT_USER=USER_KEY2 -e CT_PASS=PASS_KEY2 -v $(pwd)/docker_images/bique-gate/test:/app/test -v $(pwd)/docker_images/bique-gate/test/test-config.toml:/app/config.toml bique-gate bash
else
    docker-compose --file docker_images/bique-gate/docker-compose.yml run -e BRANCH_TOKEN=TOKEN_KEY -e CT_USER=USER_KEY2 -e CT_PASS=PASS_KEY2 -v $(pwd)/docker_images/bique-gate/test:/app/test -v $(pwd)/docker_images/bique-gate/test/test-config.toml:/app/config.toml bique-gate $CMD

fi
