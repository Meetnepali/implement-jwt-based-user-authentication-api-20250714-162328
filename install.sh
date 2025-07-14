#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if ! command -v docker &> /dev/null; then
  echo -e "${RED}Docker is required but not installed. Aborting.${NC}"
  exit 1
fi

echo -e "${GREEN}Building Docker image...${NC}"
docker-compose build

echo -e "${GREEN}Setting up DB migrations...${NC}"
# Init DB if not exists
if [ ! -f ./test.db ]; then
  touch test.db
fi

echo -e "${GREEN}Install complete.${NC}"
