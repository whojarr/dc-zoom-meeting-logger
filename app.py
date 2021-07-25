import os
import json
import boto3
from flask import Flask, request

app = Flask(__name__)

ZOOM_VARIFICATION_TOKEN = os.environ['ZOOM_VARIFICATION_TOKEN']
MEETINGS_SNS_TOPIC = os.environ['MEETINGS_SNS_TOPIC']
MEETINGS_SNS_ARN = os.environ['MEETINGS_SNS_ARN']

dbclient = boto3.client('dynamodb')
dbresource = boto3.resource('dynamodb')
snsclient = boto3.client('sns')


def sns_publish(data):

    response = snsclient.publish(
        TopicArn=MEETINGS_SNS_ARN,
        Message=json.dumps({'default': json.dumps(data)}),
        Subject='Zoom Meeting Log Entry',
        MessageStructure='json'
    )

    return response


@app.route("/", methods = ['POST'])
def meetings():

    auth_header = request.headers.get('Authorization')
    if not auth_header == ZOOM_VARIFICATION_TOKEN:
        print("Authentication Failed. {} != {}".format(auth_header, ZOOM_VARIFICATION_TOKEN))
        resp = app.response_class(
            response=json.dumps("unauthorised"),
            status=401,
            mimetype='application/json'
        )
        return resp

    data = request.json
    sns_publish(data)
    response = "ok"

    resp = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

    return resp