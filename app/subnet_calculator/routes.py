from flask import render_template, request
import ipaddress

from app.subnet_calculator import blueprint


@blueprint.route('/subnet.html', methods=('GET', 'POST'))
def subnet():
    result = None
    error = None

    if request.method == 'POST':
        ip = request.form.get('ip', '').strip()
        mask = request.form.get('mask', '').strip()
        try:
            network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
            hosts = list(network.hosts())
            result = {
                'network': str(network),
                'network_address': str(network.network_address),
                'broadcast_address': str(network.broadcast_address),
                'num_hosts': len(hosts),
                'first_host': str(hosts[0]) if hosts else 'N/A',
                'last_host': str(hosts[-1]) if hosts else 'N/A',
                'prefix_length': network.prefixlen,
                'netmask': str(network.netmask),
            }
        except ValueError as e:
            error = str(e)

    return render_template('subnet_calculator/subnet.html', result=result, error=error)
