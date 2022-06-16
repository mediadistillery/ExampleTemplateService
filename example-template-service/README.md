[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-3614/)

#  Example Service Template

This project contains the Example Service Templete (see [Github](https://github.com/mediadistillery/ExampleTemplateService.git)).
This project mainly is an example FastApi implementation where there is just an Add function implemented and returns an addition of a list of numbers. 

## Getting Started

### Configuration

Follow these steps to set up the configuration file:

```shell

mkdir -p /etc/service-templete-test-service/

cp default_config.yml /etc/service-templete-test-service/

```

Update any configuration as necessary. The template contains defaults for all variables.

### Installing

The actual service can be installed from PyPI (see [PyPI](https://pypi.org/)).

```shell

pip install service-templete-test-service

```

Or with poetry:

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

Service can be accessed through:

```bash

example-template-service/script/request.py

```

Also starts a Prometheus client server on port `8080` by default. It can be disabled with the configuration.

Swagger/OpenAPI documentation is available at http://localhost:5000/docs.




```bash

pip install service-templete-test-service==some-random-text

```

This will output all the available versions.

### Build

Indivitual packages can be build with

```bash

poetry build

```
and published to PYPI using
```bash

 twine upload -r packahe_name dist/*

```

Or with Poetry

```bash

poetry publish

```

## Authors

* **Anustup** anustup@mediadistillery.com
* **Ryan** ryan@mediadistillery.com


## License

MIT.

## Changelog

* `0.1.0`
    * First Version of the example templete service

    




