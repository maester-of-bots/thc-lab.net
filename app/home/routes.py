from flask import Blueprint
from flask import render_template, redirect
from flask import render_template, request, redirect, send_file, url_for, flash

from app.home import blueprint

home = Blueprint('home', __name__)

# Main page, there's nothing here...

'''
landing_data = [
    {
        'Title': "DNS Utilities",
        "Type": "Sysadmin",
        "Description": "Look up DNS info or check for someone squatting on a suspicious domain similar to yours",
        "Link": "dns.html",
        "Pic": "dns.png",
    },
    {
        'Title': "SSL Cert Utils",
        "Type": "Sysadmin",
        "Description": "Work with SSL certs and PFX files",
        "Link": "ssl.html",
        "Pic": "ssl.png",
    },
    {
        'Title': "Password Generator",
        "Type": "Security",
        "Description": "For when you hate making up passwords",
        "Link": "ass.html",
        "Pic": "ass.png",
    },
    {
        'Title': "Phone Number Utilities",
        "Type": "Information",
        "Description": "I wish there was universal caller-ID...",
        "Link": "phone.html",
        "Pic": "phone.png",
    },
    {
        'Title': "AI Stuff",
        "Type": "AI",
        "Description": "Everybody else is doing it.",
        "Link": "AI.html",
        "Pic": "AI.png",
    },
    {
        'Title': "URL Shortener",
        "Type": "Fun",
        "Description": "I fuckin' love URL shorteners!!",
        "Link": "shorts.html",
        "Pic": "url.png",
    },
    {
        'Title': "Vocal Stripping for Music",
        "Type": "AV",
        "Description": "Why do they always have to sing over the music.....",
        "Link": "vocals.html",
        "Pic": "url.png",
    },
    {
        'Title': "GitHub Repo Credential Checker",
        "Type": "Security",
        "Description": "Ever want to look through all your repos and commits for anything that looks like a password?",
        "Link": "gitpass.html",
        "Pic": "gitpass.png",
    },
    
    {
        'Title': "DnDGPT",
        "Status": "Testing",
        "Type": "Fun",
        "Description": "A website that generates D&D related things using AI.",
        "Link": "https://dndgpt.net",
    },
]
'''


landing_data = [
    {
        'Title': "URL Shortener",
        "Status": "Working",
        "Type": "Convenience",
        "Description": "I love doing URL shorteners.",
        "Link": "shorts.html",
    },
    {
        'Title': "THC's Automated Helpdesk",
        "Status": "Working",
        "Type": "Fun",
        "Description": "Click here to solve all your tech support problems!",
        "Link": "bofh.html",
    },
    {
        'Title': "What's my fucking IP?",
        "Status": "Working",
        "Type": "Info",
        "Description": "A foul-mouthed IP address checker",
        "Link": "https://whatsmyfuckingip.com",
    },
    {
        'Title': "Password Generator",
        "Status": "Working",
        "Type": "Security",
        "Description": "For when you hate making up passwords",
        "Link": "pass.html",
    },
    {
        'Title': "DNS Utilities",
        "Status": "Coming Soon",
        "Type": "Sysadmin",
        "Description": "Look up DNS info or check for someone squatting on a suspicious domain similar to yours",
        "Link": "dns.html",
    },
    {
        'Title': "GitHub Repo Credential Checker",
        "Status": "Coming Soon",
        "Type": "Dev/Sec",
        "Description": "Ever want to look through all your repos and commits for anything that looks like a password?",
        "Link": "gitpass.html",
    },
]


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html', data=landing_data)

@blueprint.route('/o9-province.html', methods=['GET'])
def o9():
    return render_template('home/o9.html')

