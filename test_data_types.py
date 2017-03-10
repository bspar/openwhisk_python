#!/usr/bin/env python


def main(t_str='t_str', t_int=1, t_float=1.2, t_list=[0, 1], t_tuple=(0, 1),
         t_dict={'a': 0, 'b': 1}):
    return locals()


if __name__ == '__main__':
    print(main())
