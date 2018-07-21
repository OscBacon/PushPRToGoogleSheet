# PushPRToGoogleSheet
This is an AWS Lambda function to log pull request creation to Google Sheets.

## How to use
### 1. Setup Google Sheets API
In order to edit a Google Sheet, you need to create a Google Sheet and note its id.

You must then enable the Google Sheets API. To do so, go to the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard).

To obtain an authenticaiton key that doesn't expire, create a service account for the function to use. Save the service account credentials as `credentials.json`

### 2. Setup AWS
Upload this repository as a zip to a new AWS Lambda function.

Set the `SPREADSHEET_ID` environment variable.

If you want to use Slack to be notified about a new PR, add set the `SLACK_API_TOKEN` variable.

Add an AWS Gateway API as the trigger. 

Let the Gateway accept POST requests, deploy it, and save the link to the Gateway.

### 3. Setup GitHub
Enter the settings of your desired repository.

Go to Webhooks, and create a webhook with the Payload URL being your Gateway, add a secret if desired.

In the events to trigger the playbook, only select Pull requests.

Finally, press 'Add webhook', and voilà, your spreadsheet is now logging your pull requests!
