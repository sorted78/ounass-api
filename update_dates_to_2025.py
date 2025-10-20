#!/usr/bin/env python3
"""
Update sheet dates to 2025 (current year)
This shifts all dates forward by 1 year
"""
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

load_dotenv()

SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
CREDS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

print("Updating Sheet Dates to 2025...")
print("-" * 80)

# Connect
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
client = gspread.authorize(credentials)

# Open spreadsheet
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet("Sheet1")

# Get all records
records = worksheet.get_all_records()
print(f"Found {len(records)} rows")

# Parse dates and shift to 2025
print("\nUpdating dates to 2025...")
cells_to_update = []

for i, record in enumerate(records):
    row = i + 2  # +2 for header and 1-indexing
    
    # Parse date (handle different formats)
    date_str = record['Date']
    try:
        # Try DD/MM/YYYY format
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    except:
        try:
            # Try MM/DD/YYYY format
            date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        except:
            try:
                # Try YYYY-MM-DD format
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                print(f"  Warning: Could not parse date '{date_str}' in row {row}")
                continue
    
    # Shift to 2025 (keep same month/day)
    new_date = date_obj.replace(year=2025)
    
    # Format as YYYY-MM-DD (ISO format)
    new_date_str = new_date.strftime('%Y-%m-%d')
    
    # Add to batch update (column A = 1)
    cells_to_update.append(gspread.Cell(row, 1, new_date_str))
    
    if (i + 1) % 100 == 0:
        print(f"  Prepared {i + 1} rows...")

# Update in batches
print(f"\nUpdating {len(cells_to_update)} dates...")
batch_size = 100
for i in range(0, len(cells_to_update), batch_size):
    end = min(i + batch_size, len(cells_to_update))
    worksheet.update_cells(cells_to_update[i:end])
    print(f"  Updated rows {i+1} to {end}")

print("\n" + "=" * 80)
print("SUCCESS! All dates updated to 2025")
print("=" * 80)
print("\nYour sheet now has dates starting from 2025")
print("You can now query current dates:")
print("  curl http://127.0.0.1:8000/api/v1/forecast/daily")
