#UNDER CONSTRUCTION

'''Main file for user interface. Will print a splashscreen in terminal, takefiles from users, merge if
neccessary, then take input on which stats to calculate using the FacebookChat class methods.
Can then send these stats to a seperate script where data visualisation will be calculated and exported to 
desired file system location.'''

#TODO: Implement search mode, implement top emoji, bug-fix video-chats

import sys
import os
import shutil
import emoji
from typing import TextIO, Any
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages
from facebookchat import FacebookChat as FB
from message_merge import acquire_and_merge

def main():
    pass

def splash_screen(border_char: str='#'):
    '''UNDER CONSTRUCTION
    Clear all current terminal display and display a splash screen
    with application title and copyright info.'''

    DISPLAY_STR_1 = 'FACEBOOK MESSENGER ANALYSIS UTILITY'
    DISPLAY_STR_2 = 'Copyright Shaun Ferris 2023'
    #Clear terminal
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    #Set display dimensions
    DISPLAY_WIDTH, DISPLAY_HEIGHT = \
    shutil.get_terminal_size()[0], shutil.get_terminal_size()[1]
    display_str = ''
    working_space_vert = DISPLAY_HEIGHT - 4
    working_space_hor = DISPLAY_WIDTH - 2
    head = (working_space_vert - 2) // 2
    lead_1 = (working_space_hor - len(DISPLAY_STR_1)) // 2
    lead_2 = (working_space_hor - len(DISPLAY_STR_2)) // 2
    display_str += border_char * DISPLAY_WIDTH + '\n'\
        + ((border_char + (' ' * working_space_hor) + border_char + '\n') * head)\
        + (border_char + (' ' * lead_1) + DISPLAY_STR_1 + (' ' * lead_1) + border_char) + '\n'\
        + (border_char + (' ' * lead_2) + DISPLAY_STR_2 + (' ' * lead_2) + border_char) + '\n'\
        + ((border_char + (' ' * working_space_hor) + border_char + '\n')* head)\
        + border_char * DISPLAY_WIDTH
    print(display_str)



def instantiate(json: TextIO):
    '''Create a FacebookChat object from supplied file.
    Should only ever recieve files post merge if merging is required.
    Merging will be handled by the file accept dialogue function.'''

    try:
        chat_object = FB(json)
    except:
        print("Please supply a valid .json Facebook Messenger log")
        sys.exit()
    return chat_object

def file_accept_dialogue():
    '''Presents the user with a choice of submitting one or more files.
    If one file is submitted, it is instantiated, if more than one,
    they are merged and then instantiated.
    
    Returns the instantiated facebookchat object.'''

    print('Do you need to merge files for your chat log? (y / n)') #consider adding some exception catching
    mode = input('>> ')
    if mode == 'y':
        file_path = acquire_and_merge()
    elif mode == 'n':
        print('Enter path to file: ')
        file_path = input('>> ')
    return instantiate(file_path)

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
    chosen = str(input('>> '))
    for i in range(10):
        if str(i) in chosen:
            command_list.append(OPTIONS[i])
    return command_list
    
def export_stats(command_list: list) -> dict[str, Any]:
    '''Function to call the list of desired FacebookChat class methods provided
    by the options list function, then export their results.
    
    Returns a dict of calculated stats keyed with the __name__ of function called.'''

    exported_stats = {f.__name__: f() for f in command_list}
    return exported_stats

def command_line_stats_output(exported_stats: dict):
    '''Main flow control loop for returning the desired stats as readable strings.
    Takes the exported stats dict from the export stats command, and formats the
    data into a string that corresponds to the function that produced it.
    
    Prints these strings to the terminal.'''

    for func_name, output in exported_stats.items():
        if func_name == 'get_participants':
            print(f'The chat participants were: ', end='')
            #Allow for formatting of any number of participant names
            for i in output:
                if i != output[-1] and i != output[-2]:
                    print(f'{i}, ', end='')
                elif i == output[-2]:
                    print(f'{i} ', end='')
                else:
                    print(f'and {i}.')
        elif func_name == 'get_number_days':
            print(f'The chat spanned {output} days.')
        elif func_name == 'total_interactions':
            print(f'The chat encompassed {output} interactions.')
        elif func_name == 'number_of_texts':
            for i in output[1]:
                print(f'{i[0]} sent {i[1]} texts')
            print(f'There were a total of {output[0]} texts sent.')
        elif func_name == 'common_words':
            for party, word_list in output.items():
                print(f'{party}\'s most common words were: \n {word_list}')
        elif func_name == 'voice_calls_analysis':
            for party, calls in output[0].items():
                print(f'{party} initiated {calls} voice calls.')
            print(f'There were a total of {output[1]} minutes of voice call.')
        elif func_name == 'video_calls_analysis':
            for party, calls in output[0].items():
                print(f'{party} initiated {calls} video calls.')
            print(f'There were a total of {output[1]} minutes of video call.')
        elif func_name == 'av_txts_per_day':
            print(f'On average, {output} text messages were sent every day.')
        elif func_name == 'av_words_per_text':
            for party, words in output.items():
                print(f'The average text sent by {party} contained {words} words.')

def section_header(display_text: str='Default', border_chr: str='#'):
    '''Wraps a border made up of border_chrs around a display_text.
    Returns the three strings that make up the bordered text.'''
    
    header_width = len(display_text) + 6
    top_line = (border_chr * header_width) + '\n'
    mid_line = f'{border_chr}  {display_text}  {border_chr}\n'
    bottom_line = (border_chr * header_width) + '\n'
    return top_line, mid_line, bottom_line


if __name__ == '__main__':
    selected = export_stats((options_list(file_accept_dialogue())))
    command_line_stats_output(selected)