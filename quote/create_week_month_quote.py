# coding: utf-8

import logging
import sys
from datetime import date, time

from sqlalchemy import and_

from models import HSIndex, HQ, Quote, Session
from indicator.basic import change_percent


def group_quotes_by_week(quotes):
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


def week_quote_from_days(day_quotes_of_week, quote_class):
    first = day_quotes_of_week[0]
    last = day_quotes_of_week[-1]

    pre_close = first.pre_close
    open = first.open
    high = max(q.high for q in day_quotes_of_week)
    low = min(q.low for q in day_quotes_of_week)
    close = last.close
    volume = sum(q.volume for q in day_quotes_of_week)
    amount = sum(q.amount for q in day_quotes_of_week)
    change = last.close - first.pre_close
    percent = change_percent(close, pre_close)

    week_quote = quote_class(
        market=first.market,
        code=first.code,
        from_date=first.from_date,
        to_date=last.to_date,
        from_time=time(hour=9, minute=15),
        to_time=time(hour=15),
        period='w1',
        name=first.name,
        open=open,
        close=close,
        low=low,
        high=high,
        pre_close=pre_close,
        change=change,
        change_percent=percent,
        volume=volume,
        amount=amount
    )

    if last.turnover:
        estimate_shares = int(last.volume / last.turnover * 100)
        week_quote.turnover = round(float(volume) / estimate_shares * 100, 3)

    return week_quote


if __name__ == '__main__':
    sess = Session()
    indices = sess.query(HSIndex).all()
    for index in indices:
        index_quotes = sess.query(HQ).filter(HQ.code == index.code).all()

    quotes = sess.query(Quote).filter(Quote.code == '600137').order_by(Quote.from_date.asc()).all()
    if quotes:
        week_groups = group_quotes_by_week(quotes)
        for wg in week_groups:
            quote = week_quote_from_days(wg, Quote)
            print quote.to_date, quote.open, quote.high, quote.low, quote.close,\
                quote.volume, quote.amount, quote.turnover
