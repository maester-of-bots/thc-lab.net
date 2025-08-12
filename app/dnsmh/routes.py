from flask import Blueprint
from flask import render_template, request

from app.dnsmh import blueprint
from dotenv import load_dotenv
import os
import requests
import json
dns = Blueprint('dns', __name__)

load_dotenv()
key = os.getenv('virustotal')
def check_domain_reputation(domain):
    url = f'https://www.virustotal.com/api/v3/domains/{domain}'
    headers = {
        "x-apikey": key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        raw = response.json()
        data = raw['data']['attributes']
        whois = data['whois'].replace("\n","<br>")
        last_cert = data['last_https_certificate_date']



        return data
    else:
        return None


@blueprint.route('/dns.html', methods=('GET', 'POST'))
def dns():
    if request.method == 'POST':
        domain = request.form['domain']
        result = check_domain_reputation(domain)
        if result is not None:
            data = json.dumps(result, indent=4)
            return render_template('dnsmh/dns.html', data=result)
        else:
            return render_template('dnsmh/dns.html', data="Dunno man, something broke.")

    else:
        return render_template('dnsmh/dns.html')