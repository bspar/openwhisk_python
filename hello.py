#!/usr/bin/env python

from __future__ import print_function
from sys import stderr


def main(*args, **kwargs):
    name = kwargs.get('name', 'stranger')
    print(name, file=stderr)
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"greeting": greeting}


if __name__ == '__main__':
    print(main(name=__name__))
    print(main())
