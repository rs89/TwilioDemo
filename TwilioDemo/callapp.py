# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import bottle
from bottle import route, run, post, Response
from twilio import twiml
from twilio.rest import TwilioRestClient


app = bottle.default_app()
# copy the account SID and auth token from the Twilio Console and paste below
twilio_client = TwilioRestClient('AC67c8a24c21e9835ca3030f7048702159' ,
                                 '360607a6539707b51c0ab1ec39efb437')


# input your Twilio number in the second string on the next line
TWILIO_NUMBER = '+14049752744'
NGROK_BASE_URL =  'https://e2360b77.ngrok.io'


@route('/')
def index():
    """Returns standard text response to show app is working."""
    return Response("Bottle app up and running!")


@post('/twiml')
def twiml_response():
    """Provides TwiML instructions in response to a Twilio POST webhook
    event so that Twilio knows how to handle the outbound phone call
    when someone picks up the phone.
    """
    response = twiml.Response()
    response.say("Hello, this call is from a Bottle web application.")
    response.play("https://api.twilio.com/cowbell.mp3", loop=10)
    return Response(str(response))


@route('/dial-phone/<outbound_phone_number>')
def outbound_call(outbound_phone_number):
    """Uses the Twilio Python helper library to send a POST request to
    Twilio telling it to dial an outbound phone call from our
    specific Twilio phone number (that phone number must be owned by our
    Twilio account).
    """
    # the url must match the Ngrok Forwarding URL plus the route defined in
    # the previous function that responds with TwiML instructions
    twilio_client.calls.create(to=outbound_phone_number,
                               from_=TWILIO_NUMBER,
                               url=NGROK_BASE_URL + '/twiml')
    return Response('phone call placed to ' + outbound_phone_number + '!')


if __name__ == '__main__':
    run(host='127.0.0.1', port=5000, debug=False, reloader=True)