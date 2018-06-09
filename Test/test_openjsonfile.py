#!/usr/bin/env python

import json

jsonfile = "myjson.json"

new_nodes = []


with open(jsonfile) as json_data:
    d = json.load(json_data)

admin_info = d['credentials']
print (admin_info)

print (d['time'])
print ("\n\n")
for server in d['time']['servers']:
    print (server)

print ("\n\n")
print (json.dumps(d, indent=4, sort_keys=True))
