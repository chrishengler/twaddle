# Dictionary Spec

What follows is a very dry specification of the requirements of a Twaddle dictionary file.

## Header
The header section contains definintions of the dictionary name and the forms 
it offers.

### Name

The name is defined by a line beginning `#name `, followed by the name e.g.:

```
#name noun
```

The name may not contain any spaces.

### Forms

The forms are defined by a line beginning `#forms `, followed by a 
space-separated list of the forms available from the dictionary, e.g.

```
#forms singular plural
```

The form names may not contain spaces

For backwards compatibility with dictionary files written for 
[Rant v3](https://github.com/TheBerkin/rant3), the `#forms` line may 
also be written as `#subs`, with the same syntax. This is supported but
not recommended. 

## Definitions

Definition lines begin with a greater than symbol and a space, followed by a 
slash-separated list of the forms for that definition:

 `> parachute/parachutes`

The space is mandatory. The line may begin with the `>` or with any amount of
whitespace, which will be ignored. 

Each entry must contain a definition for each form. 

## Classes

Definitions may be (but are not required to be) sorted into classes.

A class applies to a region in a dictionary file. It is started with the 
directive `#class add <classname>` and ended with the directive
`#class remove <classname>`. Any definitions between the two directives will
be considered a part of the defined class.

Classes may be opened and closed multiple times within a dictionary file, and
may overlap with each other in whole or in part. 