# Purpose
The purpose of this application is to utilize apscheduler to write datetime records to a Google Sheet

# How to use
To use the application, simply:
1. Clone this repo
2. Login to your Google Cloud console
3. Enable the Google Drive API and the Google Sheets API
4. Create a new Google Cloud project, or modify the existing project
5. Create a service account
6. Once the service account is created, open it up, hit the KEYS tab, and create a new key. Pick the JSON option. After that, the browser will download a json file
7. Open up the json file and update the environment variables in docker-compose.yml file
8. Note that, you need to invoke the create_new_sheet() function once. This will create a new Google Sheet
9. Then use the list_sheets() function to list the created Google Sheet, and then copy the sheet ID
10. Go back to docker-compose.yml file and then update the value of list_sheets
11. Run docker-compose up -d locally
12. Run docker logs -f app to check the container logs. You'll be able to see the sheet URL in the logs. Open the URL to watch the modification on the sheet