# coding: utf-8

from decimal import Decimal


def change_percent(value, base):
    exp_two_places = Decimal((0, (1,), -2))  # Decimal(10) ** -2
    change = Decimal((value-base)/base * 100).quantize(exp_two_places)
    return change
