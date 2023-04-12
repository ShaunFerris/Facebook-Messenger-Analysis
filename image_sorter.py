'''NOTE: This module is not yet feature complete, it is in active development.

This script is intended for sorting the images associated with a facebook 
messenger conversation.'''

import os
import shutil
import datetime
from facebookchat import FacebookChat as FB

test_chat = FB('/home/shaun/Documents/coding-projects/Facebook Data Analysis/essie_merged_messagesV2.json')

def get_image_info(chat_json):
    '''
    Takes as an arg the path to the chat json of interest.
    Initializes the chat as an instance of the FacebookChat class and
    uses the photos_by_sender method to organize the photo file names by
    who sent them and when.
    '''
    chat_object = FB(chat_json)
    return chat_object.images_by_sender()

def make_file_structure(start_year, end_year, title):
    '''
    Creates a file structure on the users desktop. The outer folder is 
    named 'photos from facebook chat between {participants}' and it contains 
    one folder per year of the chats duration with monthly folders inside.
    To be used for storing the files in sorted containers.
    Takes the chat object as an arg.
    '''
    #Get path to desktop and create photos folder if it doesn't already exist
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    images_path = os.path.join(desktop_path, f'photos_from_facebook_chat_{title}')
    if not os.path.exists(images_path):
        os.mkdir(images_path)
    #Make a folder for each year in the range
    for year in range(start_year, end_year + 1):
        year_folder = os.path.join(images_path, str(year))
        if not os.path.exists(year_folder):
            os.mkdir(year_folder)
        #Create monthly photos folders for each year
        for month in range(1, 13):
            month_name = datetime.date(year, month, 1).strftime('%B')
            month_folder = os.path.join(year_folder, month_name)
            if not os.path.exists(month_folder):
                os.mkdir(month_folder)
    
def sort_pictures(unsorted, destination_file_struct, images_by_sender):
    '''
    Moves the images from the 'photos' folder in the chat data directory
    to a newly created file structure organising them by month of the year sent
    and sender.
    
    Args: 
        unsorted: Path to 'photos' folder.

        destination_file_struct: Path to the top-level directory of a file structure
        made with the make_file_structure function.
        
        images_by_sender: The dictionary made by the images_by_sender function of a
        FacebookChat class instance.
        '''
    for sender_name, images in images_by_sender.items():
        for image in images:
            sent_date = image.keys()[0]
            file_name = image.values()[0]
            year, month, day = sent_date.split('-')
            year_folder = os.path.join(destination_file_struct, year)
            month_name = sent_date.split('-')[1]
            month_folder = os.path.join(year_folder, month_name)
            src_path = os.path.join(unsorted, file_name)
            dst_name = sender_name + file_name
            # Append sender name to the file name to keep track of who sent what
            dst_path = os.path.join(month_folder, dst_name)
            if not os.path.exists(month_folder):
                os.makedirs(month_folder)
            shutil.move(src_path, dst_path)

def main():
    '''
    Main loop for running the photo sorting functions as a standalone
    CLI based applications. Prompts the user for file locations and names
    that the preceeding methods use.
    '''
    pass

    

if __name__ == '__main__':
    main()