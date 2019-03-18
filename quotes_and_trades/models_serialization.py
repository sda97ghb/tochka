def serialize_ticker(ticker):
    return {
        'id': ticker.id,
        'name': ticker.name
    }


def serialize_quote(quote):
    return {
        'date': quote.date,
        'open': quote.open,
        'close': quote.close,
        'low': quote.low,
        'high': quote.high,
        'volume': quote.volume
    }


def serialize_trade(trade):
    return {
        'insider': trade.insider,
        'relation': trade.relation,
        'last_date': trade.last_date,
        'transaction_type': trade.transaction_type,
        'owner_type': trade.owner_type,
        'shares_traded': trade.shares_traded,
        'last_price': trade.last_price,
        'shares_held': trade.shares_held
    }
