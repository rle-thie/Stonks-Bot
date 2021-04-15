import requests
import json
import sys

def parser(array, file):
  with open(file, 'w+') as json_file:
    json.dump(array, json_file)

def retrieve_message(channel_id, client_id):
  headers = {
    'authorization': client_id
  }
  re = requests.get(f'https://discord.com/api/v8/channels/{channel_id}/messages', headers=headers)
  jsonn = json.loads(re.text)
  return jsonn

def scrap(channel_id, client_id):
  animation = "|/-\\"
  c=0;search = True
  while search:
    string = retrieve_message(channel_id, client_id)[0]["content"].split()
    for mot in string:
      if mot[0] == '#':
        name = mot.replace('#', '')
        search = False
    sys.stdout.write("\r" + animation[c % len(animation)])
    sys.stdout.flush()
    c+=1
  return name