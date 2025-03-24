# Stock Market Analysis API

## Overview
Stock Market Analysis API is a web application built using Python-Django, designed to facilitate stock market data management and analysis. The application provides full CRUD operations for companies and stock market data, along with an endpoint for stock trading analysis.

## Technologies Used
- **Backend**: Python-Django
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Testing**: PyTest
- **Containerization**: Docker
- **API Documentation**: Swagger
- **Architecture**: Dependency Injection
- **Data Access**: Repository Pattern

## Features
### Company Management
Users can create, retrieve, update, and delete company records. Each company has the following attributes:
- `name`
- `ticker_symbol`
- `founded_at`
- `additional_info`

### Stock Market Data Management
For each company, stock market data can be recorded with the following fields:
- `date`
- `open`
- `high`
- `low`
- `close`
- `adj_close`
- `volume`

Stock market data can be added in two ways:
1. **Manual Entry**: Entering data one by one.
2. **CSV Upload**: Uploading a `.csv` file with multiple records, which will be processed and stored in the database.

If a company is deleted, all associated stock market data will also be removed.

### Stock Trading Analysis
A dedicated endpoint is available for analyzing stock trading opportunities. The endpoint allows users to send a request with:
- **Stock Ticker Symbol** (e.g., `AAPL` for Apple Inc.)
- **Start Date** (e.g., `2020-06-01`)
- **End Date** (e.g., `2020-06-10`)

The response provides information for three periods:
1. The requested period (`2020-06-01` to `2020-06-10`)
2. The preceding period with the same duration (`2020-05-20` to `2020-05-29`)
3. The following period with the same duration (`2020-06-11` to `2020-06-20`)

For each period, the following details are returned:
- **Best Buy Date**: The most profitable day to buy stocks and its closing price.
- **Best Sell Date**: The most profitable day to sell stocks and its closing price.
- **Profit**: The profit calculated as the difference between the closing price on the buy and sell dates.
- **Max Possible Profit**: The maximum possible profit if the stock was bought and sold multiple times in the period, assuming every profitable trade was made.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/velicki/MDS_Tehnicki_zadatak.git
   cd MDS_Tehnicki_zadatak
   ```
2. Build and run the application using Docker:
   ```bash
   docker-compose up --build
   ```
3. Access the API documentation via Swagger:
   ```
   http://localhost:8000/swagger/
   ```

## Testing
To run tests, Docker containers must be running.
Inside the Django container, in its terminal, enter:
```bash
pytest
```

## API Endpoints

### Company Endpoints
- `http://127.0.0.1:8000/api/company`
  - **GET**: Returns a list of all companies.
  - **POST**: Inserts a new company into the database.
    ```json
    {
        "name": "Apple.inc",
        "ticker_symbol": "APPL",
        "founded_at": "2006-08-09",
        "additional_info": "iPhone"
    }
    ```
- `http://127.0.0.1:8000/api/one_company/<str:ticker_symbol>`
  - **GET**: Retrieve information about a single company.
  - **PUT**: Update company information.
  - **DELETE**: Delete a company (removes all associated stock data as well).

### Stock Endpoints
- `http://127.0.0.1:8000/api/stock/<str:ticker_symbol>`
  - **GET**: Returns all stock data for a specific company.
  - **POST**: Enter stock data via `.csv` file or JSON:
    ```json
    {
        "date": "2020-08-18",
        "open": "260.950012",
        "high": "265.149994",
        "low": "259.260010",
        "close": "262.339996",
        "adj_close": "262.339996",
        "volume": 18677500
    }
    ```
- `http://127.0.0.1:8000/api/one_stock/<str:ticker_symbol>/<str:date>`
  - **GET**: Retrieve data for a specific stock.
  - **PUT**: Update stock data.
  - **DELETE**: Delete a specific stock from the database.

### Stock Trading Analysis Endpoint
- `http://127.0.0.1:8000/api/triple_period_comparison/<str:ticker_symbol>/start-date/<str:mm1>/<str:dd1>/<int:yyyy1>/end-date/<str:mm2>/<str:dd2>/<int:yyyy2>`
  - **GET**: Trading analysis for a given period. Example URL:
    ```
    http://127.0.0.1:8000/api/triple_period_comparison/META/start-date/08/01/2012/end-date/08/10/2012
    ```
