from typing import Union

from awpy import DemoParser


class Demo:
    def __init__(self, path: str, data: Union[dict, None] = None):
        self._path = path
        self._data = data

    def __call__(self, *args, **kwargs) -> dict:
        if self._data is None:
            self._data = DemoParser(demofile=self._path, parse_rate=128).parse()
        return self._data

    @property
    def data(self):
        return self()

    @property
    def d(self):
        # Shortcut
        return self.data
