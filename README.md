# Facebook-Messenger-Analysis
This project is an active work in progress as of 05/03/2023.

This repository contains tools written in python for processing Facebook Messenger chats and extracting useful statistics from them. In order to use these tools you will need the .json files pertaining to a messnger chat of interest. 
Information on how to request these files for messenger chats involving your facebook account can be found here: https://www.facebook.com/help/212802592074644 (make sure to choose .json as the format)

## Intallation and requirements
These scripts require python 3.8+, an up to date pip for managing packages, and the packages listed in the provided 'requirements.txt' file. Install python following the instructions for your operating system at: https://www.python.org/

Clone this repository with the command ```git clone <clone address>``` in terminal.

Then you can install dependencies by running ```pip install -r requirements.txt```

## Module files
### messenger_analysis_interface.py
The main file for the suite of tools, this script provides functionality to take a selection of desired statistics from the user and return a report in command line or as a txt file. This script requires both message_merge.py and facebookchat.py as dependencies.

### message_merge.py
For some large chats, the chat data will be provided as multiple .json files. The message merge tool is used to combine multiple .json files for one conversation into a single file while preserving the json schema and non-message meta-data. It can be run as a standalone, in which case it will walk the user through pointing it to files and naming the output, or the main function can be imported to another script to act as part of a larger workflow.

### facebookchat.py
The facebook chat module provides a FacebookChat class, to be initialised with the json file from a chat of interest. The class implements methods for pulling useful data and statistics from the chat record.
Currently users will need to use the methods in this class in their own script to retrieve the statistics.

### Under construction module: image_sorter.py
This script will accept a path to a chat record, and a path to the photos folder associated with the chat, then sort those photos into a new file structure organised by which chat participant sent them grouped by month of the year. 

## Usage of main file: messenger_analysis_interface.py
In the current verision running this module will initiate the mode select dialogue. Currently only the CLI stats and search modes have been implemented. The user will be prompted as to whether they need to merge their files before beginning, and will then be prompted to supply one or more file paths. It is reccomended to simply copy and paste the file paths into the terminal. If the files are not in the same directory as the scripts, supply the full file path, otherwise just the file name will suffice. If a merged file is created it will be created in the working directory. Functionality to export it directly to another directory may be added in future.

Functionality for a third mode in which a pdf report of plotted chat stats will be generated is underway.