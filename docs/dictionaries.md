# Dictionaries

Twaddle has no in-built vocabulary. Its vocabulary is read from
dictionary files within a folder specified when creating the
TwaddleRunner. Each user can provide a vocabulary appropriate for
their purposes by adding dictionary files to a folder of their choice.

The format of these dictionary files must follow the 
[dictionary spec](dictionary_spec.md). Some sample dictionaries are provided
in the `twaddle/sample_dicts` folder. These are intended purely as examples
to show how a dictionary file looks and allow users to experiment writing 
Twaddle sentences before writing their own dictionaries. 

Let's look at an example, an abridged version of `noun.dic`:

```
#name noun
#forms singular plural

> paperweight/paperweights
> air freshener/air fresheners
> bird/birds
> baseball/baseballs
> desk/desks

#class add building
    > apartment/apartments
    > bungalow/bungalows
    > house/houses
    #class add retail
        > shop/shops
        > market/markets
        > mall/malls
    #class remove retail
#class remove building
```

It consists of a header section and a number of definitions. 

## Header

````
#name noun
#forms singular plural
````

The first line defines the name of the dictionary (`noun`). Once loaded by a
TwaddleRunner, this dictionary can be used in Twaddle sentences by typing
`<noun>`.

The second line defines the forms offered by the dictionary (`singular` and
`plural`). The first form is the default form which will be used whenever no
form is explicitly requested.

## Definitions

Following the header, we define our vocabulary 

```
> paperweight/paperweights
> air freshener/air fresheners
> bird/birds
> baseball/baseballs
> desk/desks

#class add building
    > apartment/apartments
    > bungalow/bungalows
    > house/houses
    #class add retail
        > shop/shops
        > market/markets
        > mall/malls
    #class remove retail
#class remove building


#class add vehicle
    > bus/buses
    > car/cars
    > helicopter/helicopters
    > hovercraft/hovercrafts
    > motorbike/motorbikes
    > truck/trucks
    > van/vans
    #class add retail
        > food truck/food trucks
        > ice cream van/ice cream vans
    #class remove retail
#class remove vehicle
```

Each entry line begins with a greater than symbol followed by a space `> `
(the space is mandatory). Then follows the word in each form, separated
by slashes. In this case, our forms defined in the header were `singular`
and `plural`, so each definition consists of the singular form of the word
(e.g. `paperweight`), then a slash, then the plural form (`paperweights`). 

Any definitions which occur before the header are ignored.

Words within a dictionary can be categorised by adding classes. A class 
is added with the `#class add <name>` directive, and removed with the
`#class remove <name>` directive. Any definitions between the two are 
considered to belong to that class. Classes may be added and removed multiple
times within a file (as with the retail class in this example) and their
active regions may overlap in whole or in part. In the example above, `desk`
does not belong to any class, `house` belongs to the `building` class, and
`shop` belongs to both the `building` and the `retail` class. 

## Comments

Lines which do not match the expected format for header information or
definitions are ignored. As such, comments can be added by simply including
them as plain text, provided the first non-whitespace character is not `>`
