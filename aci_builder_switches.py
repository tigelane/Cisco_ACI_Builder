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
    Add switches to the ACI fabric from a config file.
    '''

import requests, json, sys

def error_message(error):
    '''  Calls an error message.  This takes 1 list argument with 3 components.  #1 is the error number, #2 is the error text, 
         #3 is if the application should continue or not.  Use -1 to kill the application.  Any other number
         continues the application.  You must code in a loop and go back to where you want unless you are exiting.
    '''
    
    print ('\n=================================')
    print ('  ERROR Number: ' + str(error[0]))
    print ('  ERROR Text: ' + str(error[1]))
    print ('=================================\n')
    
    if error[2] == -1:
        print ('Application ended due to error.\n')
        sys.exit()

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

def rest_login(admin):
    ''' Login to the system.  Takes information in a dictionary form for the admin user and password
    '''
    headers = {'Content-type': 'application/json'}
  
    login_url = '{0}/api/aaaLogin.json?gui-token-request=yes'.format(admin['ip_addr'])
    payload = '{"aaaUser":{"attributes":{"name":"' + admin['user']  + '","pwd":"' + admin['password'] + '"}}}'
  
    try:
        result = requests.post(login_url, data=payload, verify=False)
    except requests.exceptions.RequestException as error:   
        error_message ([1,'There was an error with the connection to the APIC.', -1])
 
    decoded_json = json.loads(result.text)

    if (result.status_code != 200):
        error_message ([decoded_json['imdata'][0]['error']['attributes']['code'], decoded_json['imdata'][0]['error']['attributes']['text'], -1])
    
    urlToken = decoded_json['imdata'][0]['aaaLogin']['attributes']['urlToken']
    refresh = decoded_json['imdata'][0]['aaaLogin']['attributes']['refreshTimeoutSeconds']
    cookie = result.cookies['APIC-cookie']

    print ('Login Accepted\n')

    return [urlToken, refresh, cookie]

def load_nodes(nodes):
    # Returns a list of nodes to be added to the system
    # This is the main logic
    # This will need to be updated to take the entier dictionary for swithces and then calculate the node numbers and names.
    # Then return a list of dhcpNode objects
    new_nodes = []
    spine_number = int(nodes['spines']['numberbase'])
    leaf_number = int(nodes['leafs']['numberbase'])


    for switch in nodes['switches']:
        if switch[0] == 'leaf':
            newNode = dhcpNode('','',str(leaf_number),'','',nodes['leafs']['namebase'] + str(leaf_number),switch[1],'','')
            leaf_number += 1
        else:
            newNode = dhcpNode('','',str(spine_number),'','',nodes['spines']['namebase'] + str(spine_number),switch[1],'','')
            spine_number += 1

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

def build_switches(rest_session, nodes):
    # Takes ip_addr, user, and password in a dictonary for the APIC.  Takes the nodes in a list.
    # Returns True or False for sucess.
    import aci_builder as parent
    all_nodes = load_nodes(nodes)

    for node in all_nodes:
        add_node(node, rest_session)

    return True
