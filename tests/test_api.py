"""
API Tests
"""
import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from models.forecasting import PodForecastingModel
from services.sheets_service import GoogleSheetsService

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_trained" in data
    assert "timestamp" in data


def test_forecasting_model():
    """Test forecasting model training and prediction"""
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    historical_data = pd.DataFrame({
        'Date': dates,
        'GMV': [1000000 + i * 5000 for i in range(len(dates))],
        'Users': [15000 + i * 100 for i in range(len(dates))],
        'Marketing_Cost': [40000 + i * 200 for i in range(len(dates))],
        'Frontend_Pods': [8 + (i % 10) for i in range(len(dates))],
        'Backend_Pods': [5 + (i % 5) for i in range(len(dates))]
    })
    
    # Initialize and train model
    model = PodForecastingModel()
    metrics = model.train(historical_data)
    
    # Check that model is trained
    assert model.is_trained
    assert 'frontend_mae' in metrics
    assert 'backend_mae' in metrics
    assert 'frontend_r2' in metrics
    assert 'backend_r2' in metrics
    
    # Create budget data for prediction
    future_dates = pd.date_range(start='2024-07-01', end='2024-07-10', freq='D')
    budget_data = pd.DataFrame({
        'Date': future_dates,
        'GMV': [1500000 + i * 10000 for i in range(len(future_dates))],
        'Users': [20000 + i * 200 for i in range(len(future_dates))],
        'Marketing_Cost': [50000 + i * 500 for i in range(len(future_dates))]
    })
    
    # Make predictions
    predictions = model.predict(budget_data)
    
    # Verify predictions
    assert len(predictions) == len(budget_data)
    assert 'Frontend_Pods' in predictions.columns
    assert 'Backend_Pods' in predictions.columns
    assert 'Total_Pods' in predictions.columns
    assert all(predictions['Frontend_Pods'] >= 1)
    assert all(predictions['Backend_Pods'] >= 1)


def test_model_feature_engineering():
    """Test feature engineering"""
    model = PodForecastingModel()
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'GMV': [1000000] * len(dates),
        'Users': [15000] * len(dates),
        'Marketing_Cost': [40000] * len(dates)
    })
    
    # Engineer features
    engineered = model._engineer_features(data)
    
    # Check that new features were created
    assert 'DayOfWeek' in engineered.columns
    assert 'DayOfMonth' in engineered.columns
    assert 'Month' in engineered.columns
    assert 'GMV_per_User' in engineered.columns
    assert 'Marketing_per_User' in engineered.columns
    assert 'ROAS' in engineered.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
