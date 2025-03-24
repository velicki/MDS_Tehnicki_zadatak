from django.db import models
from django.core.validators import MinValueValidator

class CompanyDB(models.Model):
    name = models.CharField(max_length=200, unique=True)  # company name must be unique
    ticker_symbol = models.CharField(max_length=50, unique=True)  # ticker symbol must be unique
    founded_at = models.DateField()
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.ticker_symbol})"
    
class StockDB(models.Model):
    company = models.ForeignKey(CompanyDB, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0.0)], null=True, blank=True)
    high = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0.0)], null=True, blank=True)
    low = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0.0)], null=True, blank=True)
    close = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0.0)], null=True, blank=True)
    adj_close = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0.0)], null=True, blank=True)
    volume = models.BigIntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'date'], name='unique_company_date')
        ]

    def __str__(self):
        return f"{self.company.ticker_symbol} ({self.date})"