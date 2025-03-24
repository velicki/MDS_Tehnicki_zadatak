from ..models import CompanyDB

class CompanyRepository:

    def create_new_company(self, data):
        return CompanyDB.objects.create(
            name = data['name'], 
            ticker_symbol = data['ticker_symbol'],
            founded_at = data.get('founded_at'),
            additional_info = data.get('additional_info')
        )
    
    def get_list_of_all_companies(self):
        return CompanyDB.objects.all()
    
    def get_one_company(self, ticker_symbol):
        return CompanyDB.objects.filter(ticker_symbol=ticker_symbol).first()
    
    def update_one_company(self, company, updated_data):
        for field, value in updated_data.items():
            if hasattr(company, field):
                setattr(company, field, value)
        company.save()
        return company
    
    def delete_one_company(self, company):
        return company.delete()

    def company_name_exists(self, name):
        return CompanyDB.objects.filter(name=name).exists()
    
    def company_ticker_symbol_exists(self, ticker_symbol):
        return CompanyDB.objects.filter(ticker_symbol=ticker_symbol).exists()