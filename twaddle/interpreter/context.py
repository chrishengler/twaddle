from dataclasses import dataclass, field
from typing import Optional

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.block_attributes import BlockAttributes
from twaddle.interpreter.formatter import Formatter
from twaddle.interpreter.synchronizer import Synchronizer, sync_types
from twaddle.lookup.lookup_manager import LookupManager
from twaddle.parser.nodes import BlockNode


@dataclass
class TwaddleContext:
    persistent_labels: bool = False
    persistent_synchronizers: bool = False
    persistent_patterns: bool = False
    persistent_clipboard: bool = False
    strict_mode: bool = False

    saved_patterns = dict[str, BlockNode]()
    copied_blocks = dict[str, Formatter]()
    lookup_manager: LookupManager = field(default_factory=LookupManager)
    block_attributes: BlockAttributes = field(default_factory=BlockAttributes)
    synchronizers: dict[str, Synchronizer] = field(default_factory=dict)

    current_regex_match: Optional[str] = None

    def reset_for_new_sentence(self):
        if not self.persistent_patterns:
            self.saved_patterns.clear()
        if not self.persistent_clipboard:
            self.copied_blocks.clear()
        if not self.persistent_synchronizers:
            self.clear_synchronizers()
        if not self.persistent_labels:
            self.lookup_manager.clear_labels()
        self.consume_block_attributes()

    def force_clear(self):
        self.saved_patterns.clear()
        self.copied_blocks.clear()
        self.clear_synchronizers()
        self.lookup_manager.clear_labels()
        self.consume_block_attributes()

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

    def clear_synchronizers(self):
        self.synchronizers.clear()
