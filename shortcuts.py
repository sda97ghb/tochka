from quotes_and_trades.data_replication.data_replication import replicate as replicate_quotes_and_trades


def replicate(number_of_threads=4):
    replicate_quotes_and_trades(number_of_threads)
