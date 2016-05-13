# coding: utf-8

text_number_unit = {
    u'%': 0.01,
    u'元': 1,
    u'万': 10000,
    u'亿': 100000000
}


def text_to_number(text):
    """
        Convert text to number:
            '21.62亿' --> 21.62 * 100000000
            '3215万' --> 3215 * 10000
            '18.6%' --> 0.186
    """
    if not text or len(text) < 2:
        return 0
    unit = text_number_unit.get(text[-1])
    if unit:
        return float(text[0:-1]) * unit
    else:
        return float(text)


def stock_market(code):
    return 'sh' if code[0] == '6' else 'sz'
