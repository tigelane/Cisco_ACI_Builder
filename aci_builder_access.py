#!/usr/bin/env python

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.naming
import cobra.mit.request
import cobra.mit.session
import cobra.model.infra
from cobra.internal.codec.xmlcodec import toXMLStr

# All the other stuff we need.
import sys, random, string

system_config = ""

def switch_profile(cobra_md, portName):
    name_base = "Leafs_R1"
    portDn = "uni/infra/accportprof-" + portName
    topDn = "uni/infra/nprof-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    range_name = system_config["servers_vmware"]["switch_range_name"]
    leaf1 = system_config["servers_vmware"]["leaf1"]
    leaf2 = system_config["servers_vmware"]["leaf2"]

    blockname = [random.choice(string.hexdigits).lower() for n in xrange(16)]
    blockranname = ''.join(blockname)

    # build the request using cobra syntax
    infraNodeP = cobra.model.infra.NodeP(topMo, ownerKey=u'', name=name_base, descr=u'', ownerTag=u'')
    infraLeafS = cobra.model.infra.LeafS(infraNodeP, ownerKey=u'', type=u'range', name=range_name, descr=u'', ownerTag=u'')
    infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafS, from_=leaf1, name=blockranname, descr=u'', to_=leaf2)

    # Add the interface associations
    infraRsAccPortP = cobra.model.infra.RsAccPortP(infraNodeP, tDn=portDn)

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def linklevel_1g(cobra_md):
    name_base = "1g"
    topDn = "uni/infra/hintfpol-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fabricHIfPol = cobra.model.fabric.HIfPol(topMo, ownerKey=u'', name=name_base, descr=u'', ownerTag=u'', autoNeg=u'on', speed=u'1G', linkDebounce=u'100')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def linklevel_10g(cobra_md):
    name_base = "10g"
    topDn = "uni/infra/hintfpol-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fabricHIfPol = cobra.model.fabric.HIfPol(topMo, ownerKey=u'', name=name_base, descr=u'', ownerTag=u'', autoNeg=u'on', speed=u'10G', linkDebounce=u'100')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def cdp_on(cobra_md):
    name_base = "CDP_On"
    topDn = "uni/infra/cdpIfP-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    cdpIfPol = cobra.model.cdp.IfPol(topMo, ownerKey=u'', name=name_base, descr=u'', adminSt=u'enabled', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def cdp_off(cobra_md):
    name_base = "CDP_Off"
    topDn = "uni/infra/cdpIfP-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    cdpIfPol = cobra.model.cdp.IfPol(topMo, ownerKey=u'', name=name_base, descr=u'', adminSt=u'disabled', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)


def lldp_on(cobra_md):
    name_base = "LLDP_On"
    topDn = "uni/infra/lldpIfP-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    lldpIfPol = cobra.model.lldp.IfPol(topMo, ownerKey=u'', name=name_base, descr=u'', adminTxSt=u'enabled', adminRxSt=u'enabled', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def lldp_off(cobra_md):
    name_base = "LLDP_Off"
    topDn = "uni/infra/lldpIfP-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    lldpIfPol = cobra.model.lldp.IfPol(topMo, ownerKey=u'', name=name_base, descr=u'', adminTxSt=u'disabled', adminRxSt=u'disabled', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def interfaces(cobra_md, name_base):
    top_name = name_base + "_Servers"
    int_name = name_base + "_Interfaces"
    pol_grp = name_base + "_PolicyGrp"
    start_range = system_config["servers_vmware"]["interfaces_start"]
    end_range = system_config["servers_vmware"]["interfaces_finish"]

    topDn = "uni/infra/accportprof-" + top_name
    polgrpDn = "uni/infra/funcprof/accportgrp-" + pol_grp

    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortP = cobra.model.infra.AccPortP(topMo, ownerKey=u'', name=top_name, descr=u'', ownerTag=u'')
    infraHPortS = cobra.model.infra.HPortS(infraAccPortP, ownerKey=u'', type=u'range', name=int_name, descr=u'', ownerTag=u'')
    infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, fexId=u'101', tDn=polgrpDn)
    infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block2', descr=u'', fromPort=start_range, fromCard=u'1', toPort=end_range, toCard=u'1')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def interfacegrp(cobra_md, name):
    name_base = name + "_PolicyGrp"
    aaepName =   "uni/infra/attentp-" + name + "_AAEP"
    topDn = "uni/infra/funcprof/accportgrp-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    intspeed = system_config['servers_vmware']['speed']

    if system_config['servers_vmware']['cdp'] == "enabled":
        CDP = 'CDP_On'
    else:
        CDP = 'CDP_Off'
    if system_config['servers_vmware']['lldp'] == "enabled":
        LLDP = 'LLDP_On'
    else:
        LLDP = 'LLDP_Off'


    # build the request using cobra syntax
    infraAccPortGrp = cobra.model.infra.AccPortGrp(topMo, ownerKey=u'', name=name_base, descr=u'', ownerTag=u'')
    infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccPortGrp, tnFabricHIfPolName=intspeed)
    infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccPortGrp, tDn=aaepName)
    infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccPortGrp, tnLldpIfPolName=CDP)
    infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccPortGrp, tnCdpIfPolName=LLDP)

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def aaep(cobra_md, name):
    name_base = name + "_AAEP"
    topDn = "uni/infra/attentp-" + name_base
    topDn = cobra.mit.naming.Dn.fromString(topDn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAttEntityP = cobra.model.infra.AttEntityP(topMo, ownerKey=u'', name=name_base, descr=u'', ownerTag=u'')
    # infraRsDomP2 = cobra.model.infra.RsDomP(infraAttEntityP, tDn=u'uni/vmmp-VMware/dom-lko_aci')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def build_access(cobra_md, config):
    global system_config
    system_config = config

    # Global
    name = system_config['servers_vmware']['namebase']
    intname = name + "_Servers"

    switch_profile(cobra_md, intname)
    linklevel_1g(cobra_md)
    linklevel_10g(cobra_md)
    cdp_on(cobra_md)
    cdp_off(cobra_md)
    lldp_on(cobra_md)
    lldp_off(cobra_md)

    # Server Uplinks
    interfaces(cobra_md, name)
    interfacegrp(cobra_md, name)
    aaep(cobra_md, name)

    print 'That saved a lot of clicking!'