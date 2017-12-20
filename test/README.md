# Testing

This directory contains scripts and files needed to test your module's code.

## Setup

Much as I tried, the docs didn't help me much.

Testing in the vm.

Built and tagged docker container by hand.

Followed most of the instructions (need to recreate what worked).

Ended up using the following line for unit tests:

```
../kb_sdk/bin/kb-sdk test
```

where kb_sdk is installed as a sibling directory.

Basically, using a locally build kb-sdk and not the dockerized one.

The dockerized kb-sdk doesn't work (complains about not being in a module directory).

### test.cfg

Also, for the jgi-token, note that it looks like this in test.cfg

```
secure.jgi_token=*my secure token*
```

```
test_token=<your kbase dev token>

kbase_endpoint=https://ci.kbase.us/services

auth_service_url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login
auth_service_url_allow_insecure=true

secure.jgi_token=<jgi basic auth token>

secure.mongo_db=jgi_gateway
secure.mongo_host=172.17.0.2
secure.mongo_port=27017
secure.mongo_user=jgi_gateway
secure.mongo_pwd=test

secure.job_monitoring=false
```

Note that other configuration properties specific to the jgi search service are hard-coded in the deploy.cfg
