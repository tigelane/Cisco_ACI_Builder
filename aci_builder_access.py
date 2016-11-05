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

def switch_profile(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/nprof-Leafs')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraNodeP = cobra.model.infra.NodeP(topMo, ownerKey=u'', name=u'Leafs', descr=u'', ownerTag=u'')
    infraLeafS = cobra.model.infra.LeafS(infraNodeP, ownerKey=u'', type=u'range', name=u'Leafs', descr=u'', ownerTag=u'')
    infraNodeBlk = cobra.model.infra.NodeBlk(infraLeafS, from_=u'201', name=u'3a608b521b4633b7', descr=u'', to_=u'202')
    infraRsAccPortP = cobra.model.infra.RsAccPortP(infraNodeP, tDn=u'uni/infra/accportprof-RPIs')
    infraRsAccPortP2 = cobra.model.infra.RsAccPortP(infraNodeP, tDn=u'uni/infra/accportprof-UCS_Uplinks')
    infraRsAccPortP3 = cobra.model.infra.RsAccPortP(infraNodeP, tDn=u'uni/infra/accportprof-Routers')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def linklevel_1g(cobra_md):

    topDn = cobra.mit.naming.Dn.fromString('uni/infra/hintfpol-1g')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fabricHIfPol = cobra.model.fabric.HIfPol(topMo, ownerKey=u'', name=u'1g', descr=u'', ownerTag=u'', autoNeg=u'on', speed=u'1G', linkDebounce=u'100')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def cdp_on(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/cdpIfP-On')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    cdpIfPol = cobra.model.cdp.IfPol(topMo, ownerKey=u'', name=u'On', descr=u'', adminSt=u'enabled', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def lldp_on(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/lldpIfP-LLDP_ON')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    lldpIfPol = cobra.model.lldp.IfPol(topMo, ownerKey=u'', name=u'LLDP_ON', descr=u'', adminTxSt=u'enabled', adminRxSt=u'enabled', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def int_ucs(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/accportprof-UCS_Uplinks')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortP = cobra.model.infra.AccPortP(topMo, ownerKey=u'', name=u'UCS_Uplinks', descr=u'', ownerTag=u'')
    infraHPortS = cobra.model.infra.HPortS(infraAccPortP, ownerKey=u'', type=u'range', name=u'UCS_Uplinks', descr=u'', ownerTag=u'')
    infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, fexId=u'101', tDn=u'uni/infra/funcprof/accportgrp-UCS_single_Uplinks')
    infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block2', descr=u'', fromPort=u'17', fromCard=u'1', toPort=u'18', toCard=u'1')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def intgrp_ucs(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/funcprof/accportgrp-UCS_single_Uplinks')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortGrp = cobra.model.infra.AccPortGrp(topMo, ownerKey=u'', name=u'UCS_single_Uplinks', descr=u'', ownerTag=u'')
    infraRsL2IfPol = cobra.model.infra.RsL2IfPol(infraAccPortGrp, tnL2IfPolName=u'')
    #infraRsQosPfcIfPol = cobra.model.infra.RsQosPfcIfPol(infraAccPortGrp, tnQosPfcIfPolName=u'')
    infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccPortGrp, tnFabricHIfPolName=u'10G_UCS')
    #infraRsL2PortSecurityPol = cobra.model.infra.RsL2PortSecurityPol(infraAccPortGrp, tnL2PortSecurityPolName=u'')
    infraRsMonIfInfraPol = cobra.model.infra.RsMonIfInfraPol(infraAccPortGrp, tnMonInfraPolName=u'')
    infraRsStpIfPol = cobra.model.infra.RsStpIfPol(infraAccPortGrp, tnStpIfPolName=u'')
    #infraRsQosSdIfPol = cobra.model.infra.RsQosSdIfPol(infraAccPortGrp, tnQosSdIfPolName=u'')
    infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccPortGrp, tDn=u'uni/infra/attentp-UCS_Uplinks')
    infraRsMcpIfPol = cobra.model.infra.RsMcpIfPol(infraAccPortGrp, tnMcpIfPolName=u'')
    #infraRsQosDppIfPol = cobra.model.infra.RsQosDppIfPol(infraAccPortGrp, tnQosDppPolName=u'')
    #infraRsQosIngressDppIfPol = cobra.model.infra.RsQosIngressDppIfPol(infraAccPortGrp, tnQosDppPolName=u'')
    #infraRsStormctrlIfPol = cobra.model.infra.RsStormctrlIfPol(infraAccPortGrp, tnStormctrlIfPolName=u'')
    #infraRsQosEgressDppIfPol = cobra.model.infra.RsQosEgressDppIfPol(infraAccPortGrp, tnQosDppPolName=u'')
    #infraRsFcIfPol = cobra.model.infra.RsFcIfPol(infraAccPortGrp, tnFcIfPolName=u'')
    infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccPortGrp, tnLldpIfPolName=u'OFF')
    infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccPortGrp, tnCdpIfPolName=u'On')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def aaep_ucs(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/attentp-UCS_Uplinks')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAttEntityP = cobra.model.infra.AttEntityP(topMo, ownerKey=u'', name=u'UCS_Uplinks', descr=u'', ownerTag=u'')
    infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn=u'uni/phys-vmware_mgmt')
    infraRsDomP2 = cobra.model.infra.RsDomP(infraAttEntityP, tDn=u'uni/vmmp-VMware/dom-lko_aci')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def intgrp_routers(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/funcprof/accportgrp-1GRouter')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortGrp = cobra.model.infra.AccPortGrp(topMo, ownerKey=u'', name=u'1GRouter', descr=u'', ownerTag=u'')
    infraRsMonIfInfraPol = cobra.model.infra.RsMonIfInfraPol(infraAccPortGrp, tnMonInfraPolName=u'')
    infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccPortGrp, tnLldpIfPolName=u'')
    infraRsStpIfPol = cobra.model.infra.RsStpIfPol(infraAccPortGrp, tnStpIfPolName=u'')
    infraRsL2IfPol = cobra.model.infra.RsL2IfPol(infraAccPortGrp, tnL2IfPolName=u'')
    infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccPortGrp, tnCdpIfPolName=u'On')
    infraRsMcpIfPol = cobra.model.infra.RsMcpIfPol(infraAccPortGrp, tnMcpIfPolName=u'')
    infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccPortGrp, tDn=u'uni/infra/attentp-Routers')
    infraRsStormctrlIfPol = cobra.model.infra.RsStormctrlIfPol(infraAccPortGrp, tnStormctrlIfPolName=u'')
    infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccPortGrp, tnFabricHIfPolName=u'1g')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def int_routers(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/accportprof-Routers')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortP = cobra.model.infra.AccPortP(topMo, ownerKey=u'', name=u'Routers', descr=u'', ownerTag=u'')
    infraHPortS = cobra.model.infra.HPortS(infraAccPortP, ownerKey=u'', type=u'range', name=u'Routers_6', descr=u'', ownerTag=u'')
    infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, fexId=u'101', tDn=u'uni/infra/funcprof/accportgrp-1GRouter')
    infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block2', descr=u'', fromPort=u'6', fromCard=u'1', toPort=u'6', toCard=u'1')
    infraHPortS2 = cobra.model.infra.HPortS(infraAccPortP, ownerKey=u'', type=u'range', name=u'Routers_5', descr=u'', ownerTag=u'')
    infraRsAccBaseGrp2 = cobra.model.infra.RsAccBaseGrp(infraHPortS2, fexId=u'101', tDn=u'uni/infra/funcprof/accportgrp-1GRouter')
    infraPortBlk2 = cobra.model.infra.PortBlk(infraHPortS2, name=u'block2', descr=u'', fromPort=u'5', fromCard=u'1', toPort=u'5', toCard=u'1')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def aaep_routers(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/attentp-Routers')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAttEntityP = cobra.model.infra.AttEntityP(topMo, ownerKey=u'', name=u'Routers', descr=u'', ownerTag=u'')
    infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn=u'uni/l3dom-OSPF_Routers')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def intgrp_rpi(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/funcprof/accportgrp-RPIs')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortGrp = cobra.model.infra.AccPortGrp(topMo, ownerKey=u'', name=u'RPIs', descr=u'', ownerTag=u'')
    infraRsMonIfInfraPol = cobra.model.infra.RsMonIfInfraPol(infraAccPortGrp, tnMonInfraPolName=u'')
    infraRsLldpIfPol = cobra.model.infra.RsLldpIfPol(infraAccPortGrp, tnLldpIfPolName=u'LLDP_ON')
    infraRsStpIfPol = cobra.model.infra.RsStpIfPol(infraAccPortGrp, tnStpIfPolName=u'')
    infraRsL2IfPol = cobra.model.infra.RsL2IfPol(infraAccPortGrp, tnL2IfPolName=u'')
    infraRsCdpIfPol = cobra.model.infra.RsCdpIfPol(infraAccPortGrp, tnCdpIfPolName=u'On')
    infraRsMcpIfPol = cobra.model.infra.RsMcpIfPol(infraAccPortGrp, tnMcpIfPolName=u'')
    infraRsAttEntP = cobra.model.infra.RsAttEntP(infraAccPortGrp, tDn=u'uni/infra/attentp-RaspberryPIs')
    infraRsStormctrlIfPol = cobra.model.infra.RsStormctrlIfPol(infraAccPortGrp, tnStormctrlIfPolName=u'')
    infraRsHIfPol = cobra.model.infra.RsHIfPol(infraAccPortGrp, tnFabricHIfPolName=u'1g')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def int_rpi(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/accportprof-RPIs')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAccPortP = cobra.model.infra.AccPortP(topMo, ownerKey=u'', name=u'RPIs', descr=u'', ownerTag=u'')
    infraHPortS = cobra.model.infra.HPortS(infraAccPortP, ownerKey=u'', type=u'range', name=u'RPIs', descr=u'', ownerTag=u'')
    infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS, fexId=u'101', tDn=u'uni/infra/funcprof/accportgrp-RPIs')
    infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, name=u'block2', descr=u'', fromPort=u'1', fromCard=u'1', toPort=u'1', toCard=u'1')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def vlanpool_rpi(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/vlanns-[RaspberryPI_Server]-static')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvnsVlanInstP = cobra.model.fvns.VlanInstP(topMo, ownerKey=u'', name=u'RaspberryPI_Server', descr=u'', ownerTag=u'', allocMode=u'static')
    fvnsEncapBlk = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-99', from_=u'vlan-30', name=u'', descr=u'', allocMode=u'static')

    # commit the generated code to APIC
    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def domain_rpi(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/phys-RPIs')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    physDomP = cobra.model.phys.DomP(topMo, ownerKey=u'', name=u'RPIs', ownerTag=u'')
    infraRsVlanNs = cobra.model.infra.RsVlanNs(physDomP, tDn=u'uni/infra/vlanns-[RaspberryPI_Server]-static')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(physDomP)
    cobra_md.commit(c)

def aaep_rpis(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/attentp-RaspberryPIs')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    infraAttEntityP = cobra.model.infra.AttEntityP(topMo, ownerKey=u'', name=u'RaspberryPIs', descr=u'', ownerTag=u'')
    infraRsDomP = cobra.model.infra.RsDomP(infraAttEntityP, tDn=u'uni/phys-RPIs')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def vmware_mgmt_vlans(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/infra/vlanns-[vmware_mgmt]-static')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvnsVlanInstP = cobra.model.fvns.VlanInstP(topMo, ownerKey=u'', name=u'vmware_mgmt', descr=u'', ownerTag=u'', allocMode=u'static')
    fvnsEncapBlk = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-24', from_=u'vlan-15', name=u'', descr=u'', allocMode=u'static')

    # commit the generated code to APIC
    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def vmware_mgmt_phydomain(cobra_md):
    topDn = cobra.mit.naming.Dn.fromString('uni/phys-vmware_mgmt')
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    physDomP = cobra.model.phys.DomP(topMo, ownerKey=u'', name=u'vmware_mgmt', ownerTag=u'')
    infraRsVlanNs = cobra.model.infra.RsVlanNs(physDomP, tDn=u'uni/infra/vlanns-[vmware_mgmt]-static')

    # commit the generated code to APIC
    c = cobra.mit.request.ConfigRequest()
    c.addMo(physDomP)
    cobra_md.commit(c)

def vmware_bd(md):
    bd_name = system_config['Tenants'][0]["bridgedomain"]
    this_dn = "uni/tn-" + system_config['Tenants'][0]["name"] + "/BD-" + system_config['Tenants'][0]["bridgedomain"]
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-VMware_mgmt/BD-vmware_mgmt')
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvBD = cobra.model.fv.BD(topMo, ownerKey=u'', vmac=u'not-applicable', unkMcastAct=u'flood', name=bd_name, descr=u'', unkMacUcastAct=u'proxy', arpFlood=u'no', limitIpLearnToSubnets=u'no', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', unicastRoute=u'yes', ownerTag=u'', multiDstPktAct=u'bd-flood')
    fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, tnNdIfPolName=u'')
    fvRsBDToOut = cobra.model.fv.RsBDToOut(fvBD, tnL3extOutName=u'L3_Egress')
    fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName=u'vmware_mgmt')
    fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName=u'')
    fvSubnet = cobra.model.fv.Subnet(fvBD, name=u'', descr=u'', ctrl=u'', ip=u'172.18.20.1/24', preferred=u'no', virtual=u'no')
    fvSubnet2 = cobra.model.fv.Subnet(fvBD, name=u'', descr=u'', ctrl=u'', ip=u'172.18.18.1/24', preferred=u'no', virtual=u'no')
    fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct=u'resolve', tnFvEpRetPolName=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def vmware_contract(md):
    this_dn = "uni/tn-" + system_config['Tenants'][0]["name"] + "/brc-" + system_config['Tenants'][0]["bridgedomain"]
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-VMware_mgmt/brc-vmware_mgmt')
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    vzBrCP = cobra.model.vz.BrCP(topMo, ownerKey=u'', name=u'vmware_mgmt', prio=u'unspecified', ownerTag=u'', descr=u'')
    vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', name=u'Everything', prio=u'unspecified', descr=u'', consMatchT=u'AtleastOne', provMatchT=u'AtleastOne')
    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'default')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def vmware_app(md):
    topDn = cobra.mit.naming.Dn.fromString('uni/tn-VMware_mgmt/ap-VMware_mgmt')
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvAp = cobra.model.fv.Ap(topMo, ownerKey=u'', name=u'VMware_mgmt', prio=u'unspecified', ownerTag=u'', descr=u'')
    fvAEPg = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'vmware_mgmt', prio=u'unspecified', descr=u'')
    fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName=u'vmware_mgmt', prio=u'unspecified')
    fvRsPathAtt = cobra.model.fv.RsPathAtt(fvAEPg, tDn=u'topology/pod-1/paths-201/pathep-[eth1/18]', descr=u'', instrImedcy=u'lazy', mode=u'regular', encap=u'vlan-18')
    fvRsPathAtt2 = cobra.model.fv.RsPathAtt(fvAEPg, tDn=u'topology/pod-1/paths-202/pathep-[eth1/17]', descr=u'', instrImedcy=u'lazy', mode=u'regular', encap=u'vlan-18')
    fvRsPathAtt3 = cobra.model.fv.RsPathAtt(fvAEPg, tDn=u'topology/pod-1/paths-201/pathep-[eth1/17]', descr=u'', instrImedcy=u'lazy', mode=u'regular', encap=u'vlan-18')
    fvRsPathAtt4 = cobra.model.fv.RsPathAtt(fvAEPg, tDn=u'topology/pod-1/paths-202/pathep-[eth1/18]', descr=u'', instrImedcy=u'lazy', mode=u'regular', encap=u'vlan-18')
    fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, tDn=u'uni/phys-vmware_mgmt', instrImedcy=u'lazy', encap=u'unknown', resImedcy=u'lazy')
    fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, tnQosCustomPolName=u'')
    fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName=u'vmware_mgmt')
    fvRsProv = cobra.model.fv.RsProv(fvAEPg, tnVzBrCPName=u'vmware_mgmt', matchT=u'AtleastOne', prio=u'unspecified')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def vmware_vrf(md):
    vrf_dn = "uni/tn-" + system_config['Tenants'][0]["name"] + "/ctx-" + system_config['Tenants'][0]["vrf"]
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-VMware_mgmt/ctx-vmware_mgmt')
    topDn = cobra.mit.naming.Dn.fromString(vrf_dn)
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvCtx = cobra.model.fv.Ctx(topMo, ownerKey=u'', name=u'vmware_mgmt', descr=u'', knwMcastAct=u'permit', pcEnfDir=u'ingress', ownerTag=u'', pcEnfPref=u'enforced')
    fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName=u'')
    fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName=u'')
    vzAny = cobra.model.vz.Any(fvCtx, matchT=u'AtleastOne', name=u'', descr=u'')
    vzRsAnyToProv = cobra.model.vz.RsAnyToProv(vzAny, tnVzBrCPName=u'vmware_mgmt', matchT=u'AtleastOne', prio=u'unspecified')
    fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, tnOspfCtxPolName=u'')
    fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, tnFvEpRetPolName=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def integra_bd(cobra_md):
    tenant_name = system_config['Tenants'][1]["name"]
    this_dn = "uni/tn-" + system_config['Tenants'][1]["name"] + "/ctx-" + system_config['Tenants'][1]["bridgedomain"]
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-Integra/BD-Integra')
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvBD = cobra.model.fv.BD(topMo, ownerKey=u'', vmac=u'not-applicable', unkMcastAct=u'flood', name=tenant_name, descr=u'', unkMacUcastAct=u'proxy', arpFlood=u'yes', limitIpLearnToSubnets=u'no', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', unicastRoute=u'yes', ownerTag=u'', multiDstPktAct=u'bd-flood')
    fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, tnNdIfPolName=u'')
    l3_name = tenant_name + "_L3Gateway"
    fvRsBDToOut = cobra.model.fv.RsBDToOut(fvBD, tnL3extOutName=l3_name)
    fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName=tenant_name)
    fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName=u'')
    fvSubnet = cobra.model.fv.Subnet(fvBD, name=u'', descr=u'', ctrl=u'', ip=u'192.168.100.1/24', preferred=u'no', virtual=u'no')
    fvSubnet2 = cobra.model.fv.Subnet(fvBD, name=u'', descr=u'', ctrl=u'', ip=u'192.168.200.1/24', preferred=u'no', virtual=u'no')
    fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct=u'resolve', tnFvEpRetPolName=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def integra_dhcp(cobra_md):
    this_dn = "uni/tn-" + system_config['Tenants'][1]["name"] + "/brc-DHCP"
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-Integra/brc-DHCP')
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    topParentDn = topDn.getParent()
    topMo = cobra_md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    vzBrCP = cobra.model.vz.BrCP(topMo, ownerKey=u'', name=u'DHCP', prio=u'unspecified', ownerTag=u'', descr=u'')
    vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', name=u'Ping', prio=u'unspecified', descr=u'', consMatchT=u'AtleastOne', provMatchT=u'AtleastOne')
    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'icmp')
    vzSubj2 = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', name=u'DHCP', prio=u'unspecified', descr=u'', consMatchT=u'AtleastOne', provMatchT=u'AtleastOne')
    vzRsSubjFiltAtt2 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, tnVzFilterName=u'DHCP')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    cobra_md.commit(c)

def integra_every(md):
    this_dn = "uni/tn-" + system_config['Tenants'][1]["name"] + "/brc-Everything"
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-Integra/brc-Everything')
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    vzBrCP = cobra.model.vz.BrCP(topMo, ownerKey=u'', name=u'Everything', prio=u'unspecified', ownerTag=u'', descr=u'')
    vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', name=u'Everything', prio=u'unspecified', descr=u'', consMatchT=u'AtleastOne', provMatchT=u'AtleastOne')
    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'default')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def integra_vrf(md):
    vrf_name = system_config['Tenants'][1]["vrf"]
    this_dn = "uni/tn-" + system_config['Tenants'][1]["name"] + "/ctx-" + system_config['Tenants'][1]["vrf"]
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-Integra/ctx-Integra')
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    fvCtx = cobra.model.fv.Ctx(topMo, ownerKey=u'', name=vrf_name, descr=u'', knwMcastAct=u'permit', pcEnfDir=u'ingress', ownerTag=u'', pcEnfPref=u'enforced')
    fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName=u'')
    fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName=u'')
    vzAny = cobra.model.vz.Any(fvCtx, matchT=u'AtleastOne', name=u'', descr=u'')
    vzRsAnyToProv = cobra.model.vz.RsAnyToProv(vzAny, tnVzBrCPName=u'Everything', matchT=u'AtleastOne', prio=u'unspecified')
    vzRsAnyToCons = cobra.model.vz.RsAnyToCons(vzAny, tnVzBrCPName=u'DHCP', prio=u'unspecified')
    fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, tnOspfCtxPolName=u'')
    fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, tnFvEpRetPolName=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def integra_dhcp_filt(md):
    this_dn = "uni/tn-" + system_config['Tenants'][1]["name"] + "/flt-DHCP"
    # topDn = cobra.mit.naming.Dn.fromString('uni/tn-Integra/flt-DHCP')
    topDn = cobra.mit.naming.Dn.fromString(this_dn)
    topParentDn = topDn.getParent()
    topMo = md.lookupByDn(topParentDn)

    # build the request using cobra syntax
    vzFilter = cobra.model.vz.Filter(topMo, ownerKey=u'', name=u'DHCP', descr=u'', ownerTag=u'')
    vzEntry = cobra.model.vz.Entry(vzFilter, tcpRules=u'', arpOpc=u'unspecified', applyToFrag=u'no', dToPort=u'68', descr=u'', prot=u'udp', icmpv4T=u'unspecified', sFromPort=u'unspecified', stateful=u'no', icmpv6T=u'unspecified', sToPort=u'unspecified', etherT=u'ip', dFromPort=u'67', name=u'DHCP')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)

def build_access(cobra_md, config):
    global system_config 
    system_config = config
    # Global
    switch_profile(cobra_md)
    linklevel_1g(cobra_md)
    cdp_on(cobra_md)
    lldp_on(cobra_md)

    # UCS Uplinks
    int_ucs(cobra_md)
    intgrp_ucs(cobra_md)
    aaep_ucs(cobra_md)

    # Router Interfaces
    int_routers(cobra_md)
    intgrp_routers(cobra_md)
    aaep_routers(cobra_md)

    # Raspberry PI Servers
    int_rpi(cobra_md)
    intgrp_rpi(cobra_md)
    vlanpool_rpi(cobra_md)
    domain_rpi(cobra_md)
    aaep_rpis(cobra_md)

    # VMware Management
    vmware_mgmt_vlans(cobra_md)
    vmware_mgmt_phydomain(cobra_md)
    vmware_bd(cobra_md)
    vmware_contract(cobra_md)
    vmware_app(cobra_md)
    vmware_vrf(cobra_md)

    # Integra
    integra_bd(cobra_md)
    integra_dhcp(cobra_md)
    integra_every(cobra_md)
    integra_vrf(cobra_md)
    integra_dhcp_filt(cobra_md)

    print 'That saved a lot of clicking!'