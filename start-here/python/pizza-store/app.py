from flask import Flask, request, jsonify
from cloudevents.http import from_http
from dapr.clients import DaprClient

import uuid
import os
import time
import logging
import json
import requests


DAPR_STORE_NAME = 'pizzastatestore'
DAPR_PUBSUB_NAME = 'pizzapubsub'
DAPR_PUBSUB_TOPIC_NAME = 'order'
DAPR_PORT = 8001

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def save_order(order_id, order_data):

    with DaprClient() as client:

        # Save state into the state store
        client.save_state(DAPR_STORE_NAME, order_id, str(order_data))
        print('Saving Order %s with event %s', order_id, order_data['event'])

        # Get state from the state store
        result = client.get_state(DAPR_STORE_NAME, order_id)
        print('Result after get: ' + str(result.data))

        return order_id

# ------------------- Dapr service invocation ------------------- #

def start_cook(order_data):
    base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
                    'DAPR_HTTP_PORT', '3500')
    # Adding app id as part of the header
    headers = {'dapr-app-id': 'pizza-kitchen', 'content-type': 'application/json'}

    url = '%s/orders' % (base_url)
    print('url: ' + url, flush=True)

    # Invoking a service
    result = requests.post(
        url='%s/cook' % (base_url),
        data=json.dumps(order_data),
        headers=headers
    )
    print('result: ' + str(result), flush=True)

    time.sleep(1)

# ------------------- Dapr pub/sub ------------------- #

# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/events', methods=['POST'])
def orders_subscriber():
    event = from_http(request.headers, request.get_data())
    print('Subscriber received : %s' % event.data['order_id'], flush=True)

    save_order(event.data['order_id'], event.data)

    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}


# ------------------- Application routes ------------------- #

@app.route('/orders', methods=['POST'])
def createOrder():

    # Create a new order id
    order_id = str(uuid.uuid4())
    order_data = request.json

    order_data['order_id'] = order_id
    order_data['event'] = 'Sent to kitchen'

    # Save order to state store
    save_order(order_id, order_data)

    # Send order to kitchen
    start_cook(order_data)

    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}


app.run(port=8001)