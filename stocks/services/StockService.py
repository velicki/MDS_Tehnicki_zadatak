import csv
import io
from ..models import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .Singleton_config import SingletonMeta
from ..repositories.stock_repository import StockRepository
from ..repositories.company_repository import CompanyRepository
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class StockService(metaclass = SingletonMeta):

    def __init__(self, stock_repository=None, company_repository=None):

        self.stock_repository = stock_repository or StockRepository()
        self.company_repository = company_repository or CompanyRepository()


# Create new Company
#_________________________________________________________
    def create_stock(self, request, ticker_symbol):
        
        # Check if a company with that ticker symbol already exists and fetch the object
        company = self.company_repository.get_one_company(ticker_symbol)
        if not company:
            return Response({'error': 'The Company with that ticker symbol does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['company'] = company.id

        if 'file' in request.FILES:
            csv_file = request.FILES['file']

            # Check is .csv file
            if not csv_file.name.endswith('.csv'):
                return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Decode file
                decoded_file = csv_file.read().decode('utf-8', errors='ignore')
                reader = csv.DictReader(io.StringIO(decoded_file))

                # loop through each row
                stocks_to_create = []
                for row in reader:
                    try:
                        stocks_to_create.append(StockDB(
                            company=company, 
                            date=datetime.strptime(row['Date'], "%Y-%m-%d"),
                            open=float(row['Open']),
                            high=float(row['High']),
                            low=float(row['Low']),
                            close=float(row['Close']),
                            adj_close=float(row['Adj Close']),
                            volume=int(row['Volume'])
                        ))
                    except (ValueError, KeyError) as e:
                        return Response({'error': f'Invalid data format in CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

                self.stock_repository.bulk_create_new_stock(stocks_to_create)

                return Response({'message': f'Successfully added {len(stocks_to_create)} stock records.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a stock with that date and ticker symbol already exists
        if self.stock_repository.stock_date_and_ticker_symbol_exists(date=request.data.get('date'), ticker_symbol=ticker_symbol):
            return Response({'error': 'You alredy have that date for the given ticker symbol.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create serializer for incoming data
        serializer = StockSerializer(data=request.data)
        
        # Check if the data in the serializer is valid
        if serializer.is_valid():
            # Create new company in the database
            stock = self.stock_repository.create_new_stock(serializer.validated_data)

            # Prepare data for JSON Response
            custom_response_data = {
                'stock_id': stock.id,
                'company name': stock.company.name,
                'ticker symbol': stock.company.ticker_symbol,
                'date': stock.date,
                'open': stock.open,
                'high': stock.high,
                'low': stock.low,
                'close': stock.close,
                'adj_close': stock.adj_close,
                'volume': stock.volume
            }

            return Response(custom_response_data, status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list_of_all_stocks_of_given_company
#_________________________________________________________
    def list_of_all_stocks_of_given_company(self, request, ticker_symbol):

        # Check if a company with that ticker symbol already exists and fetch the object
        company = self.company_repository.get_one_company(ticker_symbol)
        if not company:
            return Response({'error': 'The Company with that ticker symbol does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch all stock records for that company
        stocks = self.stock_repository.get_list_of_all_stocks_of_given_company(company)

        if not stocks.exists():
            return Response([], status=status.HTTP_200_OK)
        
        # Pagination
        paginator = CustomPagination()
        paginated_stocks = paginator.paginate_queryset(stocks, request)
        serializer = StockSerializer(paginated_stocks, many=True)

        return paginator.get_paginated_response(serializer.data)
    
# get_one_stock
#_________________________________________________________
    def get_one_stock(self, ticker_symbol, date):

        # Check if a company with that ticker symbol already exists and fetch the object
        company = self.company_repository.get_one_company(ticker_symbol)
        if not company:
            return Response({'error': 'The Company with that ticker symbol does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get one stock by company id and date
        stock = self.stock_repository.get_one_stock(company=company.id, date=date)

        if not stock:
            return Response({'error': 'Stock data not found for the given date and ticker symbol.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# update_one_stock
#_________________________________________________________
    def update_one_stock(self, request, ticker_symbol, date):

        # Check if a company with that ticker symbol already exists and fetch the object
        company = self.company_repository.get_one_company(ticker_symbol)
        if not company:
            return Response({'error': 'The Company with that ticker symbol does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get one stock by company id and date
        stock = self.stock_repository.get_one_stock(company=company.id, date=date)

        if not stock:
            return Response({'error': 'Stock data not found for the given date and ticker symbol.'}, status=status.HTTP_404_NOT_FOUND)

        # Validate data
        serializer = StockSerializer(stock, data=request.data, partial=True)  # `partial=True` dozvoljava ažuriranje samo nekih polja
        if serializer.is_valid():
            self.stock_repository.update_one_stock(stock, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# delete_one_stock
#_________________________________________________________
    def delete_one_stock(self, ticker_symbol, date):

        # Check if a company with that ticker symbol already exists and fetch the object
        company = self.company_repository.get_one_company(ticker_symbol)
        if not company:
            return Response({'error': 'The Company with that ticker symbol does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get one stock by company id and date
        stock = self.stock_repository.get_one_stock(company=company.id, date=date)
        if not stock:
            return Response({'error': 'Stock data not found for the given date and ticker symbol.'}, status=status.HTTP_404_NOT_FOUND)
         
        self.stock_repository.delete_one_stock(stock)
        return Response(status=status.HTTP_204_NO_CONTENT)