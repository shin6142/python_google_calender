import json
import os
import tempfile
import datetime, re
import googleapiclient.discovery
import google.auth

#環境変数取得
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
GOOGLE_CREDENTIALS = os.environ["GOOGLE_CREDENTIALS"]





class CalenderClass(object):
    def __init__(self):
        def _google_creds_as_file():
            temp = tempfile.NamedTemporaryFile()
            temp.write(json.dumps([b'{GOOGLE_CREDENTIALS}']))
            temp.flush()
            return temp

        self.creds_file = _google_creds_as_file()
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendar_id = 'yamagashin6142@gmail.com'
        self.gapi_creds = google.auth.load_credentials_from_file(self.creds_file, self.SCOPES)[0]
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