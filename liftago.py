import os.path
import pickle
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_client():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def main():
    service = get_gmail_client()

    first = datetime.now().date().replace(day=1)
    last = first + timedelta(days=31)  # no need to be super precise

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=None,
            pageToken=None,
            q=f"ride with liftago after:{first:%Y/%m/%d} before:{last:%Y/%m/%d}",
            maxResults=25,
            includeSpamTrash=False,
        )
        .execute()
    )

    wanted_data = []
    for msg in results.get("messages", []):
        msg_object = service.users().messages().get(userId="me", id=msg.get("id")).execute()

        wanted_data.append(float(msg_object.get("snippet").split()[0][3:]))

    print(f"For this month it is: {sum(wanted_data)} CZK")


if __name__ == "__main__":
    main()
