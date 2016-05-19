# coding: utf-8

T = 2081.44  # T日挂钩标的收盘价
Base = 2309.68  # T日前(含T日)最近一个生成日挂钩标的收盘价
NAV_T = 1.0

NAV_up = max(0.0001, NAV_T + 3 * (T / Base - 1))
NAV_down = 2 * NAV_T - NAV_up
print NAV_up, NAV_down
