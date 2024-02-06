import os
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Variables Initialization
sheet_id = os.environ.get("GOOGLE_SHEET_ID") # The google sheet ID we want to edit
share_with = os.environ.get("SHARE_WITH") # The email address we want the google sheet to share with
port = int(os.environ.get("PORT", 5000))

def authorize():
    try:
        # Replace 'path/to/your/credentials.json' with the path to your downloaded JSON file
        credentials_path = 'credentials.json'

        # Set up the scope and access credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        return gspread.authorize(credentials)
    
    except Exception as e:
        print(f"Authorize error occurred: {e}")

def list_sheets():
    try:
        gc = authorize()        

        # Get a list of all accessible Google Sheets files
        sheets_list = gc.list_spreadsheet_files()
        
        print("List of Google Sheets files:")
        for sheet in sheets_list:
            print(f"- {sheet['name']} ({sheet['id']})")
        
    except Exception as e:
        print(f"List sheets error occurred: {e}")

def create_new_sheet():
    try:
        gc = authorize()

        # Create a new Google Sheet
        new_sheet = gc.create('fl0')

        print(f"New Google Sheet created. ID: {new_sheet.id}")
        
    except Exception as e:
        print(f"Create a new sheet error occurred: {e}")

def edit_sheet(sheet_id):
    try:
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        gc = authorize()

        # Replace 'Your Google Sheet Name' with the name of your Google Sheet
        worksheet = gc.open_by_key(sheet_id).sheet1

        # Hardcoded values for the new row
        new_row_values = [current_time]

        # Add a new row to the Google Sheet
        worksheet.append_row(new_row_values)
        
    except Exception as e:
        print(f"Edit sheet error occurred: {e}")

def get_sheet_details(sheet_id):
    try:
        gc = authorize()

        # Get details of the specified Google Sheet by ID
        sheet = gc.open_by_key(sheet_id)

        print(f"Details for Google Sheet (ID: {sheet_id}):")
        print(f"- Title: {sheet.title}")
        print(f"- URL: {sheet.url}")
        print(f"- Worksheet Titles: {', '.join(worksheet.title for worksheet in sheet.worksheets())}")

    except Exception as e:
        print(f"Get sheet details error occurred: {e}")

def delete_sheet(sheet_id):
    try:
        gc = authorize()

        # Delete the specified Google Sheet by ID
        gc.del_spreadsheet(sheet_id)

        print(f"Google Sheet with ID {sheet_id} deleted successfully.")
        
    except Exception as e:
        print(f"Delete sheet error occurred: {e}")

def share_sheet(sheet_id, email_address, role='reader'):
    try:
        gc = authorize()

        # Open the Google Sheet by ID
        sheet = gc.open_by_key(sheet_id)

        emails = [share_with] # Please set email addresses you want to share.
        for e in emails:
            sheet.share(e, perm_type="user", role="writer")

        print(f"Shared Google Sheet (ID: {sheet_id}) with {email_address} with {role} access.")
        
    except Exception as e:
        print(f"Share sheet error occurred: {e}")


scheduler = BackgroundScheduler(daemon=True)

# Define cron interval here
# We will trigger the cron every 5 seconds
trigger = CronTrigger(
    year="*", month="*", day="*", hour="*", minute="*", second="*/5"
)

scheduler.add_job(
    edit_sheet,
    trigger=trigger,
    args=[sheet_id]
)
scheduler.start()

# Custom operations are defined here
get_sheet_details(sheet_id)
# share_sheet(sheet_id, share_with)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
