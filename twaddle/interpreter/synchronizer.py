from abc import ABC, abstractmethod
from random import randrange, shuffle

from twaddle.exceptions import TwaddleInterpreterException


class Synchronizer(ABC):
    @abstractmethod
    def next(self) -> int:
        pass


class LockedSynchronizer(Synchronizer):
    def __init__(self, num_choices: int):
        self.pick = randrange(0, num_choices)

    def next(self) -> int:
        return self.pick


class DeckSynchronizer(Synchronizer):
    def __init__(self, num_choices: int):
        self.num_choices = num_choices
        self.deck = list()
        self.shuffle_deck()

    def shuffle_deck(self):
        self.deck = list(range(0, self.num_choices))
        shuffle(self.deck)

    def next(self) -> int:
        if len(self.deck) == 0:
            self.shuffle_deck()
        return self.deck.pop(0)


class CyclicDeckSynchronizer(Synchronizer):
    def __init__(self, num_choices: int):
        self.num_choices = num_choices
        self.deck = list()
        self.shuffle_deck()
        self.pos = 0

    def shuffle_deck(self):
        self.deck = list(range(0, self.num_choices))
        shuffle(self.deck)

    def next(self) -> int:
        self.pos = self.pos + 1
        if self.pos == self.num_choices:
            self.pos = 0
        return self.deck[self.pos]


class SynchronizerManager:

    sync_types = {
        "locked": LockedSynchronizer,
        "deck": DeckSynchronizer,
        "cdeck": CyclicDeckSynchronizer,
    }

    def __init__(self):
        self.synchronizers = dict[str, Synchronizer]()

    def synchronizer_exists(self, name: str) -> bool:
        return name in self.synchronizers

    def create_synchronizer(
        self, name: str, sync_type: str, length: int
    ) -> Synchronizer:
        self.synchronizers[name] = SynchronizerManager.sync_types[sync_type](length)
        return self.synchronizers[name]

    def get_synchronizer(self, name: str) -> Synchronizer:
        if not self.synchronizer_exists(name):
            raise TwaddleInterpreterException(
                f"[SynchronizerManager.get_synchronizer] tried to access non-existing synchronizer {name}"
            )
        return self.synchronizers[name]

    def clear(self):
        self.synchronizers.clear()
