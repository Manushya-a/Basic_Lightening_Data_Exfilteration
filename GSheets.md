# Google Sheets API Setup Guide

Follow these steps to enable and configure the Google Sheets API for use with the Lightning Data Collector project.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on **"Select a project"** in the top right corner
3. Click **"New Project"** in the top right of the popup
4. Click **"Create a project"**
5. Enter your project name (e.g., "Lightning-Data-Collector")
6. Select organization if applicable
7. Click **"Create"**

## Step 2: Enable Google Sheets API

1. In the notifications area, select your new project
2. Click **"Select Project"**
3. Navigate to **"APIs & Services"** in the left sidebar
4. Click **"Enable APIs and Services"**
5. Search for **"Google Sheets API"**
6. Select it from the results
7. Click **"Enable"**
8. After enabling, click **"Manage"**

## Step 3: Create Service Account Credentials

1. Click **"Create Credentials"**
2. Select:
   - **Which API are you using?** Google Sheets API
   - **Where will you be calling the API from?** Other UI (e.g., Windows, CLI)
   - **What data will you be accessing?** Application data
3. Click **"Next"**

## Step 4: Set Up Service Account

1. Enter:
   - **Service account name**: `lightning-data` (or your preferred name)
   - **Service account ID**: Will auto-generate
2. Click **"Create and Continue"**
3. Set role to **"Editor"**
4. Click **"Continue"**
5. Click **"Done"**

## Step 5: Generate JSON Key File

1. Navigate to the **"Credentials"** tab
2. Click on your newly created service account
3. Go to the **"Keys"** tab
4. Click **"Add Key"** → **"Create new key"**
5. Select **JSON** format
6. Click **"Create"**

This will download a JSON key file to your computer.

## Step 6: Configure Project Files

1. Move the downloaded JSON file to your project folder
2. Rename the file to: `credentials.json`

## Step 7: Set Up Google Sheet Sharing

1. Create a new Google Sheet or use an existing one
2. Click **"Share"** in the top right corner
3. In the sharing dialog:
   - Paste your service account email (found in the JSON file or in Google Cloud Console under Service Accounts)
   - Example format: `lightning-data@your-project-id.iam.gserviceaccount.com`
4. Set permission to **"Editor"**
5. Click **"Send"**

## Step 8: Configure Script

1. Open your project code
2. Locate the line with `sheets_id = "Link-to-your-google-spreadsheet"`
3. Replace it with your Google Sheet ID (found in the sheet's URL)
   - Example: `https://docs.google.com/spreadsheets/d/ABC123xyz/edit#gid=0`
   - The ID is `ABC123xyz`

## Verification

To verify everything is working:
1. Run the script in Google Sheet mode:
   ```bash
   python lightning_collector.py -gsheet 5