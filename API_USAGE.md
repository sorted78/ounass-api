# API Usage Guide

Complete guide for using the OUNASS Kubernetes Pod Forecasting API.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. For production deployment, implement API key authentication.

## Endpoints

### 1. Root Endpoint
Get API information.

**Request:**
```bash
GET /
```

**Response:**
```json
{
  "message": "OUNASS Kubernetes Pod Forecasting API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

---

### 2. Health Check
Check API and model status.

**Request:**
```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_trained": true,
  "timestamp": "2024-07-15T10:30:00"
}
```

---

### 3. Train Model
Train the forecasting model with latest historical data.

**Request:**
```bash
POST /api/v1/train
```

**Response:**
```json
{
  "frontend_mae": 0.82,
  "frontend_rmse": 1.05,
  "frontend_r2": 0.94,
  "backend_mae": 0.65,
  "backend_rmse": 0.88,
  "backend_r2": 0.92
}
```

**Notes:**
- Train the model before making predictions
- Should be retrained periodically as new historical data becomes available
- Training requires at least 10 historical records

---

### 4. Get Daily Forecast
Get pod prediction for a specific date or tomorrow by default.

**Request:**
```bash
GET /api/v1/forecast/daily?target_date=2024-07-15
```

**Parameters:**
- `target_date` (optional): Date in YYYY-MM-DD format. Defaults to tomorrow.

**Response:**
```json
{
  "date": "2024-07-15",
  "frontend_pods": 18,
  "backend_pods": 12,
  "total_pods": 30,
  "confidence_score": 0.92,
  "metrics": {
    "gmv": 2000000,
    "users": 30000,
    "marketing_cost": 70000
  }
}
```

**Example with curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/forecast/daily?target_date=2024-07-15"
```

---

### 5. Get Forecast Range
Get pod predictions for a date range.

**Request:**
```bash
GET /api/v1/forecast/range?start_date=2024-07-01&end_date=2024-07-31
```

**Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format. Defaults to tomorrow.
- `end_date` (optional): End date in YYYY-MM-DD format.
- `days` (optional): Number of days to forecast. Alternative to end_date.

**Response:**
```json
{
  "start_date": "2024-07-01",
  "end_date": "2024-07-31",
  "predictions": [
    {
      "date": "2024-07-01",
      "frontend_pods": 18,
      "backend_pods": 12,
      "total_pods": 30,
      "confidence_score": 0.92,
      "metrics": {
        "gmv": 1900000,
        "users": 28500,
        "marketing_cost": 67500
      }
    },
    {
      "date": "2024-07-02",
      "frontend_pods": 19,
      "backend_pods": 12,
      "total_pods": 31,
      "confidence_score": 0.91,
      "metrics": {
        "gmv": 1950000,
        "users": 29200,
        "marketing_cost": 69000
      }
    }
  ],
  "summary": {
    "avg_frontend_pods": 18.5,
    "avg_backend_pods": 12.2,
    "avg_total_pods": 30.7,
    "max_total_pods": 35,
    "min_total_pods": 28,
    "total_days": 31
  }
}
```

**Example with curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/forecast/range?start_date=2024-07-01&days=30"
```

---

### 6. Get Model Metrics
Get current model performance metrics.

**Request:**
```bash
GET /api/v1/metrics
```

**Response:**
```json
{
  "frontend_mae": 0.82,
  "frontend_rmse": 1.05,
  "frontend_r2": 0.94,
  "backend_mae": 0.65,
  "backend_rmse": 0.88,
  "backend_r2": 0.92
}
```

---

## Interactive API Documentation

FastAPI provides interactive API documentation:

1. **Swagger UI**: http://localhost:8000/docs
   - Try out API endpoints directly in your browser
   - See request/response schemas
   - Test with different parameters

2. **ReDoc**: http://localhost:8000/redoc
   - Alternative documentation interface
   - Better for reading and understanding the API

---

## Usage Workflow

### First Time Setup

1. **Start the API:**
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Check health:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

3. **Train the model:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/train
   ```

4. **Get a prediction:**
   ```bash
   curl http://localhost:8000/api/v1/forecast/daily
   ```

### Daily Operations

For DevOps team to get daily pod requirements:

```bash
# Get tomorrow's pod requirements
curl http://localhost:8000/api/v1/forecast/daily

# Get next week's pod requirements
curl "http://localhost:8000/api/v1/forecast/range?days=7"

# Get specific date
curl "http://localhost:8000/api/v1/forecast/daily?target_date=2024-07-20"
```

### Periodic Model Updates

Retrain the model weekly or when new historical data is available:

```bash
curl -X POST http://localhost:8000/api/v1/train
```

---

## Python Client Example

```python
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

class PodForecastClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def health_check(self):
        response = requests.get(f"{self.base_url}/api/v1/health")
        return response.json()
    
    def train_model(self):
        response = requests.post(f"{self.base_url}/api/v1/train")
        return response.json()
    
    def get_daily_forecast(self, target_date=None):
        params = {}
        if target_date:
            params['target_date'] = target_date.isoformat()
        response = requests.get(
            f"{self.base_url}/api/v1/forecast/daily",
            params=params
        )
        return response.json()
    
    def get_forecast_range(self, start_date=None, end_date=None, days=None):
        params = {}
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if days:
            params['days'] = days
        response = requests.get(
            f"{self.base_url}/api/v1/forecast/range",
            params=params
        )
        return response.json()

# Usage
client = PodForecastClient()

# Check health
health = client.health_check()
print(f"API Status: {health['status']}")

# Train model if needed
if not health['model_trained']:
    metrics = client.train_model()
    print(f"Model trained. Frontend R²: {metrics['frontend_r2']:.2f}")

# Get tomorrow's forecast
tomorrow = date.today() + timedelta(days=1)
forecast = client.get_daily_forecast(tomorrow)
print(f"Forecast for {forecast['date']}:")
print(f"  Frontend pods: {forecast['frontend_pods']}")
print(f"  Backend pods: {forecast['backend_pods']}")

# Get next 7 days
range_forecast = client.get_forecast_range(days=7)
print(f"\nNext 7 days average: {range_forecast['summary']['avg_total_pods']:.1f} pods")
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Model not trained. Please call /api/v1/train first."
}
```

### 404 Not Found
```json
{
  "detail": "No budget data found for date 2024-07-15"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Prediction failed: [error message]"
}
```

---

## Response Field Descriptions

### PodPrediction Fields

- **date**: Target date for the prediction
- **frontend_pods**: Number of frontend Kubernetes pods required
- **backend_pods**: Number of backend Kubernetes pods required
- **total_pods**: Combined total of frontend and backend pods
- **confidence_score**: Model confidence (0-1, higher is better)
- **metrics.gmv**: Gross Merchandise Value for the date
- **metrics.users**: Expected number of users
- **metrics.marketing_cost**: Marketing spend for the date

### Training Metrics Fields

- **frontend_mae**: Mean Absolute Error for frontend predictions
- **frontend_rmse**: Root Mean Squared Error for frontend predictions
- **frontend_r2**: R² score for frontend predictions (0-1, higher is better)
- **backend_mae**: Mean Absolute Error for backend predictions
- **backend_rmse**: Root Mean Squared Error for backend predictions
- **backend_r2**: R² score for backend predictions (0-1, higher is better)

---

## Best Practices

1. **Initial Training**: Always train the model after starting the API for the first time

2. **Regular Retraining**: Retrain the model:
   - Weekly or bi-weekly
   - When significant new historical data is added
   - After major business changes

3. **Monitoring**: Check model metrics regularly:
   - R² score > 0.85 indicates good performance
   - MAE < 2.0 for pod predictions is acceptable
   - Lower confidence scores may indicate unusual business patterns

4. **Date Validation**: Always validate that budget data exists for requested dates

5. **Error Handling**: Implement proper error handling in your client applications

6. **Caching**: Consider caching predictions for frequently requested dates

7. **Logging**: Monitor API logs for errors and performance issues
