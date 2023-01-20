#Badly coded slapdash attempt at merging the 3 json files of chat logs with Es from facebook data dump

import json

msg_data1 = json.load(open('/home/shaun/Documents/Coding Projects/Facebook Data Analysis/essiepreddey_10156928597205650/message_1.json'))
msg_data2 = json.load(open('/home/shaun/Documents/Coding Projects/Facebook Data Analysis/essiepreddey_10156928597205650/message_2.json'))
msg_data3 = json.load(open('/home/shaun/Documents/Coding Projects/Facebook Data Analysis/essiepreddey_10156928597205650/message_3.json'))

msgs1 = msg_data1['messages']
msgs2 = msg_data2['messages']
msgs3 = msg_data3['messages']

msgs1.extend(msgs2)
msgs1.extend(msgs3)

merged_msgs = msgs1

with open('merged_messages.json', 'x') as outfile:#if starting from scratch again, change w arg to x to create new json file
    json.dump(merged_msgs, outfile, indent=2)

'''TODO: re-write this to be more widely applicable to other users/other chat logs, and to not omit the participants section
at the top of the chat log from the final ,merged file'''
