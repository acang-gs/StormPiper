#! /usr/bin/env sh

docker-compose -f docker-stack.yml exec stormpiper-test pytest "$@"
