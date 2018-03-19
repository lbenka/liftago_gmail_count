from datetime import datetime, timedelta

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'client_id.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    gmail = discovery.build('gmail', 'v1', http=http)

    first = datetime.now().date().replace(day=1)
    last = first + timedelta(days=31)
    first = first.strftime('%Y/%m/%d')
    last = last.strftime('%Y/%m/%d')
    query = 'ride with liftago after:{0} before:{1}'.format(first, last)

    results = gmail.users().messages().list(userId='me',
                                            labelIds=None,
                                            pageToken=None,
                                            q=query,
                                            maxResults=25,
                                            includeSpamTrash=False).execute()
    wanted_data = []
    for msg in results.get('messages', []):
        msg_object = gmail.users().messages().get(userId='me', id=msg.get('id')).execute()

        wanted_data.append(float(msg_object.get('snippet').split()[0][3:]))

    print('For this month it is: {} CZK'.format(sum(wanted_data)))


if __name__ == '__main__':
    main()
