import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from ..models import CompanyDB
from unittest.mock import patch

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_create_company_fixture():
    company_data = {
        "name": "Apple.inc",
        "ticker_symbol": "APPL",
        "founded_at": "2006-08-09",
        "additional_info": "IPhone"
    }
    company = CompanyDB.objects.create(**company_data)
    return company

@pytest.mark.django_db
def test_create_company(api_client):
    url = reverse('company')

    data = {
        "name": "Apple.inc",
        "ticker_symbol": "APPL",
        "founded_at": "2006-08-09",
        "additional_info": "IPhone"
    }

    with patch.object(CompanyDB, "save", return_value=None) as mock_save:
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        mock_save.assert_called_once()

@pytest.mark.django_db
def test_list_of_all_companies(api_client):
    url = reverse('company')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_one_company(api_client, test_create_company_fixture):
    url = reverse('one_company', args=[test_create_company_fixture.ticker_symbol])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_one_company(api_client, test_create_company_fixture):
    url = reverse('one_company', args=[test_create_company_fixture.ticker_symbol])

    data = {
        "name": "Apple.inc",
        "ticker_symbol": "APPL",
        "founded_at": "2006-08-09",
        "additional_info": "IPhone 16"
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_one_company(api_client, test_create_company_fixture):
    url = reverse('one_company', args=[test_create_company_fixture.ticker_symbol])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT