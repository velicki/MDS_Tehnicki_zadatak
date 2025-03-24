from rest_framework import serializers
from stocks.models import *

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


    class Meta:
        model = CompanyDB
        fields = ['id', 'name', 'ticker_symbol', 'founded_at', 'additional_info']
        extra_kwargs = {
            'founded_at': {'required': False},
            'additional_info': {'required': False},
        }


class StockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company_ticker_symbol = serializers.SerializerMethodField()


    class Meta:
        model = StockDB
        fields = ['id', 'company', 'company_ticker_symbol', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        extra_kwargs = {
            'open': {'required': False},
            'high': {'required': False},
            'low': {'required': False},
            'close': {'required': False},
            'adj_close': {'required': False},
            'volume': {'required': False},
        }

    def get_company_ticker_symbol(self, obj):
        return obj.company.ticker_symbol