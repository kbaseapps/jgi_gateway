#!/usr/bin/bash

root=$(git rev-parse --show-toplevel)
source_dir=lib
container_root=/kb/module

# Note that this uses mongo auth, so requires a local mongo container.
# see local-development.md

docker run -i -t \
  --network=kbase-dev \
  --name=jgi_gateway  \
  --dns=8.8.8.8 \
  -e "KBASE_ENDPOINT=https://ci.kbase.us/services" \
  -e "AUTH_SERVICE_URL=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login" \
  -e "AUTH_SERVICE_URL_ALLOW_INSECURE=true" \
  -e "KBASE_SECURE_CONFIG_PARAM_mongo_db=jgi_gateway" \
  -e "KBASE_SECURE_CONFIG_PARAM_mongo_host=mongo" \
  -e "KBASE_SECURE_CONFIG_PARAM_mongo_port=27017" \
  -e "KBASE_SECURE_CONFIG_PARAM_mongo_user=jgi_gateway" \
  -e "KBASE_SECURE_CONFIG_PARAM_mongo_pwd=jgi_gateway" \
  --mount type=bind,src=${root}/test_local/workdir,dst=${container_root}/work \
  --mount type=bind,src=${root}/${source_dir},dst=${container_root}/${source_dir} \
  --rm  test/jgi_gateway:dev 
