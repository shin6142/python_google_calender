import json
import os
import datetime, re
import googleapiclient.discovery
import google.auth

credentials = {
                "type": "service_account",
                "project_id": os.environ['PROJECT_ID'],
                "private_key_id": os.environ['PRIVATE_KEY_ID'],
                "private_key": os.environ['PRIVATE_KEY'],
                "client_email": os.environ['CLIENT_EMAIL'],
                "client_id": os.environ['CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['CLIENT_X509_CERT_URL']
             }


class CalenderClass(object):
    def __init__(self):
        with open('credentials.json', 'w') as credentials_json:
            json.dump(credentials, credentials_json)

        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendar_id = 'yamagashin6142@gmail.com'
        self.gapi_creds = google.auth.load_credentials_from_file('credentials.json', self.SCOPES)[0]
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=self.gapi_creds)

class GetEvent(CalenderClass):
    def get_event(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = self.service.events().list(
            calendarId= self.calendar_id, timeMin=now,
            maxResults=1, singleEvents=True,
            orderBy='startTime').execute()
        
        events_result = events_result.get('items', None)[0]

        result_dict = {}
        result_dict['title'] = events_result['summary']
        result_dict['link'] = events_result['htmlLink']
        result_dict['start_time'] = events_result['start']
        result_dict['end_time'] = events_result['end']
        if 'description' in result_dict:
                result_dict['description'] = events_result['description']
        else:
            result_dict['description'] = ''

        return result_dict