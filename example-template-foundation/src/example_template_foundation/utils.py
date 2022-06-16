import logging
import os
import pathlib
import typing

logger = logging.getLogger(__name__)

PathLike = typing.Union[str, pathlib.Path]


class DefaultSpringCloudConfigParser:
    def _extract_name(self, name: str) -> str:
        basename = os.path.basename(name)
        return os.path.splitext(basename)[0]

    def __call__(self, raw_data: dict, *args, **kwargs) -> dict:
        expected = raw_data['name']
        for source in raw_data['propertySources']:
            if source['name'].endswith('application.yaml'):
                config = source['source']
                break
        else:
            logger.warning('No application.yaml found in response; using empty config as base')
            config = {}

        names = []
        for source in raw_data['propertySources']:
            if source['name'].endswith('application.yaml'):
                continue
            else:
                name = self._extract_name(source['name'])
                names.append(name)
                config.update(source['source'])
        if expected not in names:
            raise ValueError("expected config with name '{}' was not found in response".format(expected))

        return config
