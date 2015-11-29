#!/usr/bin/python
#
# hermes.pushover
#
# Based on pushover project by wyattjoh:
# https://github.com/wyattjoh/pushover.git
# some basic python classes to interact with Pushover REST API:
# https://pushover.net/api
#
from http.client import HTTPSConnection
from urllib.parse import urlencode
import json


class PushoverError(Exception):
    pass


class PushoverMessage:

    """
    Used for storing message specific data.
    """

    def __init__(self, message):
        """
        Creates a Pushover message object.
        """
        self.vars = {}
        self.vars['message'] = message

    def set(self, key, value):
        """
        Sets the value of a field "key" to the value of "value".
        """
        if value is not None:
            self.vars[key] = value

    def get(self):
        """
        Returns a dictionary with the values for the specified message.
        """
        return self.vars

    def user(self, user_token, user_device=None):
        """
        Sets a single user to be the recipient of this message with token
        "user_token" and device "user_device".
        """
        self.set('user', user_token)
        self.set('device', user_device)

    def __str__(self):
        return "PushoverMessage: " + str(self.vars)


class Pushover:

    """
    Creates a Pushover handler.
    Usage:
        po = Pushover("My App Token")
        po.user("My User Token", "My User Device Name")
        msg = po.msg("Hello, World!")
        po.send(msg)
    """

    PUSHOVER_SERVER = "api.pushover.net:443"
    PUSHOVER_ENDPOINT = "/1/messages.json"
    PUSHOVER_CONTENT_TYPE = {
        "Content-type": "application/x-www-form-urlencoded"
        }

    def __init__(self, token=None):
        """
        Creates a Pushover object.
        """

        if token is None:
            raise PushoverError("No token supplied.")
        else:
            self.token = token
            self.user_token = None
            self.user_device = None
            self.messages = []

    def set(self, key, value):
        """
        Sets the value of a field "key" to the value of "value".
        Examples:
          priority - send as -2 to generate no notification/alert, -1 to always
          send as a quiet notification, 1 to display as high-priority and
          bypass the user's quiet hours, or 2 to also require confirmation from
          the user.
          url - a supplementary URL to show with your message.
          sound - the name of one of the sounds supported by device clients to
          override the user's default sound choice.
        """
        if value is not None:
            self.vars[key] = value

    def msg(self, message):
        """
        Creates a PushoverMessage object. Takes one "message" parameter (the
            message to be sent).
        Returns with PushoverMessage object (msg).
        """
        message = PushoverMessage(message)
        self.messages.append(message)
        return message

    def user(self, user_token, user_device=None):
        """
        Sets a single user to be the recipient of all messages created with
        this Pushover object.
        device - your user's device name to send the message directly to that
        device, rather than all of the user's devices (multiple devices may be
        separated by a comma)
        """
        self.user_token = user_token
        self.user_device = user_device

    def send(self, message):
        """
        Sends a specified message with id "message" or as object.
        """
        # Only send message if message is instance of PushoverMessage
        if type(message) is PushoverMessage:
            # get dict contaning "message" and any other key-values declared
            # by the "set" method.
            data = message.get()
            data['token'] = self.token
            # define which user to send notification to if any
            if self.user is not None:
                data['user'] = self.user_token
                # define which device to send notification to if any
                if self.user_device is not None:
                    data['device'] = self.user_device
            # initialise HTTPS connection
            conn = HTTPSConnection(self.PUSHOVER_SERVER)
            # send HTTPS request
            conn.request(
                "POST",
                self.PUSHOVER_ENDPOINT,
                urlencode(data),
                self.PUSHOVER_CONTENT_TYPE
            )
            # get response form server
            response = conn.getresponse().read().decode('utf-8')
            data = json.loads(response)
            # check response for error
            if data['status'] != 1:
                raise PushoverError(response)
            else:
                return True
        else:
            raise PushoverError("Wrong type passed to Pushover.send()!")
