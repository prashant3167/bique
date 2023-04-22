#! /bin/bash
set -xueo pipefail

tag=$(git rev-parse --abbrev-ref HEAD)-$(git describe --dirty --always)
# repo='028686181435.dkr.ecr.ap-south-1.amazonaws.com/kafka-gate'

docker buildx build --platform linux/amd64 \
    --progress=plain \
    -t kafka-gate:$tag .