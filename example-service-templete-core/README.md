[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-3614/)

# Media Distillery Face Clustering Core

This project contains the Media Distillery face clustering core (see [Bitbucket](https://bitbucket.org/mediadistillery/md-dl-face-clustering)).

## Getting Started

### Installing

The actual service can be installed from Nexus (see [Nexus PyPI](https://mediadistillery.atlassian.net/wiki/spaces/DW/pages/21496105/Setting+up+Nexus+as+your+Extra+PyPI+repository) setup).

```shell

pip install example-service-templete-core

```

Or with poetry (requires Nexus configuration inside your destination [pyproject.toml](pyproject.toml)):

```shell

poetry add example-service-templete-core

```

## Running the tests

This project uses `pytest` for its tests.

If not done so already, first install the library:

```bash

poetry install

```

Then run the tests:

```bash

poetry run pytest tests/

```

## Versioning

We use [SemVer](http://semver.org/) for versioning. See [Nexus](http://nexus/) for all the available versions. Or use `pip` if you have the Nexus PyPI setup (see [Nexus PyPI](https://mediadistillery.atlassian.net/wiki/spaces/DW/pages/21496105/Setting+up+Nexus+as+your+Extra+PyPI+repository) setup).

```bash

pip install example-service-templete-core==<Version>

```

This will output all the available versions.

## Authors

* **Amgad** amgad@mediadistillery.com
* **Timo van Niedek** timo@mediadistillery.com

## License

This project does not have a license because it's not intended to be publicly available.

## Changelog

* `1.0.0-rc-1`
    * First version. add hdbscan clusterer
* `1.2.0`
  * Added post processing to merge similar clusters. [rc.0]
  * Review comment. Endpoint param for postprocessing. [rc.1]
  * Code cleaned and moved to face_clusterer_factory. [rc.2]
  * Code structure change for post_processing. [rc.3]
  * Keeping track of the merged clusters related work.[rc.4 - rc.5]
  * Added unit tests and structural changes. [rc.6]
