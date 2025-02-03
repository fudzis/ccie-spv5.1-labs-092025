import os

clab_config = """root
!
vrf clab-mgmt
 description Containerlab management VRF (DO NOT DELETE)
 address-family ipv4 unicast
 !
!
interface MgmtEth0/0/CPU0/0
 vrf clab-mgmt
 ipv4 address 10.0.0.15 255.255.255.0
 no shutdown
!
router static
 vrf clab-mgmt
  address-family ipv4 unicast
   0.0.0.0/0 10.0.0.2
  !
 !
!
ssh server v2
ssh server vrf clab-mgmt
!
http client vrf clab-mgmt
http client source-interface ipv4 MgmtEth0/0/CPU0/0
!
line default exec-timeout 0 0
!
"""


user_directory = input('Enter directory for XRv config to change: ')

for filename in os.listdir(user_directory):
    file_path = os.path.join(user_directory, filename)

    with open(file_path, 'r') as file:
        file_contents = file.read()

    if 'vrf definition clab-mgmt' not in file_contents:
        with open(file_path, 'w') as file:
            gigabit_interfaces = []
            for line in file_contents.splitlines():
                if 'interface GigabitEthernet0/0/0' in line:
                    gigabit_interfaces.append(line.strip())

                if line.strip() == 'end':
                    file.write(clab_config)
                    continue

                file.write(line + '\n')

            for interface_line in set(gigabit_interfaces):
                file.write(interface_line + '\n')
                file.write(' no shutdown' + '\n')

            file.write('end\n')
