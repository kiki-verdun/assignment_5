import csv
import json
import requests

# for later, when working with local files
import glob
import os
from os.path import join

endpoint = 'https://www.loc.gov/free-to-use'
parameters = {
    'fo' : 'json'
}

collection = 'libraries'

collection_list_response = requests.get(endpoint + '/' + collection, params=parameters)

collection_list_response.url

collection_json = collection_list_response.json()

# .keys() is a helpful function to see what the data elements are
collection_json.keys()

for k in collection_json['content']['set']['items']:
    print(k)

len(collection_json['content']['set']['items'])

collection_json['content']['set']['items'][0].keys()

collection_set_list = os.path.join('data','collection_set_list.csv')
headers = ['image','link','title', 'alt']

with open(collection_set_list, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for item in collection_json['content']['set']['items']:
        
        # clean up errant spaces in the title fields
        item['title'] = item['title'].rstrip()
        writer.writerow(item)
    print('wrote',collection_set_list)

# update endpoint info
endpoint = 'https://www.loc.gov'
parameters = {
    'fo' : 'json'
}

# run this cell to confirm that you have a location for the JSON files
item_metadata_directory = os.path.join('data','ftu_libs_metadata')

if os.path.isdir(item_metadata_directory):
    print(item_metadata_directory,'exists')
else:
    os.mkdir(item_metadata_directory)
    print('created',item_metadata_directory)

item_count = 0
error_count = 0
file_count = 0

data_directory = 'data'
item_metadata_directory = 'ftu_libs_metadata'
item_metadata_file_start = 'item_metadata'
json_suffix = '.json'

collection_set_list = os.path.join('data','collection_set_list.csv')

with open(collection_set_list, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f, fieldnames=headers)
    for item in reader:
        if item['link'] == 'link':
            continue
        # these resource links could redirect to item pages, but currently don't work
        if '?' in item['link']:
            resource_ID = item['link']
            short_ID = item['link'].split('/')[2]
            item_metadata = requests.get(endpoint + resource_ID + '&fo=json')
            print('requested',item_metadata.url,item_metadata.status_code)
            if item_metadata.status_code != 200:
                print('requested',item_metadata.url,item_metadata.status_code)
                error_count += 1
                continue
            try:
                item_metadata.json()
            except: #basically this catches all of the highsmith photos with hhh in the ID
                error_count += 1
                print('no json found')
                continue
            fout = os.path.join(data_directory, item_metadata_directory, str(item_metadata_file_start + '-' + short_ID + json_suffix))
            with open(fout, 'w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(item_metadata.json()['item']))
                file_count += 1
                print('wrote', fout)
            item_count += 1
        else:
            resource_ID = item['link']
            short_ID = item['link'].split('/')[2]
            item_metadata = requests.get(endpoint + resource_ID, params=parameters)
            print('requested',item_metadata.url,item_metadata.status_code)
            if item_metadata.status_code != 200:
                print('requested',item_metadata.url,item_metadata.status_code)
                error_count += 1
                continue
            try:
                item_metadata.json()
            except:
                error_count += 1
                print('no json found')
                continue
            fout = os.path.join(data_directory, item_metadata_directory, str(item_metadata_file_start + '-' + short_ID + json_suffix))
            with open(fout, 'w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(item_metadata.json()['item']))
                file_count += 1
                print('wrote', fout)
            item_count += 1

print('--- mini LOG ---')
print('items requested:',item_count)
print('errors:',error_count)
print('files written:',file_count)

current_loc = os.getcwd()

print(current_loc)

metadata_file_path = os.path.join('data','ftu_libs_metadata')

print(metadata_file_path)

file_count = 0

for file in glob.glob('data/ftu_libs_metadata/item_metadata-*.json'):
    file_count += 1
    print(file)
    
print('found',file_count)

list_of_item_metadata_files = list() 
for file in glob.glob('data/ftu_libs_metadata/item_metadata-*.json'):
    list_of_item_metadata_files.append(file)

len(list_of_item_metadata_files)

# quick duplicate check
list_of_item_metadata_files.sort()

for file in list_of_item_metadata_files:
    print(file)

# try first with one file, can you open the json, can you see what elements are in the json?
with open(list_of_item_metadata_files[0], 'r', encoding='utf-8') as item:
    # what are we looking at?
    print('file:',list_of_item_metadata_files[0],'\n')
    
    # load the item data
    item_data = json.load(item)
    
    for element in item_data.keys():
        print(element,':',item_data[element])
    
item_data.keys()

    # can you get the date?
print('\ndate:',item_data['date'], type(item_data['date']))
    # can you get the format?
print('\nformat:',item_data['format'][0], type(item_data['format']))

# set up the containers to create the csv of all the item fields
# file for csv to read out
collection_info_csv = 'collection_items_data.csv'

# set up a list for the columns in your csv; 
# your goal should be to automate this, but . . . 
# it works for demonstration as you set up the crosswalk
headers = ['source_file', 'item_id', 'title', 'date', 'source_url', 'phys_format', 'dig_format', 'rights']

# try first with one file
with open(list_of_item_metadata_files[0], 'r', encoding='utf-8') as data:
    # load the item data
    item_data = json.load(data)
    
    # extract the data you want
    # for checking purposes, add in the source of the info
    source_file = str(file)
    # make sure there's some unique and stable identifier
    try:
        item_id = item_data['library_of_congress_control_number']
    except:
        item_id = item_data['url'].split('/')[-2]
    title = item_data['title']
    try:
        date = item_data['date']
    except:
        date = None
    source_url = item_data['url']
    try:
        phys_format = item_data['format'][0]
    except:
        phys_format = 'Not found'
    try:
        dig_format = item_data['online_format'][0]
    except:
        dig_format = 'Not found'
    mime_type = item_data['mime_type']
    try:
        rights = item_data['rights_information']
    except:
        rights = 'Undetermined'


    # dictionary for the rows
    row_dict = dict()
    
    # look for the item metadata, assign it to the dictionary; 
    # start with some basic elements likely (already enumerated in the headers list) :
    # source file
    row_dict['source_file'] = source_file
    # identifier
    row_dict['item_id'] = item_id
    # title
    row_dict['title'] = title
    # date
    row_dict['date'] = date
    # link
    row_dict['source_url'] = source_url
    # format
    row_dict['phys_format'] = phys_format
    # digital format
    row_dict['dig_format'] = dig_format
    #rights
    row_dict['rights'] = rights 
    print('created row dictionary:',row_dict)

    # write to the csv
    with open(collection_info_csv, 'w', encoding='utf-8') as fout:
        writer = csv.DictWriter(fout, fieldnames=headers)
        writer.writeheader()
        writer.writerow(row_dict)
        print('wrote',collection_info_csv)

collection_info_csv = 'collection_items_data.csv'

# set up a list for the columns in your csv; in future, this should be more automated but this works for now as you set up the crosswalk
headers = ['source_file', 'item_id', 'title', 'date', 'source_url', 'phys_format', 'dig_format', 'rights']

# try first with one file
with open(list_of_item_metadata_files[0], 'r', encoding='utf-8') as data:
    # load the item data
    item_data = json.load(data)
    
    print(item_data['image_url'][0])

# for purposes of demonstration, use this block to make sure there isn't already a list file:

items_data_file = os.path.join(data_directory, 'collection_items_data.csv')

if os.path.isfile(items_data_file):
    os.unlink(items_data_file)
    print('removed',items_data_file)

# clear row_dict
row_dict = ()

from datetime import date

date_string_for_today = date.today().strftime('%Y-%m-%d') # see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

print(date_string_for_today)

# set up the containers to create the csv & counters 
# file for csv to read out
collection_info_csv = os.path.join('data','collection_items_data.csv')
file_count = 0
items_written = 0
error_count = 0

# add in a couple of extras for Omeka, including item type and date uploaded

# set up a list for the columns in your csv; in future, this should be more automated but this works for now as you set up the crosswalk
headers = ['item_type', 'date_uploaded', 'source_file', 'item_id', 'title', 'date', 'source_url', 'phys_format', 'dig_format', 'rights', 'image_url']

# now, adapt the previous loop to open each file:
for file in list_of_item_metadata_files:
    file_count += 1
    print('opening',file)
    with open(file, 'r', encoding='utf-8') as item:
        # load the item data
        try:
            item_data = json.load(item)
        except:
            print('error loading',file)
            error_count += 1
            continue

        # extract/name the data you want
        # item type
        item_type = 'Item'
        # date uplaoded
        date_uploaded = date_string_for_today
        # for checking purposes, add in the source of the info
        source_file = str(file)
        # make sure there's some unique and stable identifier
        try:
            item_id = item_data['library_of_congress_control_number']
        except:
            item_id = item_data['url'].split('/')[-2]
        title = item_data['title']
        try:
            date = item_data['date']
        except: 
            date = None
        source_url = item_data['url']
        try:
            phys_format = item_data['format'][0]
        except:
            phys_format = 'Not found'
        try:
            dig_format = item_data['online_format'][0]
        except:
            dig_format = 'Not found'
        mime_type = item_data['mime_type']
        try:
            rights = item_data['rights_information']
        except:
            rights = 'Undetermined'
        try:
            image_url = item_data['image_url'][3]
        except:
            image_url = 'Did not identify a URL.'

        # dictionary for the rows
        row_dict = dict()

        # look for the item metadata, assign it to the dictionary; 
        # start with some basic elements likely (already enumerated in the headers list) :
        # item type
        row_dict['item_type'] = item_type
        # date uploaded
        row_dict['date_uploaded'] = date_uploaded
        # source filename
        row_dict['source_file'] = source_file
        # identifier
        row_dict['item_id'] = item_id
        # title
        row_dict['title'] = title
        # date
        row_dict['date'] = date
        # link
        row_dict['source_url'] = source_url
        # format
        row_dict['phys_format'] = phys_format
        # digital format
        row_dict['dig_format'] = dig_format.capitalize()
        #rights
        row_dict['rights'] = rights
        #image
        row_dict['image_url'] = image_url

        # write to the csv
        with open(collection_info_csv, 'a', encoding='utf-8') as fout:
            writer = csv.DictWriter(fout, fieldnames=headers)
            if items_written == 0:
                writer.writeheader()
            writer.writerow(row_dict)
            items_written += 1
            print('adding',item_id)

print('\n\n--- LOG ---')
print('wrote',collection_info_csv)
print('with',items_written,'items')
print(error_count,'errors (info not written)')
