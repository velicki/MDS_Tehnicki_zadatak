from ..models import *
from django.db.models import Min, Max
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .Singleton_config import SingletonMeta
from ..repositories.stock_repository import StockRepository
from ..repositories.company_repository import CompanyRepository


class TriplePeriodComparisonService(metaclass = SingletonMeta):

    def __init__(self, stock_repository=None, company_repository=None):

        self.stock_repository = stock_repository or StockRepository()
        self.company_repository = company_repository or CompanyRepository()


# Get triple period comparison
#_________________________________________________________
    def get_triple_period_comparison(self, ticker_symbol, mm1, dd1, yyyy1, mm2, dd2, yyyy2):
        
        # Check if a company with that ticker symbol already exists and fetch the object
        company = self.company_repository.get_one_company(ticker_symbol)
        if not company:
            return Response({'error': 'The Company with that ticker symbol does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert string to date object
        start_date = datetime.strptime(f"{yyyy1}-{mm1}-{dd1}", "%Y-%m-%d").date()
        end_date = datetime.strptime(f"{yyyy2}-{mm2}-{dd2}", "%Y-%m-%d").date()

        # One period in days
        delta_days = (end_date - start_date).days

        # Define triple period
        previous_start = start_date - timedelta(days=delta_days + 1)
        previous_end = end_date - timedelta(days=delta_days + 1)

        next_start = end_date + timedelta(days=1)
        next_end = next_start + timedelta(days=delta_days)

        # Fetch date for all periods
        periods = {
            "requested": (start_date, end_date),
            "previous": (previous_start, previous_end),
            "next": (next_start, next_end),
        }

        result = {}

        for period_name, (start, end) in periods.items():
            stocks = self.stock_repository.get_stocks_in_range(company_id=company.id, start_date=start, end_date=end)

            if not stocks:
                result[period_name] = {"error": "No stock data available for this period."}
                continue

            # to buy
            best_buy = min(stocks, key=lambda s: s.close)
            best_buy_date, best_buy_price = best_buy.date, best_buy.close

            # To sell
            best_sell = max(stocks, key=lambda s: s.close)
            best_sell_date, best_sell_price = best_sell.date, best_sell.close

            # Profit
            one_trade_profit = best_sell_price - best_buy_price

            # Max profit
            max_possible_profit = TriplePeriodComparisonService.calculate_max_profit([s.close for s in stocks])

            result[period_name] = {
                "buy_date": best_buy_date,
                "buy_price": best_buy_price,
                "sell_date": best_sell_date,
                "sell_price": best_sell_price,
                "one_trade_profit": one_trade_profit,
                "max_possible_profit": max_possible_profit
            }

        return Response(result, status=200)


    def calculate_max_profit(prices):
        total_profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                total_profit += prices[i] - prices[i - 1]
        return total_profit