import copy
import json
import logging
import pathlib
import re

import requests
import yaml

from example_template_foundation.utils import PathLike, DefaultSpringCloudConfigParser

logger = logging.getLogger(__name__)


class ConfigurationMixin:
    """
    Configuration class mixin. Should be called once during initialization.
    """

    def load_config(self, config=None, default_location=None):
        logger.debug('Loading ConfigurationManager')
        if config is not None:
            logger.debug('from passed argument')
            self._config = config
        else:
            if default_location is None:
                raise ValueError('default location is required if no configuration instance is provided')
            logger.debug('from default location at {}'.format(default_location))
            self._config = ConfigurationManager.from_path(default_location)

    @property
    def config(self):
        return self._config


def flatten_dict(data):
    def expand(key, value):
        if isinstance(value, dict):
            return [(key + '.' + k, v) for k, v in flatten_dict(value).items()]
        else:
            return [(key, value)]

    items = [item for k, v in data.items() for item in expand(k, v)]

    return dict(items)


def reindex_list(data):
    pattern = '\[\d+\]'  # looking for instances like hello[0], goodbye[1]
    incorrect_indexed_items = [k for k, v in data.items() if re.search(pattern, k)]
    for item in incorrect_indexed_items:
        correct_name = re.sub(pattern, '', item)
        if correct_name in data:
            data[correct_name].append(data[item])
        else:
            data[correct_name] = [data[item]]
    return data


class ConfigurationManager:
    """
    Configuration class that contains a dictionary with all configuration options as loaded from a YAML/JSON formatted
    file or remote Spring Cloud Config URL.

    :param should_reindex_list: = Boolean to indicate whether to iterate through the configurations to load correctly
    for spring cloud.
    """

    def __init__(self, data: dict, location: str, flatten=False, should_reindex_list=True):
        self._data = copy.deepcopy(data)
        if flatten:
            self._data = flatten_dict(self._data)
        if should_reindex_list:
            self._data = reindex_list(self._data)
        self._location = str(location)

    @property
    def data(self):
        return self._data

    @property
    def location(self):
        return self._location

    def __contains__(self, item):
        return item in self.data

    def __getitem__(self, item):
        return self.data[item]

    def get(self, item, default=None):
        return self.data.get(item, default)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.data, self.location)

    def __str__(self):
        s = '{}('.format(self.__class__.__name__)
        s += '{},\n'.format(json.dumps(self.data, indent=2, sort_keys=True))
        s += '{!r}\n)'.format(self.location)
        return s

    def refresh(self):
        self._data = ConfigurationManager.from_path(self.location).data

    def _validate_path(self, filepath: PathLike) -> pathlib.Path:
        if filepath is None:
            if self.location.startswith(('http://', 'https://')):
                raise ValueError('filepath argument is required if the configuration was retrieved from remote')
            else:
                return pathlib.Path(self.location)
        else:
            return pathlib.Path(filepath)

    def to_file(self, filepath: PathLike = None, **kwargs):
        filepath = self._validate_path(filepath)
        if filepath.suffix.lower().endswith(('yaml', 'yml')):
            self.to_yaml_file(filepath, **kwargs)
        elif filepath.suffix.lower().endswith('json'):
            self.to_json_file(filepath, **kwargs)
        else:
            raise NotImplementedError("extension '{}' is not supported".format(filepath.suffix))

    def to_json_file(self, filepath: PathLike = None, **_):
        filepath = self._validate_path(filepath)
        with open(str(filepath), 'w') as f:
            json.dump(self.data, f)

    def to_yaml_file(self, filepath: PathLike = None, *, safe=True):
        filepath = self._validate_path(filepath)
        with open(str(filepath), 'w') as f:
            yaml.dump(self.data, f, yaml.SafeDumper if safe else yaml.Dumper)

    @classmethod
    def from_path(cls, filepath_or_url, **kwargs) -> 'ConfigurationManager':
        if str(filepath_or_url).startswith(('http://', 'https://')):
            return cls.from_remote(filepath_or_url, **kwargs)
        else:
            return cls.from_file(filepath_or_url, **kwargs)

    @classmethod
    def from_file(cls, filepath: PathLike, **kwargs) -> 'ConfigurationManager':
        filepath = pathlib.Path(filepath)
        if filepath.suffix.lower().endswith(('yaml', 'yml')):
            return cls.from_yaml_file(filepath, **kwargs)
        elif filepath.suffix.lower().endswith('json'):
            return cls.from_json_file(filepath, **kwargs)
        else:
            raise NotImplementedError("extension '{}' is not supported".format(filepath.suffix))

    @classmethod
    def from_yaml_file(cls, filepath: PathLike, *, safe=True, **kwargs) -> 'ConfigurationManager':
        with open(str(filepath), 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader if safe else yaml.FullLoader)
            if data is None:
                raise IOError('failed to load YAML file; is the file empty?')
            return cls(data, str(filepath), **kwargs)

    @classmethod
    def from_json_file(cls, filepath: PathLike, **kwargs) -> 'ConfigurationManager':
        with open(str(filepath), 'r') as f:
            data = json.load(f)
            return cls(data, str(filepath), **kwargs)

    @classmethod
    def from_remote(
        cls, url: str, *, parser: callable = DefaultSpringCloudConfigParser(), **kwargs
    ) -> 'ConfigurationManager':
        response = requests.get(url)
        if not response.ok:
            response.raise_for_status()
        raw = response.json()
        config = parser(raw)
        return cls(config, str(url), **kwargs)
