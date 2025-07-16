from twaddle.interpreter.block_attributes import BlockAttributeManager, BlockAttributes


def test_add_and_get_attributes():
    bam = BlockAttributeManager()
    bam.current_attributes.repetitions = 3
    bam.current_attributes.separator = "and"
    attributes: BlockAttributes = bam.get_attributes()
    new_attributes: BlockAttributes = bam.get_attributes()
    assert attributes.repetitions == 3
    assert attributes.separator == "and"
    assert new_attributes.repetitions == 1
    assert new_attributes.separator is None
