from abc import ABC, abstractmethod
from typing import List

from demo_loader import Demo
from metrics import MetricBase


class MetricExecutorBase(ABC):

    def __init__(self, metrics: List[str], data: Demo):
        self.metrics = [MetricBase.factory(metric) for metric in metrics]
        self.data = data.d
        self.result = {}

    @abstractmethod
    def execute(self):
        raise NotImplemented


class MetricExecutor(MetricExecutorBase):

    def execute(self):
        for metric in self.metrics:
            self.result[metric.name] = metric.do(self.data)
