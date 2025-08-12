import ipaddress


def subnet_calculator(ip_address, subnet_mask):
    network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    available_ip_range = list(network.hosts())

    print(f"Network Address: {network_address}")
    print(f"Broadcast Address: {broadcast_address}")
    print(f"Available IP Range: {available_ip_range}")


ip_address = '192.168.0.10'
subnet_mask = '255.255.255.0'
subnet_calculator(ip_address, subnet_mask)
