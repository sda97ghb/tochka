import csv
import itertools
from io import StringIO
from urllib.parse import urlparse, ParseResult, parse_qs

import requests
from bs4 import BeautifulSoup


class Trades:
    def __init__(self, header, records):
        self.header = header
        self.records = records

    def __iter__(self):
        return TradesIterator(self.header, self.records)

    @property
    def is_empty(self):
        return len(self.records) <= 0


class TradesIterator:
    def __init__(self, header, records):
        self.header = header
        self.records = records
        self.index = 0

    def __next__(self):
        if self.index >= len(self.records):
            raise StopIteration
        else:
            record = self.records[self.index]
            self.index = self.index + 1
            return dict(zip(self.header, record))


DEFAULT_MAX_PAGES = 10


def get(ticker, max_pages=DEFAULT_MAX_PAGES):
    header, records = get_as_header_and_records(ticker, max_pages)
    return Trades(header, records)


def get_as_csv(ticker, max_pages=DEFAULT_MAX_PAGES):
    return make_csv(get_as_header_and_records(ticker, max_pages))


def get_as_header_and_records(ticker, max_pages=DEFAULT_MAX_PAGES):
    try:
        number_of_pages = min(get_number_of_pages(ticker), max_pages)
        all_pages = download_n_pages(ticker, number_of_pages)
        all_trades_tables = [extract_trades_table(page) for page in all_pages]
        header = extract_header(all_trades_tables[0])
        trades_tables_records = [extract_records(trades_table) for trades_table in all_trades_tables]
        records = join_records(trades_tables_records)
        return header, records
    except Exception:
        return [], []


def get_number_of_pages(ticker):
    page = download_page(ticker)
    soup = BeautifulSoup(page, 'html.parser')
    last_page_reference = soup.find('a', id='quotes_content_left_lb_LastPage')['href']
    url: ParseResult = urlparse(last_page_reference)
    return int(parse_qs(url.query)['page'][0])


def download_page(ticker, page_number=1):
    url_template = "https://www.nasdaq.com/symbol/%s/insider-trades?page=%d"
    url = url_template % (ticker.lower(), page_number)
    print("Downloading %s" % url)
    return requests.get(url).text


def download_n_pages(ticker, number_of_pages):
    return [
        download_page(ticker, page_number)
        for page_number in inclusive_range(1, number_of_pages)
    ]


def inclusive_range(start, stop):
    return range(start, stop + 1)


def extract_trades_table(page):
    soup = BeautifulSoup(page, 'html.parser')
    content_main = soup.find('div', id='content_main')
    gen_table_div = content_main.find('div', class_='genTable')
    return gen_table_div.find('table', class_='certain-width')


def extract_header(trades_table):
    head_row = trades_table.find('thead').find('tr')
    column_headers = head_row.find_all('th')
    return [column_header.a.contents[0] for column_header in column_headers]


def extract_records(trades_table):
    rows = trades_table.find_all('tr', recursive=False)
    return [[column.string for column in row.find_all('td')] for row in rows]


def join_records(trades_tables_records):
    return list(itertools.chain.from_iterable(trades_tables_records))


def make_csv(header, records):
    output = StringIO()
    csv_writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    csv_writer.writerow(header)
    for record in records:
        csv_writer.writerow(record)
    return output.getvalue()
