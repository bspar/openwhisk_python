#!/usr/bin/env python


def main(*args, **kwargs):
    import logging
    logging.basicConfig(filename=__name__ + '.log')
    logging.warning('  args: {}'.format(args))
    logging.warning('kwargs: {}'.format(kwargs))
    return locals()


if __name__ == '__main__':
    print(main())
