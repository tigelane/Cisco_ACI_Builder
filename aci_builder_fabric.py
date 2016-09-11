#!/usr/bin/env python

############################################################################
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
############################################################################
description = '''
    This script will create and push a configuration for an ACI lab.  
    This will include the following:
    * BGP route reflector policy using all spines as route reflectors.
    * OOB Management interfaces and addresses from a range
    * NTP configuration
    * DNS configuration

    datacenter/WebArya on github was primarily used to build the calls to the APIC.
'''

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.naming
import cobra.mit.request
import cobra.mit.session
import cobra.model.bgp
import cobra.model.datetime
import cobra.model.dns
import cobra.model.fabric
import cobra.model.fv
import cobra.model.fvns
import cobra.model.infra
import cobra.model.mgmt
import cobra.model.pol
from cobra.internal.codec.xmlcodec import toXMLStr

import sys, getpass, random, string

spine_num = 0
leaf_num = 0

def create_bgp(md, system_config):
    global spine_num
    asnum = system_config['bgp']['asnum']
    switches = []
    spine_num = 0

    for a in system_config['nodes']['switches']:
        if a[0] == 'spine':
            spine_num += 1

    if system_config['nodes']['spines']['numberbase'] and spine_num >= 1:
        firstnumber = int(system_config['nodes']['spines']['numberbase'])
        totalnumber = spine_num

    else:
        return False

    for a in range(0, totalnumber):
        switches.append(str(firstnumber + a))

    polUni = cobra.model.pol.Uni('')
    fabricInst = cobra.model.fabric.Inst(polUni)

    bgpInstPol = cobra.model.bgp.InstPol(fabricInst, ownerKey=u'', name=u'default', descr=u'', ownerTag=u'')
    bgpRRP = cobra.model.bgp.RRP(bgpInstPol, name=u'', descr=u'')

    for spine_number in switches:
        bgpRRNodePEp = cobra.model.bgp.RRNodePEp(bgpRRP, id=spine_number, descr=u'')
    bgpAsP = cobra.model.bgp.AsP(bgpInstPol, asn=asnum, descr=u'', name=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(bgpInstPol)
    md.commit(c)

    return True

def create_oob_policy(md, system_config):
    if not create_oob_ipPool(md, system_config):
        return False
    if not create_oob_connGroup(md):
        return False
    if not create_oob_nodeMgmt(md, system_config):
        return False

def create_oob_ipPool(md, system_config):
    dg_mask = system_config['oob']['dg_mask']
    start_ip = system_config['oob']['start_ip']
    end_ip = system_config['oob']['end_ip']

    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'mgmt')

    fvnsAddrInst = cobra.model.fvns.AddrInst(fvTenant, ownerKey=u'', addr=dg_mask, descr=u'', skipGwVal=u'no', ownerTag=u'', name=u'Switch-OOB_addrs')
    fvnsUcastAddrBlk = cobra.model.fvns.UcastAddrBlk(fvnsAddrInst, to=end_ip, from_=start_ip, name=u'', descr=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)
    return True

def create_oob_connGroup(md):
    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)
    infraFuncP = cobra.model.infra.FuncP(infraInfra)

    mgmtGrp = cobra.model.mgmt.Grp(infraFuncP, name=u'Switch-OOB_conngrp')
    mgmtOoBZone = cobra.model.mgmt.OoBZone(mgmtGrp, name=u'', descr=u'')
    mgmtRsAddrInst = cobra.model.mgmt.RsAddrInst(mgmtOoBZone, tDn=u'uni/tn-mgmt/addrinst-Switch-OOB_addrs')
    mgmtRsOobEpg = cobra.model.mgmt.RsOobEpg(mgmtOoBZone, tDn=u'uni/tn-mgmt/mgmtp-default/oob-default')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(infraInfra)
    md.commit(c)

    return True

def create_oob_nodeMgmt(md, system_config):
    global leaf_num
    switches = []

    for a in system_config['nodes']['switches']:
        if a[0] == 'leaf':
            leaf_num += 1
    
    # Build a list of switches to add to the OOB Management network
    if system_config['nodes']['spines']['numberbase'] and spine_num >= 1:
        firstnumber = int(system_config['nodes']['spines']['numberbase'])
        totalnumber = spine_num
        for a in range(0, totalnumber):
            switches.append(str(firstnumber + a))

    if system_config['nodes']['leafs']['numberbase'] and leaf_num >= 1:
        firstnumber = int(system_config['nodes']['leafs']['numberbase'] )
        totalnumber = leaf_num
        for a in range(0, totalnumber):
            switches.append(str(firstnumber + a))

    polUni = cobra.model.pol.Uni('')
    infraInfra = cobra.model.infra.Infra(polUni)

    mgmtNodeGrp = cobra.model.mgmt.NodeGrp(infraInfra, ownerKey=u'', name=u'Switch-OOB_nodes', ownerTag=u'', type=u'range')
    mgmtRsGrp = cobra.model.mgmt.RsGrp(mgmtNodeGrp, tDn=u'uni/infra/funcprof/grp-Switch-OOB_conngrp')

    for switch in switches:
        names = [random.choice(string.hexdigits).lower() for n in xrange(16)]
        name = ''.join(names)
        infraNodeBlk = cobra.model.infra.NodeBlk(mgmtNodeGrp, from_=switch, name=name, to_=switch)

    c = cobra.mit.request.ConfigRequest()
    c.addMo(infraInfra)
    try:
        md.commit(c)
    except cobra.mit.request.CommitError:
        error = sys.exc_info()[1]
        print ('ERROR 1 - Commit Error:{0}'.format(error))
        pass

    return True

def create_pod_policy(md):
    polUni = cobra.model.pol.Uni('')
    fabricInst = cobra.model.fabric.Inst(polUni)
    fabricFuncP = cobra.model.fabric.FuncP(fabricInst)

    # build the request using cobra syntax
    fabricPodPGrp = cobra.model.fabric.PodPGrp(fabricFuncP, ownerKey=u'', name=u'PodPolicy', descr=u'', ownerTag=u'')
    fabricRsPodPGrpBGPRRP = cobra.model.fabric.RsPodPGrpBGPRRP(fabricPodPGrp, tnBgpInstPolName=u'default')
    fabricRsTimePol = cobra.model.fabric.RsTimePol(fabricPodPGrp, tnDatetimePolName=u'default')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(fabricInst)
    md.commit(c)

def create_pod_policy_profile(md):
    polUni = cobra.model.pol.Uni('')
    fabricInst = cobra.model.fabric.Inst(polUni)
    fabricPodP = cobra.model.fabric.PodP(fabricInst, 'default')

    fabricPodS = cobra.model.fabric.PodS(fabricPodP, ownerKey=u'', name=u'default', descr=u'', ownerTag=u'', type=u'ALL')
    fabricRsPodPGrp = cobra.model.fabric.RsPodPGrp(fabricPodS, tDn=u'uni/fabric/funcprof/podpgrp-PodPolicy')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(fabricInst)
    md.commit(c)

def create_time_policy(md, system_config):
    minpoll = system_config['time']['polling']['minpoll']
    maxpoll = system_config['time']['polling']['maxpoll']
    server_list = system_config['time']['servers']

    polUni = cobra.model.pol.Uni('')
    fabricInst = cobra.model.fabric.Inst(polUni)
    datetimePol = cobra.model.datetime.Pol(fabricInst, ownerKey=u'', name=u'default', descr=u'', adminSt=u'enabled', authSt=u'disabled', ownerTag=u'')
    
    for server in server_list:
            datetimeNtpProv = cobra.model.datetime.NtpProv(datetimePol, maxPoll=maxpoll, keyId=u'0', name=server, descr=u'', preferred=u'no', minPoll=minpoll)
	
    datetimeRsNtpProvToEpg = cobra.model.datetime.RsNtpProvToEpg(datetimeNtpProv, tDn=u'uni/tn-mgmt/mgmtp-default/oob-default')
    
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fabricInst)
    md.commit(c)

def create_dns_profile(md, system_config):
    server_pref = 'yes'
    domain_def = 'yes'
    server_list = system_config['dns']['servers']
    domain_list = system_config['dns']['domains']

    polUni = cobra.model.pol.Uni('')
    fabricInst = cobra.model.fabric.Inst(polUni)

    dnsProfile = cobra.model.dns.Profile(fabricInst, ownerKey=u'', name=u'default', descr=u'', ownerTag=u'')
    dnsRsProfileToEpg = cobra.model.dns.RsProfileToEpg(dnsProfile, tDn=u'uni/tn-mgmt/mgmtp-default/oob-default')
    for server in server_list:
        dnsProv = cobra.model.dns.Prov(dnsProfile, addr=server, preferred=server_pref, name=u'')
        server_pref = 'no'
    for domain in domain_list:
        dnsDomain = cobra.model.dns.Domain(dnsProfile, isDefault=domain_def, descr=u'', name=domain)
        domain_def = 'no'

    c = cobra.mit.request.ConfigRequest()
    c.addMo(fabricInst)
    try:
        md.commit(c)
    except:
        error = sys.exc_info()[1]
        print ('ERROR 2 - Commit Error:{0}'.format(error))
        pass

    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'mgmt')
    fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', name=u'oob', descr=u'', knwMcastAct=u'permit', ownerTag=u'', pcEnfPref=u'enforced')
    dnsLbl = cobra.model.dns.Lbl(fvCtx, ownerKey=u'', tag=u'yellow-green', name=u'default', descr=u'', ownerTag=u'')

    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    try:
        md.commit(c)
    except:
        error = sys.exc_info()[1]
        print ('ERROR 3 - Commit Error:{0}'.format(error))
        pass

def build_fabric(cobra_session, system_config):
    create_bgp(cobra_session, system_config)
    print ("Created internal BGP routing.")

    create_oob_policy(cobra_session, system_config)
    print ("Created OOB Management with given IP Addresses.")

    create_time_policy(cobra_session, system_config)
    print ("Created NTP Policy.")

    create_pod_policy(cobra_session)
    print ("Created fabric pod policy for linkage.")

    create_pod_policy_profile(cobra_session)
    print ("Applied NTP and BGP policies to the system.")

    create_dns_profile(cobra_session, system_config)
    print ("Created DNS config and applied it.")
