from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    # Create a Mininet instance
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    # Add a remote controller
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.2', port=6633)

    # Add switches
    s1 = net.addSwitch('s1', dpid='0000000000000001')
    s2 = net.addSwitch('s2', dpid='0000000000000002')
    s3 = net.addSwitch('s3', dpid='0000000000000003')

    # Add hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    # Add links between switches
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s1, s3)

    # Add links between switches and hosts
    net.addLink(s1, h1)
    net.addLink(s3, h2)

    # Start the network
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])

    # Set OpenFlow version for switches
    s1.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    s2.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')
    s3.cmd('ovs-vsctl set Bridge s3 protocols=OpenFlow13')

    # Set the default route for hosts
    h1.cmd('ip route add default via 10.0.0.1')
    h2.cmd('ip route add default via 10.0.0.2')

    return net

if __name__ == '__main__':
    setLogLevel('info')

    # Create topology
    topology = create_topology()

    # Open Mininet CLI
    CLI(topology)

    #Stop Mininet
    topology.stop()
