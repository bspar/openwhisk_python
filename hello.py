#!/usr/bin/env python

def main(params):
    name = params.get("name", "stranger")
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"greeting": greeting}


if __name__ == '__main__':
    main({'name': __name__})
