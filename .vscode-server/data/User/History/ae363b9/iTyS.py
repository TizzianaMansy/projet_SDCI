# Copyright (c) 2015 SONATA-NFV and Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
import logging
from time import sleep
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)


def create_topology():
    net = DCNetwork(monitor=False, enable_learning=True)

    dc1 = net.addDatacenter("dc1")
    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
    api1.connect_datacenter(dc1)
    api1.start()
    api1.connect_dc_network(net)
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.start()

    #info('*** Adding docker containers\n')
    server = net.addDocker('server', ip='10.0.0.10', mac='00:00:00:00:00:10', dimage='server:latest',dcmd='sh /app/start_server_app.sh')
    gi = net.addDocker('gi', ip='10.0.0.20', mac='00:00:00:00:00:20', dimage='gi:latest', dcmd = 'sh /app/start_gi.sh', environment={"LOCALNAME" : "gwi", "REMOTEIP" : "10.0.0.10", "REMOTENAME":"srv"})
    gf1 = net.addDocker('gf1', ip='10.0.0.30',  mac='00:00:00:00:00:30', dimage='gf:latest',  dcmd='sh /app/start_gf_device.sh', environment= {"LOCALNAMEGW":"gwf1", "REMOTEIP":"10.0.0.20","REMOTENAMEGW":"gwi","LOCALNAMEDEV":"dev1","PERIOD":10000})
    gf2 = net.addDocker('gf2', ip='10.0.0.40', dimage='gf:latest', dcmd='sh /app/start_gf_device.sh', environment= {"LOCALNAMEGW":"gwf2", "REMOTEIP":"10.0.0.20","REMOTENAMEGW":"gwi","LOCALNAMEDEV":"dev2","PERIOD":10000})
    gf3 = net.addDocker('gf3', ip='10.0.0.50', dimage='gf:latest', dcmd='sh /app/start_gf_device.sh', environment= {"LOCALNAMEGW":"gwf3", "REMOTEIP":"10.0.0.20","REMOTENAMEGW":"gwi","LOCALNAMEDEV":"dev3","PERIOD":10000})
    
    #monitor = net.addDocker('monitor', ip='10.0.0.60', dimage='monitor:latest')# dcmd='python3 /app/monitor.py')
  
    #info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    #info('*** Creating links\n')
    net.addLink(dc1, s2)
    net.addLink(gi, s2)
    net.addLink(gf1, s1)
    net.addLink(gf2, s1)
    net.addLink(gf3, s1)
    net.addLink(s2, s1)
    net.addLink(s2, server)

   # net.addLink(monitor, s2)
    #net.addLink(host, s2)

    net.start()
    net.CLI()
    # when the user types exit in the CLI, we stop the emulator
    net.stop()


def main():
    create_topology()


if __name__ == '__main__':
    main()
