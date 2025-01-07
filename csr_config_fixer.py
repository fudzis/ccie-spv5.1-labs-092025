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
!"""


user_directory = input('Enter directory for CSR config to change: ')

for filename in os.listdir(user_directory):
    file_path = os.path.join(user_directory, filename)

    with open(file_path, 'r') as file:
        file_contents = file.read()

    if 'vrf definition clab-mgmt' not in file_contents:
        with open(file_path, 'w') as file:
            for line in file_contents.splitlines():
                print(line)
