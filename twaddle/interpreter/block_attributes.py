class BlockAttributes:
    def __init__(self):
        self.repetitions: int = 1
        self.separator: str = ""
        self.first: str = ""
        self.last: str = ""
        self.synchronizer: str | None = None
        self.synchronizer_type: str | None = None


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
