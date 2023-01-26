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
from typing import TextIO, Any
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
    
def export_stats(command_list: list) -> dict[str, Any]:
    '''Function to call the list of desired FacebookChat class methods provided
    by the options list function, then export their results.
    
    Returns a dict of calculated stats keyed with the __name__ of function called.'''

    exported_stats = {f.__name__: f() for f in command_list}
    return exported_stats

def command_line_stats_output(exported_stats):
    for func_name, output in exported_stats.items():
        if func_name == 'get_participants':
            print(f'The chat participants were: ', end='')
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


if __name__ == '__main__':
    selected = export_stats((options_list(instantiate(\
        '/home/shaun/Documents/Coding Projects/Facebook Data Analysis/merged_messagesV2.json'))))
    
    command_line_stats_output(selected)