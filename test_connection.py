#!/usr/bin/env python3
"""Test Google Sheets Connection"""
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
CREDS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

print("Testing Google Sheets Connection...")
print(f"Sheet ID: {SHEET_ID}")
print(f"Credentials: {CREDS_PATH}")
print("-" * 80)

try:
    # Connect
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    credentials = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    client = gspread.authorize(credentials)
    
    print("✅ Connected to Google Sheets API")
    
    # Open spreadsheet
    spreadsheet = client.open_by_key(SHEET_ID)
    print(f"✅ Opened spreadsheet: {spreadsheet.title}")
    
    # List all worksheets
    print("\nAvailable sheet tabs:")
    worksheets = spreadsheet.worksheets()
    for i, ws in enumerate(worksheets, 1):
        print(f"  {i}. '{ws.title}' ({ws.row_count} rows x {ws.col_count} cols)")
    
    # Try to open Sheet1
    print("\nTrying to access 'Sheet1'...")
    worksheet = spreadsheet.worksheet("Sheet1")
    print(f"✅ Found 'Sheet1': {worksheet.row_count} rows x {worksheet.col_count} cols")
    
    # Get header row
    print("\nColumn headers:")
    headers = worksheet.row_values(1)
    for i, header in enumerate(headers, 1):
        print(f"  {i}. '{header}'")
    
    # Get first few rows
    print("\nFirst 3 data rows:")
    records = worksheet.get_all_records()[:3]
    for i, record in enumerate(records, 1):
        print(f"  Row {i}: {record}")
    
    print("\n" + "=" * 80)
    print("SUCCESS! Google Sheets is accessible.")
    print("=" * 80)
    
except gspread.exceptions.WorksheetNotFound as e:
    print(f"\n❌ ERROR: Worksheet not found - {e}")
    print("\nAvailable sheets:")
    for ws in spreadsheet.worksheets():
        print(f"  - '{ws.title}'")
    print("\nMake sure you have a tab named 'Sheet1' (case-sensitive)")
    
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"\n❌ ERROR: Spreadsheet not found - {e}")
    print("\nCheck:")
    print("  1. Sheet ID is correct in .env file")
    print("  2. Sheet is shared with service account email")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    print("\nFull error:")
    traceback.print_exc()
