from flask import Flask
import os
import json
import googleapiclient.discovery
import google.auth
import tempfile
from g_calender import GetEvent

app = Flask(__name__)



@app.route('/')
def index():
    obj = GetEvent()
    result = obj.get_event()
    return result



    
if __name__ == '__main__':
    app.run()
