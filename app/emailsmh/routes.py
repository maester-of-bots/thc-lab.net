import email as email_lib
import re

from flask import render_template, request

from app.emailsmh import blueprint


def _parse_received_headers(received_headers):
    servers = []
    for received in received_headers:
        match = re.search(r'from\s+(?P<server>[^\s]+)\s+\((?P<ip>[^)]+)\)', received)
        if match:
            servers.append(match.groupdict())
    return servers


def _analyze_header(raw):
    msg = email_lib.message_from_string(raw)
    info = {
        'from': msg.get('From'),
        'to': msg.get('To'),
        'subject': msg.get('Subject'),
        'date': msg.get('Date'),
        'dkim': msg.get('DKIM-Signature'),
        'spf': msg.get('Received-SPF'),
        'dmarc': msg.get('Authentication-Results'),
    }
    received = msg.get_all('received')
    if received:
        info['received'] = _parse_received_headers(received)
    return info


@blueprint.route('/email.html', methods=('GET', 'POST'))
def emailsmh():
    result = None

    if request.method == 'POST':
        raw = request.form.get('header', '').strip()
        if raw:
            result = _analyze_header(raw)

    return render_template('emailsmh/email.html', result=result)
