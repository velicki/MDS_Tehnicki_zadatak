from rest_framework.decorators import api_view
from .services import CompanyService, StockService, TriplePeriodComparisonService


company_service = CompanyService()
stock_service = StockService()
triple_period_comparison_service = TriplePeriodComparisonService()


# ********** company_service **********
# _____________________________________________________________________________________________
# Create new Company or List all companies
#_________________________________________________________

@api_view(['POST', 'GET'])
def company(request):

    if request.method == 'POST':   # Create new Company
        return company_service.create_company(request)
    elif request.method == 'GET':  # Get list of all companies
        return company_service.list_of_all_companies()


# GET, Update or Delete one Company
#_________________________________________________________

@api_view(['GET', 'PUT', 'DELETE'])
def one_company(request, ticker_symbol):

    if request.method == 'GET':       # GET one Company
        return company_service.get_one_company(ticker_symbol)
    elif request.method == 'PUT':     # Update one company
        return company_service.update_one_company(request, ticker_symbol)
    elif request.method == 'DELETE':  # Delete one company
        return company_service.delete_one_company(ticker_symbol)
    

# ********** stock_service **********
# _____________________________________________________________________________________________
# Create new Stock for one Company or List all Stocks of one Company
#_________________________________________________________

@api_view(['POST', 'GET'])
def stock(request, ticker_symbol):

    if request.method == 'POST':   # Create new stock manualy or upload CSV file
        return stock_service.create_stock(request, ticker_symbol)
    elif request.method == 'GET':  # Get list of all stocks of one Company
        return stock_service.list_of_all_stocks_of_given_company(request, ticker_symbol)


# GET, Update or Delete one stock
#_________________________________________________________

@api_view(['GET', 'PUT', 'DELETE'])
def one_stock(request, ticker_symbol, date):

    if request.method == 'GET':       # GET one stock
        return stock_service.get_one_stock(ticker_symbol, date)
    elif request.method == 'PUT':     # Update one stock
        return stock_service.update_one_stock(request, ticker_symbol, date)
    elif request.method == 'DELETE':  # Delete one stock
        return stock_service.delete_one_stock(ticker_symbol, date)
    

# ********** triple_period_comparison_service **********
# _____________________________________________________________________________________________
# GET triple_period_comparison_service for one Company
#_________________________________________________________

@api_view(['GET'])
def triple_period_comparison(request, ticker_symbol, mm1, dd1, yyyy1, mm2, dd2, yyyy2):

    return triple_period_comparison_service.get_triple_period_comparison(ticker_symbol, mm1, dd1, yyyy1, mm2, dd2, yyyy2)