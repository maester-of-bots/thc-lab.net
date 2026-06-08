import socket


def port_scanner(target, ports):
    open_ports = []
    closed_ports = []
    filtered_ports = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)
        elif result == 11:
            filtered_ports.append(port)
        else:
            closed_ports.append(port)

        sock.close()

    print(f"Open Ports: {open_ports}")
    print(f"Closed Ports: {closed_ports}")
    print(f"Filtered Ports: {filtered_ports}")


target = '127.0.0.1'
ports = [80, 443, 8080, 22, 3389]
port_scanner(target, ports)
