class BlockAttributes:
    def __init__(self):
        self.repetitions: int = 1
        self.separator: str = ""
        self.first: str = ""
        self.last: str = ""
        self.synchronizer: str | None = None
        self.synchronizer_type: str | None = None


class BlockAttributeManager:
    current_attributes = BlockAttributes()

    @staticmethod
    def get_attributes() -> BlockAttributes:
        attributes = BlockAttributeManager.current_attributes
        BlockAttributeManager.current_attributes = BlockAttributes()
        return attributes

    @staticmethod
    def set_synchronizer(args: list[str]):
        BlockAttributeManager.current_attributes.synchronizer = args[0]
        if len(args) > 1:
            BlockAttributeManager.current_attributes.synchronizer_type = args[1]

    @staticmethod
    def clear():
        BlockAttributeManager.current_attributes = BlockAttributes()
