# coding: utf-8

import logging
from datetime import date, time

from models import Quote, Session
from indicator.basic import change_percent


def create_week_quotes_group(code):
    sess = Session()
    quotes = sess.query(Quote).filter(Quote.code == code).order_by(Quote.from_date.asc()).all()
    if not quotes:
        return

    first = quotes[0]
    start_week_date = first.from_date
    year = start_week_date.year
    week = start_week_date.isocalendar()[1]
    day_quotes_of_week = [first]
    week_quote_groups = []
    for quote in quotes[1:]:
        quote_date = quote.from_date
        if quote_date.year == year and quote_date.isocalendar()[1] == week:
            day_quotes_of_week.append(quote)
        else:
            week_quote_groups.append(day_quotes_of_week)
            day_quotes_of_week = [quote]
            year = quote.from_date.year
            week = quote.from_date.isocalendar()[1]
    week_quote_groups.append(day_quotes_of_week)

    return week_quote_groups


def week_quote_from_day(days):
    from_date = days[0].from_date
    to_date = days[-1].to_date
    pre_close = days[0].pre_close
    open = days[0].open
    high = max(q.high for q in days)
    low = min(q.low for q in days)
    close = days[-1].close
    volume = sum(q.volume for q in days)
    amount = sum(q.amount for q in days)
    change = days[-1].close - days[0].pre_close
    percent = change_percent(close, pre_close)
    shares = int(days[-1].volume / days[-1].turnover * 100)
    turnover = round(float(volume) / shares * 100, 2)

    week_quote = Quote(
        market=days[0].market,
        code=days[0].code,
        from_date=from_date,
        to_date=to_date,
        from_time=time(hour=9, minute=15),
        to_time=time(hour=15),
        period='w1',
        name=days[0].name,
        open=open,
        close=close,
        low=low,
        high=high,
        pre_close=pre_close,
        change=change,
        change_percent=percent,
        volume=volume,
        amount=amount,
        turnover=turnover
    )

    return week_quote

if __name__ == '__main__':
    sess = Session()
    week_groups = create_week_quotes_group('000418')
    for wg in week_groups:
        week_quote = week_quote_from_day(wg)
        sess.merge(week_quote)
        # print wg[0].from_date.isocalendar()[0], wg[0].from_date.isocalendar()[1]
    sess.commit()
