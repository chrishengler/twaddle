# Synchronizers

Synchronizers greatly extend what can be achieved with 
[branching sentences](branching.md). A synchronizer can be applied to 
multiple branching sections within a sentence to require various 
relationships between the branches chosen. A synchronizer is defined by
placing the `sync` function before a set of branches:

`[sync:<name>;<type>]{first branch|second branch}`

Subsequent uses of the synchronizer need only specify the name:

`[sync:<name>]{first branch|second branch}`

The name may be any arbitrary text without special characters.

Using a single synchronizer within a sentence has no effect, but by applying
the same synchronizer to multiple sets of branches, later branches can be 
chosen according to various relationships to the initial choice.

When using synchronizers it is important that every set of branches the 
synchronizer is applied to should have the same number of branches available.
Where this is not the case the sentence will still run, but the synchronizer 
may not behave as expected.

## Synchronizer types

Synchronizers deal with each set of branches based on the order in which they
are defined.

### Locked

The `locked` synchronizer is perhaps the simplest. The same choice will be made
for every set of branches encountered. For example, if the second branch is
chosen on the first set of branches, then subsequent branches with the
synchronizer will also pick the second branch. 

`[sync:s;locked]{first|second}, [sync:s]{first|second}`

may produce 

`first, first`

or 

`second, second`

but never `first, second`

### Deck

The `deck` synchronizer treats the branches as a deck of cards. It counts the
number of branches and generates a permutation of the branch order, which is
followed until it is exhausted.

`[sync:s;deck]{A|K|Q}, [sync:s]{A|K|Q}, [sync:s]{A|K|Q}`

may produce outputs like:

`A, K, Q`, `Q, K, A`, `K, A, Q`, etc.

but will never produce

`A, A, K`, `K, Q, Q`,

or any other variation which uses the same branch
multiple times.

If the synchronizer is applied to more branch sets than the number of branches
it has, it is shuffled again once the full deck is used up. So the input:

`[sync:s;deck]{a|b} [sync:s]{a|b} [sync:s]{a|b} [sync:s]{a|b}`

may produce `abab`, `abba`, `baab`, or `baba`, but never `bbaa` or `babb`

### Cyclic deck

The `cdeck` synchronizer is a cyclic deck. It behaves as the `deck` 
synchronizer, except that if the deck size is exhausted it repeats from the
beginning rather than being shuffled again. So the input:

`[sync:s;cdeck]{a|b} [sync:s]{a|b} [sync:s]{a|b} [sync:s]{a|b}`

may produce as output `abab` or `baba`, but never `baab`.