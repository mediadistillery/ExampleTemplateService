[![Python 3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-3614/)
 <a href="">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/example-template-service"></a>

#  Example Template Core

The core library may contain python code that is core to a specific project which mainly deals with the business logic, such as model initialization, inference and data pre- or post-processing.

## Getting Started

### Installation from repo
Run the following commands:
```
sudo apt-get install libyaml-dev
cd <install-directory>/example-template-core
poetry update
poetry build
```

Alternatively, install the module from nexus:
```
pip install example-template-core
```

### Build

Individual packages can be build with

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

* **Your_Name** your_mail@address.com

## License

MIT.

### Release Notes 
* `0.1.0`
    * First Version of the example templete core

    




