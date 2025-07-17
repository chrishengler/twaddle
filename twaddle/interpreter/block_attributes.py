from twaddle.compiler.compiler_objects import RootObject


class BlockAttributes:
    def __init__(self):
        self.repetitions: int = 1
        self.separator: RootObject | None = None
        self.first: RootObject | None = None
        self.last: RootObject | None = None
        self.synchronizer: str | None = None
        self.synchronizer_type: str | None = None
        self.hidden: bool = False


class BlockAttributeManager:
    def __init__(self):
        self.current_attributes = BlockAttributes()

    def get_attributes(self) -> BlockAttributes:
        attributes = self.current_attributes
        self.current_attributes = BlockAttributes()
        return attributes

    def set_synchronizer(self, args: list[str]):
        self.current_attributes.synchronizer = args[0]
        if len(args) > 1:
            self.current_attributes.synchronizer_type = args[1]

    def clear(self):
        self.current_attributes = BlockAttributes()
