from twaddle.parser.transformer import TwaddleTransformer
from twaddle.parser.twaddle_parser import Lark_StandAlone

parser = Lark_StandAlone(propagate_positions=True)
# tree = parser.parse(r"\a {<noun>|group of <noun.plural>} <verb.ed> <adv>")
tree = parser.parse(
    r"\a <noun.plural-circular-!square::!=a::^=b::=c> or not? [if:[gt:\d;5];hat;cat]"
)
# tree = parser.parse(r"[if:[gt:\d;5];hat;cat]")
# tree = parser.parse("[gt:\\a;5]")
# tree = parser.parse("\a cat")
# tree = parser.parse("[if:hello;hello;goodbye]")
print(tree.pretty())

transformer = TwaddleTransformer()

transformed_tree = transformer.transform(tree)
print(f"{transformed_tree=}")
