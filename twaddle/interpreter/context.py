from dataclasses import dataclass, field

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.block_attributes import BlockAttributes
from twaddle.interpreter.synchronizer import Synchronizer, sync_types
from twaddle.lookup.lookup_manager import LookupManager


@dataclass
class TwaddleContext:
    lookup_manager: LookupManager = field(default_factory=LookupManager)
    block_attributes: BlockAttributes = field(default_factory=BlockAttributes)
    synchronizers: dict[str, Synchronizer] = field(default_factory=dict)

    def reset_for_new_sentence(self):
        pass

    def consume_block_attributes(self) -> BlockAttributes:
        attrs = self.block_attributes
        self.block_attributes = BlockAttributes()
        return attrs

    def synchronizer_exists(self, name: str) -> bool:
        return name in self.synchronizers

    def create_synchronizer(
        self, name: str, sync_type: str, length: int
    ) -> Synchronizer:
        self.synchronizers[name] = sync_types[sync_type](length)
        return self.synchronizers[name]

    def get_synchronizer(self, name: str) -> Synchronizer:
        if not self.synchronizer_exists(name):
            raise TwaddleInterpreterException(
                f"[TwaddleContext.get_synchronizer] tried to access non-existing synchronizer {name}"
            )
        return self.synchronizers[name]

    def clear(self):
        self.synchronizers.clear()
