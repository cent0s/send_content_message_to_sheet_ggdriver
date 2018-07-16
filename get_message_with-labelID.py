"""Get a list of Messages from the user's mailbox.
"""

from apiclient import errors
import time
import os
from threading import Timer
import sys
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import requests
import sys
import json

import base64
import email

####################### Setup the Gmail API #############################
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    # creds = None
service = build('gmail', 'v1', http=creds.authorize(Http()))
####################### Setup the Gmail API #############################

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.
  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])
        # for message in messages:
        #     print message

        return messages
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def GetMessage(service, user_id, msg_id):
    """Get a Message with given ID.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.
    Returns:
      A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        # print 'Message snippet: %s' % message['snippet']

        current_subject = message['payload']['headers'][38]['value']
        print current_subject
        # print message['snippet']
        # print message['payload']['body']['data']

        # Get content message clear text by message_id
        # message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
        #
        # msg_str = base64.urlsafe_b64decode(message['raw'].replace('-_', '+/').encode('ASCII'))
        # print msg_str

        return message

    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def update_subject_content(content_subject):
    file = open("last_message.txt", "w")
    file.close()
    time.sleep(1)
    file = open("last_message.txt", "w")
    file.write(content_subject)
    file.close()


def hipchat_notify(token, room, message, color='yellow', notify=False,
                   format='text', host='api.hipchat.com'):
    """Send notification to a HipChat room via API version 2
    Parameters
    ----------
    token : str
        HipChat API version 2 compatible token (room or user token)
    room: str
        Name or API ID of the room to notify
    message: str
        Message to send to room
    color: str, optional
        Background color for message, defaults to yellow
        Valid values: yellow, green, red, purple, gray, random
    notify: bool, optional
        Whether message should trigger a user notification, defaults to False
    format: str, optional
        Format of message, defaults to text
        Valid values: text, html
    host: str, optional
        Host to connect to, defaults to api.hipchat.com
    """

    if len(message) > 10000:
        raise ValueError('Message too long')
    if format not in ['text', 'html']:
        raise ValueError("Invalid message format '{0}'".format(format))
    if color not in ['yellow', 'green', 'red', 'purple', 'gray', 'random']:
        raise ValueError("Invalid color {0}".format(color))
    if not isinstance(notify, bool):
        raise TypeError("Notify must be boolean")

    url = "https://{0}/v2/room/{1}/notification".format(host, room)
    headers = {'Content-type': 'application/json'}
    headers['Authorization'] = "Bearer " + token
    payload = {
        'message': message,
        'notify': notify,
        'message_format': format,
        'color': color
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)


if __name__ == '__main__':
    list_messages = ListMessagesWithLabels(service, 'me', 'Label_26')
id_last_message = list_messages[0]['id']
current_message = GetMessage(service, 'me', id_last_message)
# help python can read special string encode utf8 japanese letter
reload(sys)
sys.setdefaultencoding('utf-8')
current_subject = str(current_message['payload']['headers'][38]['value'])
# write the first subject message to compare with after check
# file = open("last_message.txt", "w")
# file.write(current_subject)


file = open("last_message.txt", "r")
before_subject = file.read()
file.close()
# print "The lasest subject %s" % before_subject
token = 'p45CptgxUGc0qvlxSWCyZPR7C60WhxrPLNYXHDQx'
room = '4090741'
if os.stat("last_message.txt").st_size == 0:
    print "Please give subject to last_message.txt file"
else:
    if current_subject == before_subject:
        message_normal = "We don't have new message"
        hipchat_notify(token, room, message_normal, "green")
    else:
        update_subject_content(current_subject)
        warning_message = "WARING...WE HAVE NEW MESSAGE IN RKT PROJECT"
        hipchat_notify(token, room, warning_message, "red")


# https://developers.google.com/gmail/api/v1/reference/users/messages
