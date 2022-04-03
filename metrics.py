from abc import ABC, abstractmethod
from typing import Any, Callable, Union


class MetricBase(ABC):
    _registry = []

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)

    @classmethod
    def factory(cls, name):
        for metric in cls._registry:
            if metric.name == name:
                return metric.create()

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @abstractmethod
    def do(self, data):
        raise NotImplemented


class MetricKAST(MetricBase):
    name = 'kast'

    def do(self, data):
        """
        Метрика KAST - доля раундов, в которых игрок:
        1. K - кого то убил
        2. A - помог убить
        3. S - выжил в раунде
        4. T - был убит, но был разменен товарищем по команде
        """

        from collections import Counter
        from itertools import chain

        r = {}
        for gameRound in data['gameRounds']:
            r[gameRound['roundNum']] = set()
            _stat = r[gameRound['roundNum']]

            for killNum in gameRound['kills']:
                _stat.add(killNum['attackerName'])

                if killNum['assisterName'] is not None:
                    _stat.add(killNum['assisterName'])

                if killNum['isTrade']:
                    _stat.add(killNum['playerTradedName'])

            if gameRound['frames']:
                last_frame = gameRound['frames'][-1]
                for side in ('t', 'ct'):
                    for player in last_frame[side]['players']:
                        if player['isAlive']:
                            _stat.add(player['name'])

        f: Callable[[Any], Union[float, Any]] = lambda stat: stat / len(r)
        counter = Counter([p for p in chain(*r.values())])

        return [(p, f(stat)) for p, stat in counter.most_common()]
