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

Note that other configuration properties specific to the jgi search service are hard-coded in the deploy.cfg
