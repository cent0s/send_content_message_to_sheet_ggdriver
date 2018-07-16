import gspread
import json
import pprint
import time
import re
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope) # get email and key from creds


gfile = gspread.authorize(credentials) # authenticate with Google

sheet = gfile.open("Monitor Error").sheet1
content = sheet.get_all_records()
pp = pprint.PrettyPrinter()
pp.pprint(content.__len__())
pp.pprint(content[848])



# def update_message_send_to_sheet(new_content):
#     file = open("send_sheet.txt", "w")
#     file.close()
#     time.sleep(1)
#     file = open("send_sheet.txt", "w")
#     file.write(new_content)
#     file.close()
def clear_file(file_name):
    file = open(file_name,'w')
    file.close()
    time.sleep(1)


if __name__ == '__main__':
    clear_file("key.txt")
    filter = open('fill_content_message.txt').read().splitlines()
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

    with open('key.txt') as infile, open("key_2.txt",'w') as outfile:
        clear_file("key_2.txt")
        for line in infile:
            if not line.strip():
                continue
            outfile.write(line)

    with open('key_2.txt') as f, open("key_3.txt",'w') as outfile:
        clear_file("key_3.txt")
        outfile.write(" ".join(line.strip() for line in f))
    file = open('key_3.txt','r+')
    line = file.read()
    clear_file("key_4.txt")
    print '\nERR [FX'.join(re.split('ERR\s\[FX', line))

    # with open('key_4.txt','w') as ufile:
    #     ufile.write('\n\nWARN [FX'.join(re.split('WARN\s\[FX', line)))

    # print '\nWARN [FX'.join(re.split('WARN\s\[FX', line))
    # Keyword "use re  python add new line before string"
    # https: // stackoverflow.com / questions / 45039268 / to - add - a - new - line - before - a - set - of - characters - in -a - line - using - python



    # List some error can have when setup
# https://github.com/burnash/gspread/issues/513
