from ..models import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from .Singleton_config import SingletonMeta
from ..repositories.company_repository import CompanyRepository


class CompanyService(metaclass = SingletonMeta):

    def __init__(self, company_repository=None):

        self.company_repository = company_repository or CompanyRepository()


# Create new Company
#_________________________________________________________
    def create_company(self, request):
        
        # Check if a company with that name already exists
        if self.company_repository.company_name_exists(name=request.data['name']):
            return Response({'error': 'You alredy created Company with that name.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a company with that ticker symbol already exists
        if self.company_repository.company_ticker_symbol_exists(ticker_symbol=request.data['ticker_symbol']):
            return Response({'error': 'You alredy created Company with that ticker symbol.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create serializer for incoming data
        serializer = CompanySerializer(data=request.data)
        
        # Check if the data in the serializer is valid
        if serializer.is_valid():
            # Create new company in the database
            company = self.company_repository.create_new_company(serializer.validated_data)

            # Prepare data for JSON Response
            custom_response_data = {
                'company_id': company.id,
                'name': company.name,
                'ticker_symbol': company.ticker_symbol,
                'founded_at': company.founded_at,
                'additional_info': company.additional_info
            }

            return Response(custom_response_data, status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list_of_all_companies
#_________________________________________________________
    def list_of_all_companies(self):

        companies = self.company_repository.get_list_of_all_companies()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# get_one_company
#_________________________________________________________
    def get_one_company(self, ticker_symbol):
        # Check if a company with that ticker symbol does not exists
        if not self.company_repository.company_ticker_symbol_exists(ticker_symbol=ticker_symbol):
            return Response({'error': 'Company with that ticker symbol does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get company by ticker symbol
        company = self.company_repository.get_one_company(ticker_symbol)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# update_one_company
#_________________________________________________________
    def update_one_company(self, request, ticker_symbol):
        # Get company
        company = self.company_repository.get_one_company(ticker_symbol)
        
        if not company:
            return Response({'error': 'Company with that ticker symbol does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Update company
        updated_company = self.company_repository.update_one_company(company, request.data)

        # Serialize updated company for response
        serializer = CompanySerializer(updated_company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# delete_one_company
#_________________________________________________________
    def delete_one_company(self, ticker_symbol):
        # Get company
        company = self.company_repository.get_one_company(ticker_symbol)
        
        if not company:
            return Response({'error': 'Company with that ticker symbol does not exist.'}, status=status.HTTP_404_NOT_FOUND)
         
        self.company_repository.delete_one_company(company)
        return Response(status=status.HTTP_204_NO_CONTENT)