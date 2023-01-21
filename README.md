# Facebook-Messenger-Analysis

This repository contains two tools written in python for processing Facebook Messenger chats, a message merge tool, and an analysis module.

The message merge tool is used to combine multiple .json files for one conversation into a single file, while preserving the json schema and non-message meta data.

The analysis module provides a FacebookChat class, to be initialised with the json file from a chat of interest. The class implements methods for pulling useful data and statistics from the chat record.

This project is an active work in progress as of 21/01/2023.

Dependencies:
  emoji v2.2.0
