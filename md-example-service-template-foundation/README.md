The foundation library contains shared python code that can be reused in the Python projects.

# Installation from repo
Run the following commands:
```
sudo apt-get install libyaml-dev
cd <install-directory>/md-example-service-template-foundation
poetry update
poetry build
```

Alternatively, install the module from nexus:
```
pip install md-foundation
```

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


### Release Notes 
1.0.0: Change log one can maintain for each release.
