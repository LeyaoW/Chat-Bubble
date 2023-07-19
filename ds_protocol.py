# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.


from collections import namedtuple
import time

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['typ', 'username', 'message', 'token'])


def join(usr, pwd):  # Compose JSON message for joining server
    join = {"join": {"username": usr, "password": pwd, "token": ''}}
    return join


def post(msg, token):  # Compose JSON message for posting message on server
    post = {"token": token, "post": {"entry": msg, "timestamp": time.time()}}
    return post


def bio(bio, token):  # Compose JSON message for posting bio on server
    bio = {"token": token, "bio": {"entry": bio, "timestamp": time.time()}}
    return bio


def send_message_to_user(token, entry, recipient):
    data = {"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": time.time()}}
    return data


def get_unread_message(token):
    data = {"token": token, "directmessage": "new"}
    return data


def get_all_message(token):
    data = {"token": token, "directmessage": "all"}
    return data
