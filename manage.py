#!/usr/bin/env python

import re
import sys
from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

defaults = init_defaults('auth-sheep')
defaults['auth-sheep']['debug'] = False

class AuthSheep(CementApp):
    class Meta:
        label = 'auth-sheep'
        config_defaults = defaults

def main(argv):
    with AuthSheep() as app:
        app.args.add_argument('--access-key', action='store', dest='access_key')
        app.args.add_argument('--secret-key', action='store', dest='secret_key')
        app.args.add_argument('--region', action='store', dest='region')
        app.args.add_argument('--name', action='store', dest='name')
        app.args.add_argument('--description', action='store', dest='description')
        app.args.add_argument('command')
        app.args.add_argument('input_config_file')
        app.args.add_argument('output_config_file')
        app.run()
        command = app.pargs.command
        input_config_file = app.pargs.input_config_file
        output_config_file = app.pargs.output_config_file
        if command == 'init':
            region = ''
            name = ''
            description = ''
            if app.pargs.region:
                region = app.pargs.region
            else:
                region = raw_input('Region: ')
            if app.pargs.name:
                name = app.pargs.name
            else:
                name = raw_input('Name: ')
            if app.pargs.description:
                description = app.pargs.description
            else:
                description = raw_input('Description: ')
            init(input_config_file, output_config_file, region, name, description)
        elif command == 'auth':
            access_key = ''
            secret_key = ''
            if app.pargs.access_key:
                access_key = app.pargs.access_key
            else:
                access_key = raw_input('Access Key: ')
            if app.pargs.secret_key:
                secret_key = app.pargs.secret_key
            else:
                secret_key = raw_input('Secret Key: ')
            auth(input_config_file, output_config_file, access_key, secret_key)

def init(input_config_file, output_config_file, region, name, description):
    lines = []
    with open(input_config_file) as f:
        for line in f.readlines():
            matches = re.findall(r'^(region:)|(function_name:)|(description:)', line)
            if (len(matches) > 0):
                match = matches[0]
                if (len(match[0]) > 0): # region
                    line = 'region: ' + region + '\n'
                if (len(match[1]) > 0): # function_name
                    line = 'function_name: ' + name + '\n'
                if (len(match[2]) > 0): # description
                    line = 'description: ' + description + '\n'
            lines.append(line)
    with open(output_config_file, 'w') as f:
        for line in lines:
            f.write(line)

def auth(input_config_file, output_config_file, access_key, secret_key):
    lines = []
    with open(input_config_file) as f:
        for line in f.readlines():
            matches = re.findall(r'^(aws_access_key_id:)|(aws_secret_access_key:)', line)
            if (len(matches) > 0):
                match = matches[0]
                if (len(match[0]) > 0): # aws_access_key
                    line = 'aws_access_key_id: ' + access_key + '\n'
                if (len(match[1]) > 0): # aws_secret_access_key
                    line = 'aws_secret_access_key: ' + secret_key + '\n'
            lines.append(line)
    with open(output_config_file, 'w') as f:
        for line in lines:
            f.write(line)

main(sys.argv)
