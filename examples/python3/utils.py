# -*- coding: utf-8 -*-


def check_is_all_digit(*args, **kwargs):
    to_check = [i for i in args]
    [to_check.append(i) for i in kwargs.values()]

    for i in to_check:
        if not '{}'.format(i).isdigit():
            return False

    return True
