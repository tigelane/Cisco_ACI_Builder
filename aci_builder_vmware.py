#!/usr/bin/env python
################################################################################
#
################################################################################
description = '''
    This script will create an environment for VMware in an ACI fabric.
    The following tasks will be accomplished:
    * VMware VMM setup
    * VMM VLAN pool
    * Physical interface configs
    * Switch and Interface linkage from VMM to physical
'''

# Cisco ACI Cobra packages
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.cdp
import cobra.model.fabric
import cobra.model.infra
import cobra.model.lldp
import cobra.model.pol

from cobra.internal.codec.xmlcodec import toXMLStr

# ACI Toolkit packages
import acitoolkit.acitoolkit as ACI

# All the other stuff we need.
import sys, random, string

# Global vars
unique_tenant = 'ESXi-Tenant'
vmm_name = ''

def create_vmm_domain(session):
    global vmm_name
    # Get all the arguments
    description = 'Create VMM Domain'

    # Define dynamic vlan range
    pool_name = system_config['vmware_vmm']['namebase'] + '_vlans'
    encap = 'vlan'
    mode = 'dynamic'
    vlans = ACI.NetworkPool(pool_name, encap, system_config['vmware_vmm']['vlan_start'], system_config['vmware_vmm']['vlan_end'], mode)

    # Commit VLAN Range
    vlanresp = session.push_to_apic(vlans.get_url(), vlans.get_json())

    if not vlanresp.ok:
        print('%% Error: Could not push VLAN configuration to APIC')
        print(vlanresp.text)
        exit()

    admin_name = system_config['vmware_vmm']['namebase'] + "_admin"

    # Create Credentials object
    vcenter_creds = ACI.VMMCredentials(admin_name, system_config['vmware_vmm']['user'], system_config['vmware_vmm']['password'])

    # Vswitch Info object
    vmmtype = 'VMware'
    dvs_name = system_config['vmware_vmm']['namebase']
    vswitch_info = ACI.VMMvSwitchInfo(vmmtype, system_config['vmware_vmm']['datacenter'], dvs_name)

    # Create VMM object
    vmm_name = system_config['vmware_vmm']['namebase']
    vmm = ACI.VMM(vmm_name, system_config['vmware_vmm']['vcenterip'], vcenter_creds, vswitch_info, vlans)

    # Commit Changes
    resp = session.push_to_apic(vmm.get_url(), vmm.get_json())

    if not resp.ok:
        print('%% Error: Could not push VMM configuration to APIC')
        print(resp.text)
        exit()

def create_int_basics(cobra_md):
    global int_name, cdp_name, lldp_name
    int_name = system_config['servers_vmware']['namebase'] + '_link'
    link_speed = system_config['servers_vmware']['speed']
    cdp_name = system_config['servers_vmware']['namebase'] + '_cdp'
    cdp_state = system_config['servers_vmware']['cdp']
    lldp_name = system_config['servers_vmware']['namebase'] + '_lldp'
    lldp_state = system_config['servers_vmware']['lldp']

    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)
    
    # build the request using cobra syntax
    fabricHIfPol = cobra.model.fabric.HIfPol(infraInfra, ownerKey=u'', name=int_name, descr=u'', ownerTag=u'', autoNeg=u'on', speed=link_speed, linkDebounce=u'100')
    cdpIfPol = cobra.model.cdp.IfPol(infraInfra, ownerKey=u'', name=cdp_name, descr=u'', adminSt=cdp_state, ownerTag=u'')
    lldpIfPol = cobra.model.lldp.IfPol(infraInfra, ownerKey=u'', name=lldp_name, descr=u'', adminTxSt=lldp_state, adminRxSt=lldp_state, ownerTag=u'')

    # commit the generated code to APIC
    c = cobra.mit.request.ConfigRequest()
    c.addMo(infraInfra)
    cobra_md.commit(c)

def create_aaep(cobra_md):
    global aaep_name
    aaep_name = system_config['servers_vmware']['namebase'] + '_aaep'
    vmm_domain = 'uni/vmmp-VMware/dom-' + vmm_name

    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)

    # build the request using cobra syntax
    infraAttEntityP = cobra.model.infra.AttEntityP(infraInfra, ownerKey=u'', name=aaep_name, descr=u'', ownerTag=u'')
    infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn=vmm_domain)

    c = cobra.mit.request.ConfigRequest()
    c.addMo(infraInfra)
    cobra_md.commit(c)

def create_int_polgrp(cobra_md):
    global intgrp_name
    intgrp_name = system_config['servers_vmware']['namebase'] + '_intgrp'
    dnattach_point = 'uni/infra/attentp-' + aaep_name

    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)
    infraFuncP = cobra.model.infra.FuncP(infraInfra)

    infraAccPortGrp = cobra.model.infra.AccPortGrp(infraFuncP, ownerKey=u'', name=intgrp_name, descr=u'', ownerTag=u'')
    infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccPortGrp, tnLldpIfPolName=lldp_name)
    infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccPortGrp, tnCdpIfPolName=cdp_name)
    infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccPortGrp, tDn=dnattach_point)
    infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccPortGrp, tnFabricHIfPolName=int_name)

    c = cobra.mit.request.ConfigRequest()
    c.addMo(infraInfra)
    cobra_md.commit(c)

def create_int_profile(cobra_md):
    global intpro_name
    intpro_name = system_config['servers_vmware']['namebase'] + '_servers'
    sel_name = system_config['servers_vmware']['namebase'] + '_interfaces'
    dnintgrp_name = 'uni/infra/funcprof/accportgrp-' + intgrp_name

    fromcard = system_config['servers_vmware']['interfaces'].split('/')[0]
    tocard = system_config['servers_vmware']['interfaces'].split('/')[0]
    fromport = system_config['servers_vmware']['interfaces'].split('/')[1].split('-')[0]
    toport = system_config['servers_vmware']['interfaces'].split('/')[1].split('-')[1]

    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)

    infraAccPortP = cobra.model.infra.AccPortP(infraInfra, ownerKey=u'', name=intpro_name, descr=u'', ownerTag=u'')
    infraHPortS = cobra.model.infra.HPortS(infraAccPortP, ownerKey=u'', type=u'range', name=sel_name, descr=u'', ownerTag=u'')
    infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, fexId=u'101', tDn=dnintgrp_name)
    infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block1', descr=u'', fromPort=fromport, fromCard=fromcard, toPort=toport, toCard=tocard)

    c = cobra.mit.request.ConfigRequest()
    c.addMo(infraInfra)
    cobra_md.commit(c)

def get_leafs(session):
    from acitoolkit.aciphysobject import Node
    data = []

    items = Node.get(session)
    for item in items:
        if item.role == 'leaf':
            data.append(item.node)
    
    return data

def create_sw_profile(cobra_md, leafs):
    swproname = system_config['servers_vmware']['namebase'] + '_sw_pro'
    dnintpro_name = 'uni/infra/accportprof-' + intpro_name


    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)

    for leaf in leafs:
        blockname = [random.choice(string.hexdigits).lower() for n in xrange(16)]
        blockname = ''.join(blockname)
        b_name = 'leaf-' + leaf

        infraNodeP = cobra.model.infra.NodeP(infraInfra, ownerKey=u'', name=swproname, descr=u'', ownerTag=u'')
        infraLeafS = cobra.model.infra.LeafS(infraNodeP, ownerKey=u'', type=u'range', name=b_name, descr=u'', ownerTag=u'')
        infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafS, from_=leaf, name=blockname, descr=u'', to_=leaf)
        infraRsAccPortP = cobra.model.infra.RsAccPortP(infraNodeP, tDn=dnintpro_name)

        c = cobra.mit.request.ConfigRequest()
        c.addMo(infraInfra)
        cobra_md.commit(c)

def build_vmware(cobra_md, session, config):
    global system_config
    system_config = config

    create_vmm_domain(session)
    create_int_basics(cobra_md)
    create_aaep(cobra_md)
    create_int_polgrp(cobra_md)
    create_int_profile(cobra_md)

    leafs = get_leafs(session)
    create_sw_profile(cobra_md, leafs)
