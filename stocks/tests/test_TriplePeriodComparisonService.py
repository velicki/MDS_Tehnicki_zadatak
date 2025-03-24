import pytest
from django.urls import reverse
from rest_framework import status
from ..models import StockDB
from .test_CompanyService import api_client, test_create_company_fixture
from .test_StockService import test_create_stock_fixture


@pytest.mark.django_db
def test_get_triple_period_comparison(api_client, test_create_company_fixture, test_create_stock_fixture):
    url = reverse('triple_period_comparison', args=[test_create_company_fixture.ticker_symbol, 8, 18, 2020, 8, 18, 2020])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK