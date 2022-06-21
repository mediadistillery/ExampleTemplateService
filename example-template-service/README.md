 <a href="">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/example-template-service"></a>

#  Example Template Service

This project contains the Example Service Template (see [Github](https://github.com/mediadistillery/ExampleTemplateService.git)).
This project mainly is an example FastApi implementation where there is just an Add function implemented and returns an addition of a list of numbers. 

## Getting Started

### Configuration

Follow these steps to set up the configuration file:

```shell

mkdir -p /etc/example-template-service/

cp default_config.yml /etc/example-template-service/config.yml

```

Update any configuration as necessary. The template contains defaults for all variables.

### Installing

The actual service can be installed from PyPI (see [PyPI](https://pypi.org/)).

```shell

pip install example-template-service

```

Or with poetry:

```shell

poetry add example-template-service

```

> You need to have Poetry installed. It can be installed with pip. See the Poetry [docs](https://python-poetry.org/docs/) for more installations options.

The library can be installed for development like this with Poetry:
```shell
poetry install
```

Or using the requirements.txt:
```shell
pip install -r requirements.txt
pip install -e .
```

### Usage

To start the service run:

```bash

example_template_service_web_start

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

pip install example-template-service==some-random-text

```

This will output all the available versions.

### Build

Individual packages can be build with

```bash

poetry build

```
and published to PYPI using
```bash

 twine upload -r package_name dist/*

```

Or with Poetry

```bash

poetry publish

```

### Docker
To build a docker image for the service, run this command from the current directory:

> docker build --build-arg VERSION=$(poetry version --short) --tag example-template-service:$(poetry version --short) --file docker/Dockerfile .

To run that docker image, run this command:

> docker run -p 5000:5000 -p 8080:8080 example-template-service 

## Authors

* **Anustup** anustup@mediadistillery.com
* **Ryan** ryan@mediadistillery.com


## License

MIT.

## Changelog

* `0.1.0`
    * First Version of the example template service

    




