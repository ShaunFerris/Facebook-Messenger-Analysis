'''Small utility script for merging multiple .json files from the same messenger conversation into one for analysis
by message analysis.py'''

import json

print('how many files do you want to merge?')
num_files_to_merge = int(input('>>'))
files_to_merge = {n: 0 for n in range(1, num_files_to_merge + 1)}
for n in files_to_merge:
    print('Input file...')
    files_to_merge[n] = input('>>')

#add latest timestamp to data so they can be stitched in the right order
for n, f in files_to_merge.items():
    file = json.load(open(f))
    files_to_merge[n] =(f, file['messages'][0]['timestamp_ms'])
#Set the order to stitch files by index in a list
files_to_merge = sorted(files_to_merge.values(), key=lambda x:x[1], reverse=True)

output = json.load(open(files_to_merge[0][0]))
count = 0
for tup in files_to_merge:
    count += 1
    if count == 1:
        continue
    data = json.load(open(tup[0]))
    output['messages'].extend(data['messages'])

print('Enter name for merged file')
out_name = input('>>')

with open(out_name, 'x') as outfile:
    json.dump(output, outfile, indent=2)