from flask import Flask, redirect
from flask import render_template
from flask import request
import os, json
import ibmiotf.application
import uuid

client = None

organization = "kjmozg"
appId = str(uuid.uuid4())
authkey = "a-kjmozg-sldw2kbkq7"
authtoken = "prHK!y8*Ql*8B&nc48"

deviceType = "raspberry-leoniknik-0417"
deviceId = "raspberry-leo-0417"


def myEventCallback(event):
    print(event.data)
    pass

try:
    appOptions = {"org": organization, "id": appId, "auth-method": "apikey", "auth-key": authkey,
                  "auth-token": authtoken}
    client = ibmiotf.application.Client(appOptions)
    client.connect()
    client.deviceEventCallback = myEventCallback
    client.subscribeToDeviceEvents(event="input")

except ibmiotf.ConnectionException as e:
    print(e)

app = Flask(__name__)

if os.getenv("PORT"):
    port = int(os.getenv("PORT"))
else:
    port = 8080


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/light/<command>', methods=['GET', 'POST'])
def light_route(command):
    print(command)
    myData = {'command': command}
    client.publishCommand(deviceType, deviceId, "light", data=myData, msgFormat="json")
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
