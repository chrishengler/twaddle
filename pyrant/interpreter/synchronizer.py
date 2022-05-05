from abc import ABC, abstractmethod
from random import randrange
from rant_exceptions import RantInterpreterException


class Synchronizer(ABC):
    @abstractmethod
    def next(self) -> int:
        pass


class LockedSynchronizer(Synchronizer):
    def __init__(self, num_choices: int):
        self.pick = randrange(0, num_choices)

    def next(self) -> int:
        return self.pick


class SynchronizerManager:
    sync_types = {'locked': LockedSynchronizer, }
    synchronizers = dict[str, Synchronizer]()

    @staticmethod
    def synchronizer_exists(name: str) -> bool:
        return name in SynchronizerManager.synchronizers

    @staticmethod
    def create_synchronizer(name: str, sync_type: str, length: int) -> Synchronizer:
        SynchronizerManager.synchronizers[name] = SynchronizerManager.sync_types[sync_type](length)
        return SynchronizerManager.synchronizers[name]

    @staticmethod
    def get_synchronizer(name: str) -> Synchronizer:
        if not SynchronizerManager.synchronizer_exists(name):
            raise RantInterpreterException(
                f"[SynchronizerManager.get_synchronizer] tried to access non-existing synchronizer {name}")
        return SynchronizerManager.synchronizers[name]
