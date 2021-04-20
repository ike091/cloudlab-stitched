"""Spins up nodes for installing a SLATE cluster split between two physical locations.

Instructions:
Wait for the profile instance to start, and then follow instructions on the SLATE website for cluster install.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as igext

# Define OS image
CENTOS7_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD'

# Create a portal context, needed to define parameters
pc = portal.Context()

# Create a Request object to start building RSpec
request = pc.makeRequestRSpec()

# Create some user-configurable parameters
pc.defineParameter('public_ip_count', 'The number of additional public IPs to allocate', portal.ParameterType.INTEGER, 2)

params = pc.bindParameters()

# Validate parameters
if params.public_ip_count < 1:
    pc.reportError(portal.ParameterError('You must allocate at least 1 additional public ip.', ['public_ip_count']))
pc.verifyParameters()

# Create a node
node1 = request.RawPC('node1')
node2 = request.RawPC('node2')

# Set node image
node1.disk_image = CENTOS7_IMG
node2.disk_image = CENTOS7_IMG

# Request a pool of dynamic publically routable ip addresses - pool name cannot contain underscores - hidden bug
addressPool = igext.AddressPool('addressPool', int(params.public_ip_count))
request.addResource(addressPool)

# Output RSpec
pc.printRequestRSpec(request)

