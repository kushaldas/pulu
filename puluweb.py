import json
from pprint import pprint
from flask import Flask, request

from pulu.system import get_post
from pulu.utils import update

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/updatehook/', methods=['POST'])
def updatehook():
    """
    Should be called after github hook calls our app.

    :return: String "done"
    """
    rf = request.form
    if request.method == 'POST':
        if 'payload' in rf:
            update(rf['payload'])

    return "done"


if __name__ == '__main__':
    app.run(debug=True)
