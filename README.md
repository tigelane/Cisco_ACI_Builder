# ACI_Builder

**Automated deployment and configuration of Cisco ACI Application Centric Infrastructure**

* Run aci_builder.py with no arguments for help.

ACI Builder starts from a completly unconfigured ACI Fabric.  
**This script should be run imdediatly after the the APICs can be connected to via the API.**


## This script will complete the following:

* Add All Switches to the fabric
* Configure the fabric for required admin functions
* BGP, DNS, NTP, SNMP, OOB Management (with security), syslog server, and external authentication
* Configure a VMware domain and pyhsical interfaces for ESXi hosts
* Create two Tenants with associated components
* Demo Application Profiles
* L3 Gateway
* Common Filters and Contracts
