import os
import yaml

user_directory = input('Enter directory for XRd config to change: ')
clab_directory = os.path.abspath(os.path.join(user_directory, '..', '..'))

node_name = os.path.basename(os.path.normpath(user_directory))

for filename in os.listdir(clab_directory):
    if filename.endswith('.clab.yml'):
        with open(os.path.join(clab_directory, filename), 'r') as file:
            clab_topology = yaml.safe_load(file)
clab_nodes = [{"name": key, **value} for key, value in clab_topology["topology"]["nodes"].items()]

for node in clab_nodes:
    if node['name'] == node_name:
        mgmt_ip = node['mgmt-ipv4']

clab_config = f"""hostname {node_name}
username clab
 group root-lr
 group cisco-support
 secret 10 $6$KIdSE0Je5Yu/7E0.$OJR/sA.gFWARhit.mnQLH0sKeAde8.KgNZM5yz8i/qKgClEQk9PJ0c6Ltq/tpr3.3AzxhS37b6.UbomuaVYLg.
!
line default
 transport input ssh
 exec-timeout 0 0
!
vrf clab-mgmt
 description Containerlab management VRF (DO NOT DELETE)
 address-family ipv4 unicast
 !
!
interface MgmtEth0/RP0/CPU0/0
 vrf clab-mgmt
 ipv4 address {mgmt_ip} 255.255.255.0
 no shutdown
!
router static
 vrf clab-mgmt
  address-family ipv4 unicast
   0.0.0.0/0 10.200.255.1
  !
 !
!
ssh server v2
ssh server vrf clab-mgmt
!
http client vrf clab-mgmt
http client source-interface ipv4 MgmtEth0/RP0/CPU0/0
!
"""

for filename in os.listdir(user_directory):
    file_path = os.path.join(user_directory, filename)

    with open(file_path, 'r') as file:
        file_contents = file.read()

    if 'vrf clab-mgmt' not in file_contents:
        with open(file_path, 'w') as file:
            gigabit_interfaces = []
            for line in file_contents.splitlines():
                if 'interface GigabitEthernet0/0/0' in line:
                    gigabit_interfaces.append(line.strip().split('.')[0])

                if line.strip() == 'end':
                    file.write(clab_config)
                    continue

                file.write(line + '\n')

            for interface_line in set(gigabit_interfaces):
                file.write(interface_line + '\n')
                file.write(' no shutdown' + '\n')

            file.write('end\n')
