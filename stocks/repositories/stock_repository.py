from ..models import StockDB

class StockRepository:

    def create_new_stock(self, data):
        return StockDB.objects.create(
            company = data['company'],
            date = data['date'],
            open = data.get('open'),
            high=data.get('high'),
            low=data.get('low'),
            close=data.get('close'),
            adj_close=data.get('adj_close'),
            volume=data.get('volume'),
        )
    
    def bulk_create_new_stock(self, stocks_to_create):
        return StockDB.objects.bulk_create(stocks_to_create)
    
    def get_list_of_all_stocks_of_given_company(self, company):
        return StockDB.objects.filter(company=company).order_by('-date')
    
    def get_one_stock(self, company, date):
        return StockDB.objects.filter(company=company, date=date).first()
    
    def update_one_stock(self, stock, updated_data):
        for field, value in updated_data.items():
            if hasattr(stock, field):
                setattr(stock, field, value)
        stock.save()
        return stock
    
    def delete_one_stock(self, stock):
        return stock.delete()

    def stock_date_and_ticker_symbol_exists(self, date, ticker_symbol):
        return StockDB.objects.filter(date=date, company__ticker_symbol=ticker_symbol).exists()
    
    def get_stocks_in_range(self, company_id, start_date, end_date):
        return StockDB.objects.filter(company=company_id, date__range=(start_date, end_date)).order_by('date')