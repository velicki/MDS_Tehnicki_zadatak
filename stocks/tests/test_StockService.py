import pytest
from django.urls import reverse
from rest_framework import status
from ..models import StockDB
from .test_CompanyService import api_client, test_create_company_fixture
from unittest.mock import patch
from decimal import Decimal

@pytest.fixture
def test_create_stock_fixture(test_create_company_fixture):
    stock_data = {
        "company": test_create_company_fixture,
        "date": "2020-08-18",
        "open": Decimal("260.950012"),
        "high": Decimal("265.149994"),
        "low": Decimal("259.260010"),
        "close": Decimal("262.339996"),
        "adj_close": Decimal("262.339996"),
        "volume": 18677500
    }
    stock = StockDB.objects.create(**stock_data)
    return stock

@pytest.mark.django_db
def test_create_stock(api_client, test_create_company_fixture):
    url = reverse('stock', args=[test_create_company_fixture.ticker_symbol])

    data = {
        "date": "2020-08-18",
        "open": Decimal("260.950012"),
        "high": Decimal("265.149994"),
        "low": Decimal("259.260010"),
        "close": Decimal("262.339996"),
        "adj_close": Decimal("262.339996"),
        "volume": 18677500
    }

    with patch.object(StockDB, "save", return_value=None) as mock_save:
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        mock_save.assert_called_once()

@pytest.mark.django_db
def test_list_of_all_stocks_of_given_company(api_client, test_create_company_fixture):
    url = reverse('stock', args=[test_create_company_fixture.ticker_symbol])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_one_stock(api_client, test_create_company_fixture, test_create_stock_fixture):
    url = reverse('one_stock', args=[test_create_company_fixture.ticker_symbol, test_create_stock_fixture.date])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_one_stock(api_client, test_create_company_fixture, test_create_stock_fixture):
    url = reverse('one_stock', args=[test_create_company_fixture.ticker_symbol, test_create_stock_fixture.date])

    data = {
        "date": "2020-08-18",
        "open": Decimal("260.950012"),
        "high": Decimal("265.149994"),
        "low": Decimal("259.260010"),
        "close": Decimal("262.339996"),
        "adj_close": Decimal("262.339996"),
        "volume": 18677555
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_one_stock(api_client, test_create_company_fixture, test_create_stock_fixture):
    url = reverse('one_stock', args=[test_create_company_fixture.ticker_symbol, test_create_stock_fixture.date])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT