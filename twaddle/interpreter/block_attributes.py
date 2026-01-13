from typing import Optional

from twaddle.compiler.compiler_objects import RootObject
from twaddle.interpreter.formatting_object import FormattingStrategy


class BlockAttributes:
    def __init__(self):
        self.repetitions: int = 1
        self.separator: RootObject | None = None
        self.first: RootObject | None = None
        self.last: RootObject | None = None
        self.synchronizer: str | None = None
        self.synchronizer_type: str | None = None
        self.hidden: bool = False
        self.reverse: bool = False
        self.save_as: Optional[str] = None
        self.copy_as: Optional[str] = None
        self.abbreviate: bool = False
        self.abbreviation_case: Optional[FormattingStrategy] = None
        self.max_decimals: Optional[int] = None


class BlockAttributeManager:
    def __init__(self):
        self.saved_blocks = dict()
        self.current_attributes = BlockAttributes()

    def get_attributes(self) -> BlockAttributes:
        attributes = self.current_attributes
        self.current_attributes = BlockAttributes()
        return attributes

    def set_synchronizer(self, args: list[str]):
        self.current_attributes.synchronizer = args[0]
        if len(args) > 1:
            self.current_attributes.synchronizer_type = args[1]

    def save_block(self, name: str):
        self.current_attributes.save_as = name

    def copy_block(self, name: str):
        self.current_attributes.copy_as = name

    def clear(self):
        self.current_attributes = BlockAttributes()
