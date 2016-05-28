# coding: utf-8


class Index(object):
    def __init__(self, market, name, code, listing_date):
        self.market = market
        self.code = code
        self.name = name
        self.listing_date = listing_date


i000001 = Index('sh', '000001', '上证指数', '1990-12-19')
i000016 = Index('sh', '000016', '上证50', '2004-01-02')
i000300 = Index('sh', '000300', '沪深300', '2005-06-30')
i000905 = Index('sh', '000905', '中证500', '2007-01-15')
i399001 = Index('sz', '399001', '深圳成指', '1991-04-03')
i399006 = Index('sz', '399006', '创业板指', '2010-06-01')
i399102 = Index('sz', '399102', '创业板综', '2010-06-01')
