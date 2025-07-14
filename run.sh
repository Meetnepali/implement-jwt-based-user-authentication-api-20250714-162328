#!/bin/bash
set -e

./install.sh

echo "Starting containers..."
docker-compose up
