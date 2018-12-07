# coding: utf-8

from decimal import Decimal


cn_number_unit = {
    u'%': 1,
    u'元': 1,
    u'万': 10**4,
    u'亿': 10**8
}


def cn_text_to_number(text):
    """
        Convert text to number:
            '21.62亿' --> 21.62 * 10^8
            '3215万' --> 3215 * 10^5
            '18.6%' --> 0.186
    """

    # TODO: Check regex match numbers: \-?[0-9]*(\.[0-9]*)?

    if isinstance(text, str):
        text = text.decode('utf8')

    if not text[-1] in cn_number_unit:
        return Decimal(text)

    unit = cn_number_unit.get(text[-1])
    return Decimal(text[0:-1]) * Decimal(unit)


def cn_text_to_int(text):
    num = cn_text_to_number(text)
    return int(num) if num is not None else None


def cn_text_to_float(text):
    num = cn_text_to_number(text)
    return float(num) if num is not None else None


def stock_market(code):
    return 'sh' if code[0] == '6' else 'sz'


def index_market(code):
    from const import index_market
    return index_market.get(code)


if __name__ == '__main__':
    n = cn_text_to_number('21.62亿'.decode('utf8'))
    assert n == int(21.62 * 10**8)
    n = cn_text_to_number('3215万')
    assert n == 3215 * 10**4

    try:
        _ = cn_text_to_number('-')
    except Exception as e:
        print(e)
