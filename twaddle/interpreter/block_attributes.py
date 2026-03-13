from dataclasses import dataclass
from typing import Optional

from twaddle.interpreter.formatting_object import FormattingStrategy
from twaddle.parser.nodes import RootNode


@dataclass
class BlockAttributes:
    repetitions: int = 1
    separator: Optional[RootNode] = None
    first: Optional[RootNode] = None
    last: Optional[RootNode] = None
    synchronizer: Optional[str] = None
    synchronizer_type: Optional[str] = None
    hidden: bool = False
    reverse: bool = False
    save_as: Optional[str] = None
    copy_as: Optional[str] = None
    abbreviate: bool = False
    abbreviation_case: Optional[FormattingStrategy] = None
    max_decimals: Optional[int] = None
    while_predicate: Optional[RootNode] = None
    while_iteration = 0
    max_while_iterations = 100

    def set_synchronizer(self, args: list[str]):
        self.synchronizer = args[0]
        if len(args) > 1:
            self.synchronizer_type = args[1]
