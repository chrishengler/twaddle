class BlockAttributes:
    def __init__(self):
        self.repetitions: int = 1
        self.separator: str = ''
        self.first: str = ''
        self.last: str = ''



class BlockAttributeManager:
    current_attributes = BlockAttributes()

    @staticmethod
    def get_attributes() -> BlockAttributes:
        attributes = BlockAttributeManager.current_attributes
        BlockAttributeManager.current_attributes = BlockAttributes()
        return attributes

