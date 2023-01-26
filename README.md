# Facebook-Messenger-Analysis

This project is an active work in progress as of 21/01/2023.

This repository contains tools written in python for processing Facebook Messenger chats and extracting useful statistics from them. In order to use these tools you will need the .json files pertaining to a messnger chat of interest. 
Information on how to request these files for messenger chats involving your facebook account can be found here: https://www.facebook.com/help/212802592074644 (make sure to choose .json as the format)

## message_merge.py

For some large chats, the chat data will be provided as multiple .json files. The message merge tool is used to combine multiple .json files for one conversation into a single file while preserving the json schema and non-message meta-data. It can be run as a standalone, in which case it will walk the user through pointing it to files and naming the output, or the main function can be imported to another script to act as part of a larger workflow.

## facebookchat.py

The facebook chat module provides a FacebookChat class, to be initialised with the json file from a chat of interest. The class implements methods for pulling useful data and statistics from the chat record.
Currently users will need to use the methods in this class in their own script to retrieve the statistics.

## messenger_analysis_interface.py

Under active construction, this script provides functionality to take a selection of desired statistics from the user and return a report.