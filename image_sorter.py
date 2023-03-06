'''NOTE: This module is not yet feature complete, it is in active development.

This script is intended for sorting the images associated with a facebook 
messenger conversation.'''

import os 
import datetime
from facebookchat import FacebookChat as FB

test_chat = FB('/home/shaun/Documents/coding-projects/Facebook Data Analysis/essie_merged_messagesV2.json')

def get_photo_info(chat_json):
    '''Takes as an arg the path to the chat json of interest.
    Initializes the chat as an instance of the FacebookChat class and
    uses the photos_by_sender method to organize the photo file names by
    who sent them and when.'''

    chat_object = FB(chat_json)
    return chat_object.photos_by_sender()

def make_file_structure(start_year, end_year, title):
    '''Creates a file structure on the users desktop. The outer folder is 
    named 'photos from facebook chat between {participants}' and it contains 
    one folder per year of the chats duration with monthly folders inside.
    To be used for storing the files in sorted containers.
    Takes the chat object as an arg.'''
    
    #Get path to desktop and create photos folder if it doesn't already exist
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    photos_path = os.path.join(desktop_path, f'photos_from_facebook_chat_{title}')
    if not os.path.exists(photos_path):
        os.mkdir(photos_path)
    #Make a folder for each year in the range
    for year in range(start_year, end_year + 1):
        year_folder = os.path.join(photos_path, str(year))
        if not os.path.exists(year_folder):
            os.mkdir(year_folder)
        #Create monthly photos folders for each year
        for month in range(1, 13):
            month_name = datetime.date(year, month, 1).strftime('%B')
            month_folder = os.path.join(year_folder, month_name)
            if not os.path.exists(month_folder):
                os.mkdir(month_folder)
    
    
