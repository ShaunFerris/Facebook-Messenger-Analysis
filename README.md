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

Under active construction, this script provides functionality to take a selection of desired statistics from the user and return a report in command line. This script requires both message_merge.py and facebookchat.py as dependencies.

### Usage of messenger_analysis_iterface.py

In the current verision running this module will initiate the file select dialouge. The user will be prompted as to wether they need to merge their files before beginning, and will then be prompted to supply one or more file paths. If the files are not in the same directory as the scripts, supply the full file path, otherwise just the file name will suffice. If a merged file is created it will be created in the working directory. Functionality to export it directly to another directory may be added in future.

Next the user will be prompted to select from a list the stats they wish to extract from the chat record, and the results will be displayed as readable scentences in the terminal window.

Functionality to export the stats as a text file and create graphical visualisations of the stats is intended for future updates.