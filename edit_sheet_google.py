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
# pp.pprint(content[964])
# all_cells = sheet.acell('B966').value
#sheet.update_cell(968,2,"ERR [FX0000001343] portalweb=1B$B$G%(%i!<$,H/@8$7$^$7$?!#=1B(B2018-07-17 10= :49:50,203, [http-nio-8087-exec-20] ERROR phn.com.nts.util.common.CommonUti= l Failed to copy full contents from '/opt/tomcat_backend/webapps/amsadmin/o= pt/tomcat/upload/6104518_GBG_20180717104950_1.pdf' to '/opt/tomcat/upload/r= kt/6104518_GBG_20180717104950_1.pdf'(/opt/tomcat_backend/logs/rktbe.log)")
# print(all_cells)
start_row = content.__len__() + 3
# file handle fh
fh = open('key_4.txt')
while True:
    # read line
    line = fh.readline()
    sheet.update_cell(start_row,2,line)
    start_row = start_row + 1
    # in python 2, print line
    # in python 3
    # print(line)
    # check if line is not empty
    if not line:
        break
fh.close()






# def update_message_send_to_sheet(new_content):
#     file = open("send_sheet.txt", "w")
#     file.close()
#     time.sleep(1)
#     file = open("send_sheet.txt", "w")
#     file.write(new_content)
#     file.close()
# def clear_file(file_name):
#     file = open(file_name,'w')
#     file.close()
#     time.sleep(1)


# if __name__ == '__main__':
    ################ Edit message content to file ##############################
    # clear_file("key.txt")
    # filter = open('fill_content_message.txt').read().splitlines()
    # parsing = False
    # for line in filter:
    #     if line.startswith("Message Text =1B$B!'=1B(B"):
    #         parsing = True
    #     elif line.startswith("=1B$BHw9M!'=1B(B"):
    #         parsing = False
    #     if parsing:
    #         with open("key.txt", 'a') as mykey:
    #             mykey.write(line)
    #             mykey.write("\n")
    #
    # with open('key.txt') as infile, open("key_2.txt",'w') as outfile:
    #     clear_file("key_2.txt")
    #     for line in infile:
    #         if not line.strip():
    #             continue
    #         outfile.write(line)
    #
    # with open('key_2.txt') as f, open("key_3.txt",'w') as outfile:
    #     clear_file("key_3.txt")
    #     outfile.write(" ".join(line.strip() for line in f))
    # file = open('key_3.txt','r+')
    # line = file.read()
    # if 'ERR' in line and 'WARN' not in line:
    #     print '\nERR [FX'.join(re.split('ERR\s\[FX', line))
    #
    # if 'ERR' not in line and 'WARN' in line:
    #     print '\n\nWARN [FX'.join(re.split('WARN\s\[FX', line))
    #
    # if 'ERR' in line and 'WARN' in line:
    #     print 'Message content include both "WARN" and "ERR", please paste from your email !!!'
    ################ Edit message content to file ##############################

    # with open('key_4.txt','w') as ufile:
    #     ufile.write('\n\nWARN [FX'.join(re.split('WARN\s\[FX', line)))

    # print '\nWARN [FX'.join(re.split('WARN\s\[FX', line))
    # Keyword "use re  python add new line before string"
    # https: // stackoverflow.com / questions / 45039268 / to - add - a - new - line - before - a - set - of - characters - in -a - line - using - python



    # List some error can have when setup
# https://github.com/burnash/gspread/issues/513
