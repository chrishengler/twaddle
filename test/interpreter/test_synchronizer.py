from interpreter.synchronizer import *


def test_synchronizer_manager():
    locked = SynchronizerManager.create_synchronizer('x', 'locked',1)
    assert isinstance(locked, LockedSynchronizer)

def test_locked_synchronizer():
    locked = LockedSynchronizer(10)
    pick = locked.next()
    for _ in range(0,10):
        assert locked.next() == pick
