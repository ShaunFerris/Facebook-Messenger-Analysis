'''This is a refactor of a previous script for analysing facebook messenger logs.
This iteration implements a facebook-chat class to process the .json logs and includes methods to call stats from the record.

Inspiration and pointers for this project came from this git repo:
https://github.com/davidkrantz/FacebookChatStatistics/blob/master/facebook_messenger_conversation.py
by David Krantz, but I am writing this code for myself as a learning exercise.
Additionaly, my implementation will treat voice, video and text messages as different entities,
allowing stats on the different categories to be more easily pulled with in class methods.'''

import json
import emoji
from typing import TextIO
from collections import Counter
from copy import deepcopy
from datetime import datetime

class FacebookChat():
    '''A module for processing and retrieving relvent data from the JSON records of a messenger conversation.
    
    Attributes:
        chat_contents (list): List of dicts, each dict representing one message/call
        participants (list): List of conversation participants
        title (str): Title of the conversation'''

    def __init__(self, chat_file: TextIO):
        '''Parses the JSON, separates the participant data and the 
        message contents, and decodes UTF escape characters like emoji in the text contents
        
        Args: 
        chat_file(.json):JSON chat-log in the format provided by facebook. 
        NOTE: some large chats are provided in multiple JSON files,
        these muct be merged first to get accuarate data of the whole chat'''

        #read the .json file and set the class attributes
        with open(chat_file, 'r') as f:
            self.chat_data = json.load(f)

        self.chat_contents = self.chat_data['messages']
        self.title = self.chat_data['title']
        self.participants = []
        for party in self.chat_data['participants']:
            self.participants.append(party['name'])

        #decode relevant text data
        for p in self.participants:
            p = p.encode('raw_unicode_escape').decode('utf-8')
        for msg in self.chat_contents:
            msg['sender_name'] = msg['sender_name'].encode('raw_unicode_escape').decode('utf-8')
            if 'content' in msg:
                msg['content'] = msg['content'].encode('raw_unicode_escape').decode('utf-8')

    def __str__(self):
        '''Allow a facebookchat object to be printed, returning it's title
        and the participants.'''

        return f'Facebook Chat titled {self.title} including {str(self.participants)}.'
        
    def get_participants(self) -> list:
        '''Returns a list of participant names'''

        return self.participants

    def total_interactions(self) -> int:
        '''Returns the total number of interactions between participants,
        including texts, voice calls and video calls'''

        return len(self.chat_contents)

    def txts_by_party(self) -> dict[str, list]:
        '''Sort the messages containing text content by sender.
        
        Returns a dict of format sender_name:[messages].'''

        txts = {party: [] for party in self.participants}
        for msg in self.chat_contents:
            if 'call_duration' not in msg and 'content' in msg:
                txt_list = txts.get(msg['sender_name'])
                txt_list.append(msg['content'])
        return txts

    def number_of_texts(self) -> tuple[int, list[tuple[str, int]]]:
        '''Returns the overall total number of texts sent, and
        the number of texts sent by each chat participant.
        Returns the total as an int, and the breakdown as a list containing 
        tuples: (name (str), number of msgs (int))'''
        
        txts = self.txts_by_party()
        txt_counts = []
        total = 0
        for name, msgs in txts.items():
            txt_counts.append((name, len(msgs)))
        for i in txt_counts:
            total += i[1]
        return total, txt_counts

    def words_in_txts(self) -> dict[str, list[str]]:
        '''Takes the sorted texts by participant and splits each message into individual words.
        Adds these words to a list of all words used by participants in all their messages.
        
        Returns a dict of format name: list of words'''

        txts = self.txts_by_party()
        words_by_party = {party: [] for party in self.participants}
        for name, msgs in txts.items():
            for msg in msgs:
                words = msg.split()
                for word in words:
                    word_list = words_by_party.get(name)
                    word_list.append(word.lower())
        return words_by_party

    def number_of_words(self) -> tuple[int, dict[str, int]]:#TODO test this function
        '''Counts all words sent by all parties
        
        Returns total words in chat, number sent by each participant'''

        words_by_party = self.words_in_txts()
        word_count_by_party = {p: len(w) for p, w in words_by_party.items()}
        total_word_count = 0
        for c in word_count_by_party.values():
            total_word_count += c
        return total_word_count, word_count_by_party

    def common_words(self, number: int = 10) -> dict[str, list[tuple[str, int]]]:
        ''''Takes the words list for each participant and counts the most common.
        
        Args: 
            number(int): The number of most common words to return, eg: 100 most common.
            defaults to 10.
            
        Returns a dictionary of format name: n most common words used'''

        words_by_party = self.words_in_txts()
        top_words = {party: [] for party in self.participants}
        for name, words in words_by_party.items():
            p_counter = Counter(words)
            top_words[name] = p_counter.most_common(number)
        return top_words

    def message_search(self, search_term: str) -> dict[str, int]:
        '''Searches for the input search term in every text message
        in the chat. 
        
        Returns the number of times the search term appeared in messages
        sent by each of the participants.'''
        
        results = {}
        messages = self.chat_contents
        for message in messages:
            if 'call_duration' not in message and 'content' in message:
                if search_term in message['content']:
                    results[message['sender_name']] = results.get(message['sender_name'], 0) + 1
        return results

    def voice_calls_analysis(self) -> tuple[dict[str, int], int]:
        '''Counts the number and duration of voice calls made between parites in the chat
        
        Returns:
            voice_calls_by_party(dict): which participant made how many calls
            total_duration(int): duration in minutes of voice calls between all parties'''
            
        voice_calls_by_party = {party: 0 for party in self.participants}
        total_duration = 0
        for msg in self.chat_contents:
            if 'call_duration' in msg\
            and msg['content'] != 'The video chat ended.':
                voice_calls_by_party[msg['sender_name']] += 1
                total_duration += msg['call_duration']
        total_duration = total_duration // 60
        return voice_calls_by_party, total_duration

    def video_calls_analysis(self) -> tuple[dict[str, int], int]:
        '''Counts the number and duration of video calls made between parites in the chat
        
        Returns:
            video_calls_by_party(dict): which participant made how many calls
            total_duration(int): duration in minutes of video calls between all parties'''

        video_calls_by_party = {party: 0 for party in self.participants}
        total_call_duration = 0
        for msg in self.chat_contents:
            if 'call_duration' in msg\
            and msg['content'] == 'The video chat ended.':
                video_calls_by_party[msg['sender_name']] += 1
                total_call_duration += msg['call_duration']
        total_call_duration = total_call_duration // 60
        return video_calls_by_party, total_call_duration

    def emoji_by_party(self) -> dict[str, list[tuple[str, int]]]:
        '''Checks message from each sender for emoji, notes which users sent which
        emoji and how many times in total.
        
        Returns a dict of participants:emojis sent'''

        emojis = {e: 0 for e in emoji.EMOJI_DATA.keys()}
        emojis_by_party = {party: deepcopy(emojis) for party in self.participants}
        words_by_party = self.words_in_txts()
        for party in emojis_by_party:
            number_of_words = len(words_by_party[party])
            to_search = self.common_words(number=number_of_words)[party]
            for tup in to_search:
                if emoji.is_emoji(tup[0]) == True:
                    emojis_by_party[party][tup[0]] += tup[1]
            emojis_by_party[party] = \
                {emoji.emojize(emoji.demojize(e)): c for e, c in emojis_by_party[party].items() if c}
            emojis_by_party[party] = \
                sorted(emojis_by_party[party].items(), key=lambda x:x[1], reverse=True)
        return emojis_by_party

    def get_time_interval(self, output: str = 'str') -> tuple:
        '''Gets the start and end timestamps of the messages
        
        Returns the start and end times converted to desired format'''
        
        start = datetime.fromtimestamp(self.chat_contents[-1]['timestamp_ms']/1000)
        end = datetime.fromtimestamp(self.chat_contents[0]['timestamp_ms']/1000)
        if output == 'datetime':
            return start, end
        elif output == 'str':
            return start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError('Type not supported. Must be either datetime or str.')

    def get_number_days(self) -> int:
        '''Calculates the number of days between first and last messages
        
        Returns the number of days as an int'''

        start, end = self.get_time_interval('datetime')
        return (end - start).days + 1

    def av_words_per_text(self) -> dict[str, int]:
        '''Gets the average words per text message for each party'''

        words = self.number_of_words()[1]
        words_per_text = {p: w // self.get_number_days() for p, w in words.items()}
        return words_per_text

    def av_txts_per_day(self) -> int:
        '''Gets the average number of text messages sent per day'''
        
        return int(self.number_of_texts()[0] / self.get_number_days())