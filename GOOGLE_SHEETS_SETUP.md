# Google Sheets Setup Guide

This guide will help you set up Google Sheets API access for the OUNASS Pod Forecasting API.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on "Select a project" at the top
3. Click "NEW PROJECT"
4. Enter project name: "OUNASS Pod Forecasting"
5. Click "CREATE"

## Step 2: Enable Google Sheets API

1. In your Google Cloud project, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and then click "ENABLE"
4. Also search for and enable "Google Drive API"

## Step 3: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" > "Service account"
3. Fill in the details:
   - Service account name: `ounass-pod-forecasting`
   - Service account ID: (auto-generated)
   - Description: "Service account for OUNASS pod forecasting API"
4. Click "CREATE AND CONTINUE"
5. Skip the optional steps and click "DONE"

## Step 4: Create and Download Credentials

1. In the "Credentials" page, find your newly created service account
2. Click on the service account email
3. Go to the "KEYS" tab
4. Click "ADD KEY" > "Create new key"
5. Choose "JSON" format
6. Click "CREATE"
7. The credentials JSON file will be downloaded automatically
8. Rename the file to `credentials.json`
9. Move it to your project root directory

## Step 5: Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "OUNASS Pod Data"
4. Create the following column headers in the first row:
   - Date
   - GMV
   - Users
   - Marketing_Cost
   - Frontend_Pods
   - Backend_Pods

## Step 6: Share Sheet with Service Account

1. Open your Google Sheet
2. Click the "Share" button in the top right
3. Copy the service account email from your credentials.json file
   - It looks like: `ounass-pod-forecasting@project-name.iam.gserviceaccount.com`
4. Paste the email in the "Add people and groups" field
5. Set permission to "Viewer" (read-only access)
6. Uncheck "Notify people"
7. Click "Share"

## Step 7: Get Your Sheet ID

1. Look at your Google Sheet URL
2. It will look like: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
3. Copy the `SHEET_ID` part (between `/d/` and `/edit`)
4. Save this for your `.env` file

## Step 8: Import Sample Data

You can import the sample data from `data/sample_data.csv`:

1. In your Google Sheet, go to File > Import
2. Upload the `sample_data.csv` file
3. Choose "Replace current sheet"
4. Import location: "Replace current sheet"
5. Separator type: "Comma"
6. Click "Import data"

## Step 9: Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Fill in your values:
   ```
   GOOGLE_SHEET_ID=your_sheet_id_here
   GOOGLE_CREDENTIALS_PATH=./credentials.json
   ```

## Data Format

Your Google Sheet should have the following structure:

| Date       | GMV     | Users | Marketing_Cost | Frontend_Pods | Backend_Pods |
|------------|---------|-------|----------------|---------------|--------------|
| 2024-01-01 | 1200000 | 18000 | 45000          | 10            | 6            |
| 2024-01-02 | 1150000 | 17500 | 42000          | 9             | 6            |
| ...        | ...     | ...   | ...            | ...           | ...          |
| 2024-06-30 | 1690000 | 25400 | 62000          | 15            | 10           |
| 2024-07-01 | 1900000 | 28500 | 67500          |               |              |
| 2024-07-02 | 1950000 | 29200 | 69000          |               |              |

**Notes:**
- Historical data (Jan-June): Should have all columns filled including pod counts
- Budget data (July onwards): Only GMV, Users, and Marketing_Cost are filled
- The API will predict Frontend_Pods and Backend_Pods for budget rows
- Dates should be in YYYY-MM-DD format
- All numeric values should be numbers (no currency symbols or commas)

## Troubleshooting

### Authentication Error
- Make sure the credentials.json file is in the correct location
- Verify the service account has access to the sheet
- Check that both Google Sheets API and Google Drive API are enabled

### No Data Found
- Verify your GOOGLE_SHEET_ID is correct
- Check that the sheet name in the code matches your sheet tab name
- Ensure column headers match exactly (case-sensitive)

### Permission Denied
- Confirm you've shared the sheet with the service account email
- Check that the service account has at least "Viewer" permission

## Security Notes

- Keep your `credentials.json` file secure and never commit it to version control
- The `.gitignore` file is configured to exclude credential files
- Service accounts should only have read access to the Google Sheet
- Regularly rotate service account keys for production use
