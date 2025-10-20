# OUNASS Kubernetes Pod Forecasting API

## Overview
This API forecasts the required number of Kubernetes pods (front-end and back-end) based on business metrics including GMV (Gross Merchandise Value), user counts, and marketing costs.

## Features
- Fetches historical and budgeted data from Google Sheets
- Machine learning model for pod requirement forecasting
- RESTful API endpoint for daily pod predictions
- Automated data pipeline for continuous forecasting

## Tech Stack
- **Backend**: Python 3.9+ with FastAPI
- **ML Framework**: scikit-learn
- **Data Source**: Google Sheets API
- **Deployment**: Docker-ready

## Project Structure
```
ounass-api/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── forecasting.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── sheets_service.py
│   └── main.py
├── data/
│   └── sample_data.csv
├── tests/
│   └── test_api.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sorted78/ounass-api.git
cd ounass-api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Google Sheets API
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create service account credentials
4. Download credentials JSON file and save as `credentials.json`
5. Share your Google Sheet with the service account email

### 4. Environment Variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Required environment variables:
- `GOOGLE_SHEET_ID`: Your Google Sheet ID
- `GOOGLE_CREDENTIALS_PATH`: Path to credentials.json

### 5. Run the API
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /health
Health check endpoint

### GET /api/v1/forecast/daily
Get daily pod predictions

**Response:**
```json
{
  "date": "2024-07-15",
  "frontend_pods": 12,
  "backend_pods": 8,
  "confidence_score": 0.92,
  "metrics": {
    "predicted_gmv": 1500000,
    "predicted_users": 25000,
    "predicted_marketing_cost": 50000
  }
}
```

### GET /api/v1/forecast/range?start_date=2024-07-01&end_date=2024-07-31
Get pod predictions for a date range

## Model Details
The forecasting model uses multiple regression algorithms:
- Feature engineering from GMV, users, and marketing costs
- Historical pod usage patterns from June
- Budget projections for future dates

## Development

### Running Tests
```bash
pytest tests/
```

### Docker Build
```bash
docker build -t ounass-api .
docker run -p 8000:8000 ounass-api
```

## Data Format
The Google Sheet should have the following columns:
- Date
- GMV (Gross Merchandise Value)
- Users (Number of users)
- Marketing Cost
- Frontend Pods (historical data only)
- Backend Pods (historical data only)

## Contributing
1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License
MIT License
