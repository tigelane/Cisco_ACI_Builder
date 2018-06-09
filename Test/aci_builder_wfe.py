#!/usr/bin/env python

from flask import Flask, send_from_directory, request, render_template, url_for, redirect, abort
from datetime import datetime
import sys, requests, re
import json
import ipaddress
import copy
app = Flask(__name__)

applicationTitle = "ACI Builder - Template Creator"
header_graphic_file = 'new.png'
# header_graphic_file = 'wicat-header-2.png'
style_builder_file = 'new.css'
style_bootstrap_file = 'bootstrap.min.css'
style_dataTables_bootstrap_file = 'dataTables.bootstrap.css'
aci_builder_template = 'aci_builder_template.json'

def import_config(config_file_name):
    try:
        with open(config_file_name) as json_data:
            system_config = json.load(json_data)

    except IOError:
        print ('No config file found ({0}).  Use "aci_builder_config.py --makeconfig" to create a base file.'.format(config_file_name))
        exit()

    except:
        print ('There is a syntax error with your config file.  Please use the python interactive interpreture to diagnose. (python; import {0})'.format(config_file_name))
        exit()

    return system_config

def base_menu():
    """
    Draw initial screen and menu items.
    :return: html pages as rendered html
    """
    description = ('ACI Builder')
    creds = aci.Credentials('apic', description)
    args = creds.get()
    fabric = get_fabric_friendly_name(args.url)
    header_graphic = url_for('static', filename=header_graphic_file)
    style_wu = url_for('static', filename=style_wu_file)

    #html = render_template('style.html', width=menu_width)
    html = render_template('menu_template.html', header_graphic=header_graphic, app_title=applicationTitle, style_guide=style_builder_file)
    return html

def table_header():
    """
    Should be included on all table based screens - includes the base menu
    :return: html pages as rendered html
    """

    html = base_menu()
    html += render_template('table_header.html')
    return html

def table_footer():
    """
    Should be inlcuded on all table based screens
    :return: html pages as rendered html
    """
    return  render_template('table_footer.html')

def render_error_screen(error):
    """
    Draw error screen.
    :param error: Error code
    :return: html pages as rendered html
    """
    # Takes the error as a string, returns full html page to display
    html = base_menu()
    html += render_template('error.html',
                            error=error)
    return html

@app.route('/')
def build_config_form():
    """
    Render the form to fill out from the template
    """
    html = base_menu()
    html += render_template('build_config_template.html')

    return html

@app.route('/build_config', methods=['POST'])
def build_config_post():
    """
    Render the config file from what was filled out in the form
    :return:
    """

    html = table_header()
    html += render_template('build_config_post.html', CONTRACTS=CONTRACTS)
    html += table_footer()

    return html

if __name__ == '__main__':
    app.config.update(
            DEBUG=True)

    app.run(host='0.0.0.0', port=80)
