from flask import Flask
from g_calender_api import GetEvent

app = Flask(__name__)

@app.route('/')
def index():
    obj = GetEvent()
    result = obj.get_event()
    return result

if __name__ == '__main__':
    app.run()