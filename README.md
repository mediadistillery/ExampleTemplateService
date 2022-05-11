[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-3614/)

# Media Distillery Example Service Templete

This project contains the Media Distillery example templete service (see [Bitbucket](https://bitbucket.org/mediadistillery/md-dl-face-clustering)).

## Getting Started

### Configuration

Follow these steps to set up the configuration file:

```shell

mkdir -p /etc/service-templete-test-service/

cp dlfaceclustering-config.yaml /etc/service-templete-test-service/

```

Update any configuration as necessary. The template contains defaults for all variables.

### Installing

The actual service can be installed from Nexus (see [Nexus PyPI](https://mediadistillery.atlassian.net/wiki/spaces/DW/pages/21496105/Setting+up+Nexus+as+your+Extra+PyPI+repository) setup).

```shell

pip install service-templete-test-service

```

Or with poetry (requires Nexus configuration inside your destination [pyproject.toml](example-service-templete-service/pyproject.toml)):

```shell

poetry add service-templete-test-service

```

### Usage

To start the service run:

```bash

example_service_templete_web_start

```

Or use the alias:

```bash

run-cli

```

Also starts a Prometheus client server on port `8080` by default. It can be disabled with the configuration.

Swagger/OpenAPI documentation is available at http://localhost:5000/docs.


## Deployment

To be filled 

## Versioning

To be filled 

```bash

pip install service-templete-test-service==some-random-text

```

This will output all the available versions.

## Authors

* **Anustup** anustup@mediadistillery.com


## License

This project does not have a license but we are working on it.

## Changelog

* `0.1.0`
    * First Version of the example templete service

    




