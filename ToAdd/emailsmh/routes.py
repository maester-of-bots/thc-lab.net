from flask import Blueprint

email = Blueprint('email', __name__)
import email

import email
import re


def parse_received_headers(received_headers):
    received_servers = []
    for received in received_headers:
        # regex to extract server and IP
        match = re.search(r'from\s+(?P<server>[^\s]+)\s+\((?P<ip>[^)]+)\)', received)
        if match:
            received_servers.append(match.groupdict())
    return received_servers


def analyze_email_header(raw_email_header):
    msg = email.message_from_string(raw_email_header)
    header_keys_of_interest = ['from', 'to', 'subject', 'date', 'DKIM-Signature']
    header_info = {}
    for key in header_keys_of_interest:
        header_info[key] = msg.get(key)
    # Get all the 'Received' headers
    received_headers = msg.get_all('received')
    if received_headers:
        header_info['received'] = parse_received_headers(received_headers)
    # Get authentication results
    header_info['SPF'] = msg.get('Received-SPF')
    header_info['DMARC'] = msg.get('Authentication-Results')
    return header_info


def main():
    raw_email_header = input("Please paste the raw email header here:\n")
    result = analyze_email_header(raw_email_header)

    for key, value in result.items():
        print(f'{key}: {value}\n')


if __name__ == "__main__":
    main()
