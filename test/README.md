# Testing

This directory contains scripts and files needed to test your module's code.

## Setup
To run this app you will need to set a few additional parameters in your test.cfg

```
test_token=<your kbase dev token>

kbase_endpoint=https://ci.kbase.us/services

auth_service_url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login
auth_service_url_allow_insecure=true

secure.jgi_token=<jgi basic auth token>
secure.mongo_db=jgi_gateway
secure.mongo_host=localhost
secure.mongo_port=27017
```

Note that other configuration properties specific to the jgi search service are hard-coded in the deploy.cfg
