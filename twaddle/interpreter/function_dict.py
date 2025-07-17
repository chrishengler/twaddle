from .function_definitions import (
    case,
    first,
    hide,
    last,
    match,
    rand,
    repeat,
    separator,
    sync,
)

function_definitions = {
    "rep": repeat,
    "sep": separator,
    "rand": rand,
    "first": first,
    "last": last,
    "x": sync,
    "sync": sync,
    "case": case,
    "match": match,
    "hide": hide,
}
