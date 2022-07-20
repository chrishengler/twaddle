from twaddle.interpreter.block_attributes import BlockAttributeManager, BlockAttributes


def test_add_and_get_attributes():
    BlockAttributeManager.current_attributes.repetitions = 3
    BlockAttributeManager.current_attributes.separator = "and"
    attributes: BlockAttributes = BlockAttributeManager.get_attributes()
    new_attributes: BlockAttributes = BlockAttributeManager.get_attributes()
    assert attributes.repetitions == 3
    assert attributes.separator == "and"
    assert new_attributes.repetitions == 1
    assert new_attributes.separator == ""
