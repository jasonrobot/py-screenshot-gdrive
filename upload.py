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

import time

import subprocess
from subprocess import Popen, PIPE

import pyperclip

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    #parser.add_argument('image')
    flags = parser.parse_args()
except ImportError:
    flags = None

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'only-just-a-test'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    auth_scopes = {'drive': 'https://www.googleapis.com/auth/drive',
                   'urlshortener': 'https://www.googleapis.com/auth/urlshortener'}

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credentials = dict()
    for key in auth_scopes:
        credential_path = os.path.join(credential_dir,
                                       'only-just-a-test-' + key + '.json')

        store = oauth2client.file.Storage(credential_path)
        credentials[key] = store.get()
        if not credentials[key] or credentials[key].invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, auth_scopes[key])
            flow.user_agent = APPLICATION_NAME
#        if flags:
            credentials[key] = tools.run_flow(flow, store, flags)
#        else: # Needed only for compatability with Python 2.6
#            credentials = tools.run(flow, store)
            print('Storing ' + key + ' credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """

    image_file_name = "Screenshot_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".png"

    #subprocess.call(["scrot"])
    #Popen(["scrot", "-s",  image_file_name])
    subprocess.call(["scrot", "-s", image_file_name])

    #print(flags.image)
    #fileName = flags.image

    credentials = get_credentials()
    http = dict()
    for key in credentials:
        http[key] = credentials[key].authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v2', http=http['drive'])
    files_resource = drive_service.files()

    #query = service.files().list(q="title contains 'screenshots'").execute().items[0].id
    #print(query)
    screenshot_folder = files_resource.list(q="title contains 'screenshots'").execute()['items'][0]['id']

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

    file = MediaFileUpload(image_file_name, mimetype="image/png", resumable=True)

    result = files_resource.insert(media_body=file, body=metadata).execute()

    links = dict()
    #this one opens in the google drive window. Not bad, but not fullscreen
    #links['alternateLink'] = result.get('alternateLink', [])
    #this will give us a direct link to the file if we trim '&export=download' off the end
    links['webContentLink'] = result.get('webContentLink', [])

    image_link = links['webContentLink'].split('&')[0]
    # print(image_link)

    # for key in links:
    #     print(key)
    #     print(links[key])
    #     print("")

    shortener_service = discovery.build('urlshortener', 'v1', http['urlshortener'])
    shortener_resource = shortener_service.url()
    shortener_request_body = {
        "longUrl": image_link
    }
    shortener_response = shortener_resource.insert(body=shortener_request_body).execute()
    short_url = shortener_response.get('id', [])
    print("Url is: " + short_url)

    pyperclip.copy(short_url)

if __name__ == '__main__':
    main()
