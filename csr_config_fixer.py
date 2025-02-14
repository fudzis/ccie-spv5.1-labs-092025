import os

clab_config = """vrf definition clab-mgmt
 description Containerlab management VRF (DO NOT DELETE)
 !
 address-family ipv4
 exit-address-family
!
ip domain name example.com
!
username admin privilege 15 password 0 admin
!
interface GigabitEthernet1
 vrf forwarding clab-mgmt
 ip address 10.0.0.15 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
ip http client source-interface GigabitEthernet1
ip tftp source-interface GigabitEthernet1
ip route vrf clab-mgmt 0.0.0.0 0.0.0.0 10.0.0.2
!
"""


user_directory = input('Enter directory for CSR config to change: ')

for filename in os.listdir(user_directory):
    file_path = os.path.join(user_directory, filename)

    with open(file_path, 'r') as file:
        file_contents = file.read()

    if 'vrf definition clab-mgmt' not in file_contents:
        with open(file_path, 'w') as file:
            clab_config_added = False
            line_num = 0
            skip_count = 0
            for line in file_contents.splitlines():
                if not line.startswith('!') and not clab_config_added and line_num != 0:
                    file.write(clab_config)
                    clab_config_added = True
                line = line.replace('GigabitEthernet9', 'GigabitEthernet10')
                line = line.replace('GigabitEthernet8', 'GigabitEthernet9')
                line = line.replace('GigabitEthernet7', 'GigabitEthernet8')
                line = line.replace('GigabitEthernet6', 'GigabitEthernet7')
                line = line.replace('GigabitEthernet5', 'GigabitEthernet6')
                line = line.replace('GigabitEthernet4', 'GigabitEthernet5')
                line = line.replace('GigabitEthernet3', 'GigabitEthernet4')
                line = line.replace('GigabitEthernet2', 'GigabitEthernet3')
                line = line.replace('GigabitEthernet1', 'GigabitEthernet2')

                if skip_count == 0 and line.strip() == 'line vty 0 4':
                    file.write(line + '\n')
                    file.write(' login local\n')
                    file.write(' transport input all\n')
                    skip_count = 2
                elif skip_count > 0:
                    skip_count -= 1
                else:
                    file.write(line + '\n')

                line_num += 1

                if 'interface GigabitEthernet' in line:
                    file.write(' no shutdown' + '\n')
