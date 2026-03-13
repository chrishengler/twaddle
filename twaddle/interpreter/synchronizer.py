from abc import ABC, abstractmethod
from random import randrange, shuffle


class Synchronizer(ABC):
    def __init__(self, num_choices: int):
        self.num_choices = num_choices

    @abstractmethod
    def next(self) -> int:
        pass


class LockedSynchronizer(Synchronizer):
    def __init__(self, num_choices: int):
        super().__init__(num_choices)
        self.pick = randrange(0, num_choices)

    def next(self) -> int:
        return self.pick


class DeckSynchronizer(Synchronizer):
    def __init__(self, num_choices: int):
        super().__init__(num_choices)
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
        super().__init__(num_choices)
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


sync_types = {
    "locked": LockedSynchronizer,
    "deck": DeckSynchronizer,
    "cdeck": CyclicDeckSynchronizer,
}
