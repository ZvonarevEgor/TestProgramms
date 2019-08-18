import os
import csv
import pandas as pd


class CalculatePerformance:
    CURRENCIES = os.path.abspath('currencies.csv')
    EXCHANGES = os.path.abspath('exchanges.csv')
    PRICES = os.path.abspath('prices.csv')
    WEIGHTS = os.path.abspath('weights.csv')

    def __init__(self, name_of_asset):
        self.name = name_of_asset
        self.price_index = self.get_price_index
        self.exchange_index = 1

    def get_price_index(self):
        reader = csv.DictReader(self.PRICES, delimiter=',')
        i = 0
        for line in reader:
            for asset in line:
                if asset == self.name:
                    price_index = i
                    return price_index
                i += 1

    def calculate_asset_performance(self, start_date, end_date):
        start_price = self.get_price(start_date)
        end_price = self.get_price(end_date)
        result = (int(end_price) - int(start_price))/int(start_price)
        return pd.Series(result)

    def calculate_currency_performance(self, start_date, end_date):
        start_exchange = self.get_exchange(start_date)
        end_exchange = self.get_exchange(end_date)
        result = (int(end_exchange) - int(start_exchange)) / int(start_exchange)
        return pd.Series(result)

    def calculate_total_performance(self, start_date, end_date):
        start_price = self.get_price(start_date)
        end_price = self.get_price(end_date)
        start_exchange = self.get_exchange(start_date)
        end_exchange = self.get_exchange(end_date)
        top_expression = (int(end_price) * int(end_exchange)) - (int(start_price) * int(start_exchange))
        result = top_expression / (int(start_exchange) * int(start_price))
        return pd.Series(result)

    def get_price(self, date):
        reader = csv.DictReader(self.PRICES, delimiter=',')
        for line in reader[1:]:
            if line[0] == date:
                return line[self.price_index]

    def get_exchange(self, date):
        reader = csv.DictReader(self.EXCHANGES, delimiter=',')
        for line in reader[1:]:
            if line[0] == date:
                return line[self.exchange_index]
