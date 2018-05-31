#!/usr/bin/env python

from __future__ import print_function
from sys import stderr

# input datatypes: ['name']
# output datatypes: ['greeting', 'foo']
def main(args):
    name = args.get('name', 'stranger')
    operation = args.get('operation', 'global')
    print(name, file=stderr)
    greeting = 'Hello ' + name + '!'
    print(greeting)
    return {'data':{'greeting':greeting, 'foo':'bar'},
            'operation':operation}
