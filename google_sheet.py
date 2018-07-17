"""Get a list of Messages from the user's mailbox.
"""

from apiclient import errors
import time
import os
from threading import Timer
import sys
import json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import base64
import email
# import packages setup google drive API, Sheet API
import gspread

import pprint
import time
import re
from oauth2client.service_account import ServiceAccountCredentials

# Setup Drive API and Sheet API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope) # get email and key from creds


gfile = gspread.authorize(credentials) # authenticate with Google

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    # creds = None
service = build('gmail', 'v1', http=creds.authorize(Http()))




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



def GetMessageBody(service, user_id, msg_id):
    try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_string(msg_str)
            messageMainType = mime_msg.get_content_maintype()
            if messageMainType == 'multipart':
                    for part in mime_msg.get_payload():
                            if part.get_content_maintype() == 'text':
                                    return part.get_payload()
                    return ""
            elif messageMainType == 'text':
                    return mime_msg.get_payload()
    except errors.HttpError, error:
            print 'An error occurred: %s' % error
# def GetMimeMessage(service, user_id, msg_id):
#
#   try:
#     message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
#     # print 'Message snippet: %s' % message['snippet']
#     # msg_str = base64.urlsafe_b64decode(message['full'].encode('ASCII'))
#     # mime_msg = email.message_from_string(msg_str)
#     mime_msg = message
#
#     return message
#   except errors.HttpError, error:
#     print 'An error occurred: %s' % error
# def GetMimeMessage(service, user_id, msg_id):
#     """Get a Message and use it to create a MIME Message.
#
#     Args:
#       service: Authorized Gmail API service instance.
#       user_id: User's email address. The special value "me"
#       can be used to indicate the authenticated user.
#       msg_id: The ID of the Message required.
#
#     Returns:
#       A MIME Message, consisting of data from Message.
#     """
#     try:
#         message = service.users().messages().get(userId=user_id, id=msg_id,
#                                                  format='raw').execute()
#         print('Message snippet: %s' % message['snippet'].encode('ASCII'))
#         MessageBody = []
#         msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
#         mime_msg = email.message_from_string(msg_str)
#         for parts in mime_msg.walk():
#             mime_msg.get_payload()
#             print(parts.get_content_type())
#             if parts.get_content_type() == 'application/xml':
#                 mytext = base64.urlsafe_b64decode(parts.get_payload().encode('UTF-8'))
#             if parts.get_content_type() == 'text/plain':
#                 myMSG = base64.urlsafe_b64decode(parts.get_payload().encode('UTF-8'))
#                 MessageBody.append(myMSG)
#                 with open('messages.json', 'w') as jsonfile:
#                     json.dump(MessageBody, jsonfile)
#
#     except errors.HttpError, error:
#         print ('An error occurred: %s' % error)
#     return mytext


def update_subject_content(content_subject):
    file = open("last_message.txt", "w")
    file.close()
    time.sleep(2)
    file = open("last_message.txt", "w")
    file.write(content_subject)
    file.close()

def update_message_content(msg):
    file = open("fill_content_message.txt",'w')
    file.close()
    time.sleep(1)
    file = open("fill_content_message.txt",'w')
    file.write(msg)

def clear_file(file_name):
    file = open(file_name,'w')
    file.close()
    time.sleep(1)
def get_before_subject():
    file = open("last_message.txt", "r")
    before_subject = file.read()
    file.close()
    return before_subject

def edit_content_message():
    clear_file("key.txt")
    filter = open("fill_content_message.txt").read().splitlines()
    parsing = False
    for line in filter:
        if line.startswith("Message Text =1B$B!'=1B(B"):
            parsing = True
        elif line.startswith("=1B$BHw9M!'=1B(B"):
            parsing = False
        if parsing:
            with open("key.txt", 'a') as mykey:
                mykey.write(line)
                mykey.write("\n")

    clear_file("key_2.txt")
    with open('key.txt') as infile, open("key_2.txt", 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue
            outfile.write(line)

    clear_file("key_3.txt")
    with open('key_2.txt') as f, open("key_3.txt", 'w') as outfile:
        outfile.write(" ".join(line.strip() for line in f))
    file = open('key_3.txt', 'r+')
    line = file.read()
    clear_file("key_4.txt")
    if 'ERR' in line and 'WARN' not in line:
        with open('key_4.txt', 'w') as ufile:
            # ufile.write('\n\nWARN [FX'.join(re.split('WARN\s\[FX', line)))
            ufile.write('\n\nERR [FX'.join(re.split('ERR\s\[FX', line)))

    if 'WARN' in line and 'ERR' not in line:
        with open('key_4.txt', 'w') as ufile:
            # ufile.write('\n\nWARN [FX'.join(re.split('WARN\s\[FX', line)))
            ufile.write('\n\nWARN [FX'.join(re.split('WARN\s\[FX', line)))

    if 'ERR' in line and 'WARN' in line:
        print 'Message content include both "WARN" and "ERR", please paste from your email !!!'

def add_content_to_ggsheet():
    sheet = gfile.open("Monitor Error").sheet1
    content = sheet.get_all_records()
    pp = pprint.PrettyPrinter()
    pp.pprint(content.__len__())
    # pp.pprint(content[964])
    # all_cells = sheet.acell('B966').value
    # sheet.update_cell(968,2,"ERR [FX0000001343] portalweb=1B$B$G%(%i!<$,H/@8$7$^$7$?!#=1B(B2018-07-17 10= :49:50,203, [http-nio-8087-exec-20] ERROR phn.com.nts.util.common.CommonUti= l Failed to copy full contents from '/opt/tomcat_backend/webapps/amsadmin/o= pt/tomcat/upload/6104518_GBG_20180717104950_1.pdf' to '/opt/tomcat/upload/r= kt/6104518_GBG_20180717104950_1.pdf'(/opt/tomcat_backend/logs/rktbe.log)")
    # print(all_cells)
    start_row = content.__len__() + 3
    # file handle fh
    fh = open('key_4.txt')
    while True:
        # read line
        line = fh.readline()
        sheet.update_cell(start_row, 2, line)
        start_row = start_row + 1
        # in python 2, print line
        # in python 3
        # print(line)
        # check if line is not empty
        if not line:
            break
    fh.close()


if __name__ == '__main__':
    list_messages = ListMessagesWithLabels(service, 'me', 'Label_26')
    id_last_message = list_messages[0]['id']
    current_message = GetMessage(service, 'me', id_last_message)
    content_message = GetMessageBody(service, 'me', id_last_message)
    reload(sys)
    sys.setdefaultencoding('utf-8')
    current_subject = str(current_message['payload']['headers'][38]['value'])
    # print str(content_message)
    before_subject = str(get_before_subject())
    update_message_content(content_message)
    edit_content_message()
    if os.stat("last_message.txt").st_size == 0:
        print "Please give subject to last_message.txt file"
    else:
        if current_subject == before_subject:
            print "We don't have new message"
        else:
            print "WARING...WE HAVE NEW MESSAGE IN RKT PROJECT"
            update_subject_content(current_subject)
            add_content_to_ggsheet()




        # print '\nERR [FX'.join(re.split('ERR\s\[FX', line))
    # clear_file("key_4.txt")
    # print '\nERR [FX'.join(re.split('ERR\s\[FX', line))

    # file = open("content_message.txt", "w")
    # file.write(content_message)
    # file.close()
    # byte_string = open("content_message.txt",'r').read()
    # unicode_text = byte_string.decode('UTF-8')
    # print(unicode)

    # help python can read special string encode utf8 japanese letter

    # write the first subject message to compare with after check
    # file = open("last_message.txt", "w")
    # file.write(current_subject)
    # file = open("last_message.txt", "r")
    # before_subject = file.read()
    # # print "The lasest subject %s" % before_subject
    # file.close()
    ################## send inform to Hipchat if have any new message ####################################

    # if os.stat("last_message.txt").st_size == 0:
    #     print "Please give subject to last_message.txt file"
    # else:
    #     if current_subject == before_subject:
    #         print "We don't have new message"
    #     else:
    #         print "WARING...WE HAVE NEW MESSAGE IN RKT PROJECT"
    #         update_subject_content(current_subject)
    ############################################################################################################
    # https://developers.google.com/gmail/api/v1/reference/users/messages
