from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    return json

if __name__ == '__main__':
    app.run()