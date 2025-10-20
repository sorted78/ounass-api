# Python Version Compatibility Guide

## Issue: Pandas Installation Error with Python 3.13

If you see an error like:
```
error: too few arguments to function call, expected 6, have 5
```

This is a known compatibility issue between pandas 2.1.3 and Python 3.13.

## Solutions

### ✅ RECOMMENDED: Use Python 3.11 or 3.12

Python 3.13 is very new and many scientific packages haven't caught up yet.

#### Install Python 3.12 with Homebrew:

```bash
# Install Python 3.12
brew install python@3.12

# Create virtual environment with Python 3.12
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies (use the stable version)
pip install -r requirements-py39-py312.txt
```

### Alternative 1: Use Python 3.13 with Latest Packages

If you must use Python 3.13, use the main requirements.txt which has flexible versions:

```bash
# Make sure you're using Python 3.13
python3.13 -m venv venv
source venv/bin/activate

# Install with latest compatible versions
pip install -r requirements.txt
```

### Alternative 2: Use pyenv to Manage Python Versions

```bash
# Install pyenv
brew install pyenv

# Install Python 3.12
pyenv install 3.12.0

# Set local Python version
cd /Users/root1/Desktop/Projects/ounass-api
pyenv local 3.12.0

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-py39-py312.txt
```

## Which Requirements File to Use?

### requirements.txt (Main)
- For Python 3.13 or when you want the latest versions
- Uses flexible version constraints (>=)
- May have breaking changes

### requirements-py39-py312.txt (Recommended)
- For Python 3.9, 3.10, 3.11, or 3.12
- Uses pinned versions
- Stable and tested
- **RECOMMENDED for production**

## Verification

After installation, verify everything works:

```bash
# Check Python version
python --version

# Check pandas installation
python -c "import pandas; print(f'Pandas {pandas.__version__} OK')"

# Check numpy installation
python -c "import numpy; print(f'NumPy {numpy.__version__} OK')"

# Check scikit-learn installation
python -c "import sklearn; print(f'scikit-learn {sklearn.__version__} OK')"

# Check all imports
python -c "from src.models.forecasting import PodForecastingModel; print('All imports OK')"
```

## Docker Alternative

If you continue having issues, use Docker which has a controlled environment:

```bash
# Build Docker image (uses Python 3.9 internally)
docker build -t ounass-api .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/.env:/app/.env \
  ounass-api
```

## Current Python Versions on Your System

Check what you have:

```bash
# Check Python 3.13
python3.13 --version

# Check Python 3.12
python3.12 --version || echo "Python 3.12 not installed"

# Check Python 3.11
python3.11 --version || echo "Python 3.11 not installed"

# Check default Python 3
python3 --version
```

## Recommended Setup for This Project

```bash
# 1. Install Python 3.12
brew install python@3.12

# 2. Navigate to project
cd /Users/root1/Desktop/Projects/ounass-api

# 3. Create virtual environment with Python 3.12
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install stable dependencies
pip install -r requirements-py39-py312.txt

# 7. Verify installation
python -c "import pandas, numpy, sklearn, fastapi; print('All packages installed successfully!')"

# 8. Run the application
uvicorn src.main:app --reload
```

## Still Having Issues?

### Option 1: Use Conda Instead of pip

```bash
# Install miniconda
brew install --cask miniconda

# Create conda environment
conda create -n ounass python=3.12
conda activate ounass

# Install from conda-forge
conda install -c conda-forge pandas numpy scikit-learn fastapi uvicorn

# Install remaining via pip
pip install gspread google-auth google-auth-oauthlib google-api-python-client pydantic-settings loguru pytest
```

### Option 2: Use a Different Machine

If you're on a Mac with Apple Silicon and having persistent issues, try:
1. Using Docker (recommended)
2. Using a Linux VM
3. Using a cloud development environment

## Summary

**Best approach for immediate success:**

1. Install Python 3.12: `brew install python@3.12`
2. Use it for venv: `/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv`
3. Use stable requirements: `pip install -r requirements-py39-py312.txt`

This will avoid all Python 3.13 compatibility issues!
