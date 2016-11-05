#!/usr/bin/env python
################################################################################
#
################################################################################
#                                                                              #
# Copyright (c) 2015 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
"""
Sample of creating OSPF interface in a Tenant
"""

from acitoolkit.acitoolkit import Credentials, Session, Tenant, Context
from acitoolkit.acitoolkit import OutsideL3, OutsideEPG, Interface, L2Interface
from acitoolkit.acitoolkit import L3Interface, OSPFRouter, OSPFInterfacePolicy
from acitoolkit.acitoolkit import OSPFInterface, Contract, BridgeDomain


def build_tenant(session, tenant):

    try:
        create_interface(session, tenant)
        print ("Created a Layer 3 External gateway in tenant {}.".format(tenant['name']))
        return True
    except:
        print ("ERROR: Problem creating tenant {}.".format(tenant['name']))
        return False

def create_interface(session, tenant):
    ''' The epgs are in the form of a dictionary with provide and consume.  
        There can be only one of each.
    '''

    theTenant = Tenant(tenant['name'])

    theVRF = Context('{0}_VRF'.format(tenant['name']), theTenant)
    outside_l3 = OutsideL3(tenant['name'] + "_gateway", theTenant)
    outside_l3.add_context(theVRF)
    theBD = BridgeDomain(tenant['bridgedomain'], theTenant)
    theBD.add_context(theVRF)

    phyinterface = 'eth ' + tenant['gateway']['nodeID'] + "/" + tenant['gateway']['interface']['interface1'] + "/" + tenant['gateway']['interface']['interface2']

    # Interface Config
    phyif = Interface('eth', '1', tenant['gateway']['nodeID'], tenant['gateway']['interface']['interface1'], tenant['gateway']['interface']['interface2'])
    phyif.speed = tenant['gateway']['interface']['speed']
    l2if = L2Interface(phyinterface, 'vlan', tenant['gateway']['interface']['vlan'])
    l2if.attach(phyif)
    l3if = L3Interface('l3if')
    l3if.set_l3if_type('sub-interface')
    # l3if.set_mtu('1500')
    l3if.set_addr(tenant['gateway']['interface']['ipaddress'])
    l3if.add_context(theVRF)
    l3if.attach(l2if)

    #Router Config
    rtr = OSPFRouter('rtr-2')
    rtr.set_router_id(tenant['gateway']['routerID'])
    rtr.set_node_id(tenant['gateway']['nodeID'])
    ifpol = OSPFInterfacePolicy('1G_OSPF', theTenant)
    #ifpol.set_nw_type('p2p')
    ospfif = OSPFInterface(tenant['name'], router=rtr, area_id=tenant['gateway']['area'])
    #ospfif.auth_key = ''
    ospfif.int_policy_name = ifpol.name
    ospfif.auth_keyid = '1'
    ospfif.auth_type = 'simple'
    theTenant.attach(ospfif)
    ospfif.networks.append(tenant['gateway']['network'])
    ospfif.attach(l3if)
    outside_epg = OutsideEPG(tenant['gateway']['ext_epg'], outside_l3)
    outside_l3.attach(ospfif)

    resp = session.push_to_apic(theTenant.get_url(),
                                theTenant.get_json())

    # print resp.text
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)
