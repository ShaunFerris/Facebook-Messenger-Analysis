'''UNDER CONSTRUCTION DOES NOT RUN'''

'''Main file for user interface. Will print a splashscreen in terminal, takefiles from users, merge if
neccessary, then take input on which stats to calculate using the FacebookChat class methods.
Can then send these stats to a seperate script where data visualisation will be calculated and exported to 
desired file system location.'''

import sys
import os
import shutil
import json
import emoji
from typing import TextIO, Any, List, Dict, AnyStr
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages
from facebookchat import FacebookChat as FB

def main():
    pass

def splash_screen():
    pass

def instantiate(json: TextIO):
    '''Create a FacebookChat object from supplied file.
    Should only ever recieve files post merge if merging is required.
    Merging will be handled by a different function.'''

    try:
        chat_object = FB(json)
    except:
        print("Please supply a valid .json Facebook Messenger log")
        sys.exit()
    return chat_object

def options_list(chat_object):
    '''Presents a list of options for desired stats which map to FacebookChat class methods,
    takes user input for which stats to get and prepares a list of ready to go methods.

    Args: 
        FacebookChat object passed from instantiate method

    Returns:
        A list of the desired methods to run which can then be invoked iteratively'''

    command_list = []
    OPTIONS = {
        1: chat_object.get_participants, 2: chat_object.get_number_days,
        3: chat_object.total_interactions, 4: chat_object.number_of_texts,
        5: chat_object.common_words, 6: chat_object.voice_calls_analysis,
        7: chat_object.video_calls_analysis, 8: chat_object.av_txts_per_day,
        9: chat_object.av_words_per_text
        }
    OPTIONS_TO_PRINT = '''
        1: Chat participants, 2: Conversation length (days),
        3: Total interactions, 4: Number of text messages,
        5: Common words, 6: Voice call stats,
        7: Video call stats, 8: Texts per day,
        9: Words per text
        '''
    print(
        f'Which statistics would you like from the supplied chat log? \n {OPTIONS_TO_PRINT}'
        f'\n (Enter the option codes, eg: 174)'
        )
    chosen = str(input('>>'))
    for i in range(10):
        if str(i) in chosen:
            command_list.append(OPTIONS[i])
    return command_list
    
def export_stats(command_list: List) -> Dict[AnyStr, Any]:
    '''Function to call the list of desired FacebookChat class methods provided
    by the options list function, then export their results.
    
    Returns a dict of calculated stats keyed with the __name__ of function called.'''

    results = {f.__name__: f() for f in command_list}
    return results

def command_line_stats_output(command_list):
    #Participants
    pass

def border(display_chr: AnyStr='#') -> AnyStr:
    '''Incomplete.
    Function to draw a border of characters around the terminal.
    Will be used for the splash screen function.'''
    #Clear terminal of existing ouputs
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    display_matrix = init_display_control()
    display_matrix[0][:], display_matrix[-1][:] = display_chr, display_chr

def init_display_control():
    '''NOTE: Unsure if this will be used.
    Get terminal dimensions and initialise a matrix representing output "pixels" 
    
    Returns a matrix containing 0s as ints. 
    Each 0 represents one chr space on the terminal window when the function was called'''

    DISPLAY_WIDTH, DISPLAY_HEIGHT = \
    shutil.get_terminal_size()[0], shutil.get_terminal_size()[1]
    display_matrix = [0] * DISPLAY_HEIGHT
    for i in range(DISPLAY_HEIGHT):
        display_matrix[i] = [0] * DISPLAY_WIDTH
    return display_matrix

if __name__ == '__main__':
    selected = export_stats((options_list(instantiate(\
        ''))))
    print(selected)