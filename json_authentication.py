import json
import os

def get_credential(json_file, key, sub_key):
   '''This function queries your secrets so you don\'t have to upload them to your Git repository.
   The function takes three arguments:

   json_file is a JSON file path (supplied as a string) where the function will find your API authentication information.
   key is the first level of the JSON document and provides a unique name for each set of API documentation. The function is structured this way so that you can store authentication information for multiple APIs in this file.
   sub_key is the name of the individual keys for each API. For the Omeka S API, there are two, one named key_identity and another named key_credential.

   The authentication information provides a level of security for your API, so you should not share keys publicly. 
   This function allows you to draw on the keys without sharing them, while also uploading your code to a public space like GitHub.

   You may need to modify the information provided based on the name of your secrets file, and the name that you give to the keys and sub_keys in your file.'''
   try:
       with open(json_file) as f:
           data = json.load(f)
           return data[key][sub_key]
   except Exception as e:
       print("Error: ", e)

key_identity = get_credential('../secrets.json', 'omeka', 'key_identity')
key_credential = get_credential('../secrets.json', 'omeka', 'key_credential') 

print(key_identity)
print(key_credential)

current_path = os.getcwd()
print("Current Path:", current_path)

