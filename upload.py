#!/usr/bin/python
"""Just a thing I'm testing

Apparently, this is where the module-level docstring goes
"""

import httplib2
import os

from apiclient import discovery
from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('image')
    flags = parser.parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'only-just-a-test'


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
    credential_path = os.path.join(credential_dir,
                                   'only-just-a-test.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
#        if flags:
        credentials = tools.run_flow(flow, store, flags)
#        else: # Needed only for compatability with Python 2.6
#            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """

    #print(flags.image)
    fileName = flags.image

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    #query = service.files().list(q="title contains 'screenshots'").execute().items[0].id
    #print(query)
    screenshot_folder = service.files().list(q="title contains 'screenshots'").execute()['items'][0]['id']

    #metadata = "{\"parents\":[{\"id\":\"screenshots\"}]}"
    metadata = {
        "mimeType": "image/png",
        "parents":
        [
            {
                "id": screenshot_folder
            }
        ]
    }

    file = MediaFileUpload(fileName, mimetype="image/png", resumable=True)

    result = service.files().insert(media_body=file, body=metadata).execute()

    link = result.get('alternateLink', [])
    print(link)

if __name__ == '__main__':
    main()
