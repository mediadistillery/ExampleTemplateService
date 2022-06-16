[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-3614/)
 <a href="">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/example-template-service"></a>

#  Example Template Foundation

The foundation library contains shared python code that can be reused in the Python projects.

## Getting Started

### Installation from repo
Run the following commands:
```
sudo apt-get install libyaml-dev
cd <install-directory>/example-template-foundation
poetry update
poetry build
```

Alternatively, install the module from PYPI:
```
pip install example-template-foundation
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
1.0.0: Change log one can maintain for each release.
