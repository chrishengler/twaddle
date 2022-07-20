from twaddle.interpreter.synchronizer import (
    CyclicDeckSynchronizer,
    DeckSynchronizer,
    LockedSynchronizer,
    SynchronizerManager,
)


def test_synchronizer_manager():
    locked = SynchronizerManager.create_synchronizer("x", "locked", 1)
    assert isinstance(locked, LockedSynchronizer)


def test_locked_synchronizer():
    locked = LockedSynchronizer(10)
    pick = locked.next()
    for _ in range(0, 10):
        assert locked.next() == pick


def test_deck_synchronizer():
    deck = DeckSynchronizer(10)
    results = dict[int:int]()
    for value in range(0, 10):
        results[value] = 0
    for _ in range(0, 20):
        value = deck.next()
        results[value] = results[value] + 1
    for value in range(0, 10):
        assert results[value] == 2


# noinspection SpellCheckingInspection
def test_cyclic_deck_synchronizer():
    cdeck = CyclicDeckSynchronizer(10)
    results1 = list()
    results2 = list()

    for _ in range(0, 10):
        results1.append(cdeck.next())
    for _ in range(0, 10):
        results2.append(cdeck.next())
    for n in range(0, 10):
        assert results1[n] == results2[n]
