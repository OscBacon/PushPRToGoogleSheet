import os
from datetime import datetime
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from slackclient import SlackClient

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SERVICE_ACCOUNT_FILE = 'credentials.json'
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SC = SlackClient(SLACK_API_TOKEN)


def lambda_handler(event, context):
    """ Handles incoming pull request creation payload """
    if "pull_request" not in event or event["action"] != "opened":
        return

    service = build('sheets', 'v4', credentials=CREDENTIALS,
                    cache_discovery=False)

    range_name = 'A2:E2'

    # Row contains: number, url, title, created_at, user.login
    # row_value = ['3', 'http://github.com', 'Test PR',
    #            datetime.now().strftime("%m/%d/%Y %H:%M:%S"), 'Oscar']
    created_at = datetime.strptime(
        event["pull_request"]["created_at"],
        "%Y-%m-%dT%H:%M:%SZ"
    ).strftime("%m/%d/%Y %H:%M:%S")
    title = event["pull_request"]["title"]
    url = event["pull_request"]["html_url"]
    user = event["pull_request"]["user"]["login"]

    row_value = [event["pull_request"]["number"],
                 url,
                 title,
                 created_at,
                 user]

    body = {'requests': [{
        'insertDimension': {
            'range': {
                'dimension': 'ROWS',
                'startIndex': 1,
                'endIndex': 2
            }
        }
    }]}
    request1 = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                                  body=body)

    request2 = service.spreadsheets().values()\
        .append(spreadsheetId=SPREADSHEET_ID,
                range=range_name,
                valueInputOption='USER_ENTERED',
                insertDataOption='OVERWRITE',
                body={'values': [row_value]})
    request1.execute()
    request2.execute()

    sheet_url = "https://docs.google.com/spreadsheets/d/{}".format(
        SPREADSHEET_ID)

    SC.api_call(
        "chat.postMessage",
        channel="backteam",
        text="<{}|New PR Created> \n <{}|{}> by {}".format(
            sheet_url, url, title, user)
    )


lambda_handler({}, {})
