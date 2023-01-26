'''Small utility script for merging multiple .json files from the same messenger conversation into one for analysis.
The script can be run stand-alone to prompt the user through the process of merging files, or the functionality
can be imported, allowing automation or other applications.'''

import json
from time import sleep

def fb_chat_merge(files_to_merge: list, outfile_name: str='unnamed_merged_messages'):
    '''The function to import to apply the file merge functionality
    in other scripts. Takes a list containing the paths to files,
    and a name to give the completed file.
    
    Returns one merged .json file, in the schema used by facebook.'''

    files_to_merge = {n + 1: f for n, f in enumerate(files_to_merge)}
    #Add latest timestamp to data so they can be stitched in the right order
    for n, f in files_to_merge.items():
        file = json.load(open(f))
        files_to_merge[n] = (f, file['messages'][0]['timestamp_ms'])
    #Set the order to stitch files by index in a list
    files_to_merge = sorted(files_to_merge.values(), key=lambda x:x[1], reverse=True)
    #Set latest fragment as top of file
    output = json.load(open(files_to_merge[0][0]))
    count = 0
    for tup in files_to_merge:
        count += 1
        if count == 1:
            continue
        data = json.load(open(tup[0]))
        output['messages'].extend(data['messages'])

    with open(outfile_name, 'x') as outfile:
        json.dump(output, outfile, indent=2)

if __name__ == '__main__':
    file_list = []
    print('How many files would you like to merge?')
    num_files_to_merge = input('>> ')
    for i in range(1, num_files_to_merge + 1):
        print('Enter path to file: ')
        file_list.append(input('>> '))
    print('What would you like the merged file to be called?')
    outfile_name = input('>> ')
    fb_chat_merge(file_list, outfile_name)
    sleep(0.5)
    print('File created.')