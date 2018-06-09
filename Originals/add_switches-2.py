#!/usr/bin/env python
################################################################################
#                                                                                                                                  
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   
#    not use this file except in compliance with the License. You may obtain   
#    a copy of the License at                                                  
#                                                                              
#         http://www.apache.org/licenses/LICENSE-2.0                           
#                                                                              
#    Unless required by applicable law or agreed to in writing, software       
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  
#    License for the specific language governing permissions and limitations   
#    under the License.                                                        
#                                                                              
################################################################################

description = '''
    This script uses a configuration file to build your ACI environment.  If the config file is not found 
    in the same directory as the script is run from it will prompt you to create it.  
    Please modify it to your requirements and then run the script again.
    '''

import requests, json

class dhcpNode:

    def __init__(self, clientEvent,hwAddr,serial,ip,model,name,nodeId,nodeRole,supported):
        self.clientEvent = clientEvent
        self.hwAddr = hwAddr
        self.serial = serial
        self.ip = ip
        self.model = model
        self.name = name
        self.nodeId = nodeId
        self.nodeRole = nodeRole
        self.supported = supported

    def __str__(self):
        return 'Name: {0}  Model: {1}  Serial: {2}  ID: {3}'.format(self.name, self.model, self.serial, self.nodeId)

    def set_name(self, name):
        self.name = name

    def set_serial(self, serial):
        self.serial = serial

    def set_nodeId(self, nodeId):
        self.nodeId = nodeId

    def not_installed(self):
        if self.clientEvent == 'denied':
          return True
        else:
          return False

    def push_to_apic(self, admin):
        if self.name == '' or self.nodeId == '':
          return False

        headers = {'Content-type': 'application/json', 'APIC-challenge':admin['urlToken']}
        cookie = {'APIC-cookie':admin['APIC-cookie']}
        url = '{0}/api/node/mo/uni/controller/nodeidentpol.json'.format(admin['ip_addr'])

        payload = '{"fabricNodeIdentP":{"attributes":{'
        payload += '"dn": "uni/controller/nodeidentpol/nodep-' + self.serial
        payload += '","serial": "' + self.serial
        payload += '","nodeId": "' + self.nodeId
        payload += '","name": "' + self.name
        payload += '","status": "created,modified"},"children": []}}'

        result = requests.post(url, data=payload, headers=headers, cookies=cookie, verify=False)
        return result

def load_nodes():
    # Returns a list of nodes to be added to the system
    new_nodes = []

    with open(switches_file) as file:
        for line in file:
            # seperate the values
            items = [x.strip() for x in line.split(',')]
            newNode = dhcpNode('','',items[2],'','',items[1],items[0],'','')
            new_nodes.append(newNode)

    return new_nodes

def add_node(node, admin):
    print ('\nWould you like to add this device to the system?')
    print (node)
    junk = raw_input('(Yes) or No: ')
    if junk.lower() == 'no' or junk.lower() == 'n':
        print ('Node skipped.')
        return

    print ("YES - Ok, let's add it.\n")

    result = node.push_to_apic(admin)
    if (result.status_code != 200):
        decoded_json = json.loads(result.text)
        error_message ([decoded_json['imdata'][0]['error']['attributes']['code'], decoded_json['imdata'][0]['error']['attributes']['text'], -1])

    return True

def main(argv):
    # Need to send me a login object.

    # Read in the csv file on the command line and create Nodes from each line
    # Error and show format if it doesn't work.
    # While I have Nodes in a list, add them to the APIC
  
    all_nodes = load_nodes()
    for node in all_nodes:
        add_node(node, admin)


    return True

if __name__ == '__main__':
    main(sys.argv)
