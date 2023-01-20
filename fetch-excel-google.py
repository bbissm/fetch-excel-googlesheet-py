#! /usr/bin/env python3
import requests
import json
import pandas as pd
# First, you need to install gspread and oauth2client

# Import the necessary modules
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import webbrowser

# Use your own credentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
service = build("drive", "v3", credentials=creds)

# Fetch JSON data from a URL
api_end_point = input("What is the API endpoint?")

response = requests.get(api_end_point)

if response.status_code == 200:
    data = json.loads(response.text)

    # Convert JSON data to a pandas DataFrame
    df = pd.json_normalize(data)

    #create a new sheet in google sheets
    sh = client.create("components.xlsx")
    worksheet = sh.get_worksheet(0)
    set_with_dataframe(worksheet, df)
    sheet_url = sh.url
    # Replace this with your own email address
    email_address = input("What is your email address?")

    # Get the sheet ID
    sheet_id = sh.id

    # Build the request body
    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email_address
    }

    # Share the sheet with the specified user
    response = service.permissions().create(
        fileId=sheet_id,
        body=permission,
        sendNotificationEmail=True
    ).execute()

    print(f'Sheet shared with {email_address}')
    webbrowser.open(sheet_url)
else:
    print('Failed to fetch data. Error code:', response.status_code)
