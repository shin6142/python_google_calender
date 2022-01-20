import json
import os
import tempfile
import datetime, re
import googleapiclient.discovery
import google.auth

GOOGLE_CREDENTIALS = os.environ['GOOGLE_CREDENTIALS']
CALENDAR_ID = os.environ['CALENDAR_ID']

class CalenderClass(object):
    def __init__(self):

        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as t:
            with open(t.name, 'w+') as temp_json:
                json.dump(GOOGLE_CREDENTIALS, temp_json, indent=2)

        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendar_id = CALENDAR_ID
        self.gapi_creds = google.auth.load_credentials_from_file(temp_json.name, self.SCOPES)[0]
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