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
        app.args.add_argument('--access-key', action='store_true', dest='access_key')
        app.args.add_argument('--secret-key', action='store_true', dest='secret_key')
        app.args.add_argument('example_config_file')
        app.args.add_argument('config_file')
        app.run()
        example_config_file = app.pargs.example_config_file
        config_file = app.pargs.config_file
        access_key = ''
        secret_key = ''
        if app.pargs.access_key and app.pargs.secret_key:
            access_key = app.pargs.access_key
            secret_key = app.pargs.secret_key
        else:
            access_key = raw_input('Access Key: ')
            secret_key = raw_input('Secret Key: ')
        auth(example_config_file, config_file, access_key, secret_key)

def auth(example_config_file, config_file, access_key, secret_key):
    lines = []
    with open(example_config_file) as f:
        for line in f.readlines():
            matches = re.findall(r'^(aws_access_key_id:)|(aws_secret_access_key:)', line)
            if (len(matches) > 0):
                match = matches[0]
                if (len(match[0]) > 0): # aws_access_key
                    line = 'aws_access_key_id: ' + access_key + '\n'
                if (len(match[1]) > 0): # aws_secret_access_key
                    line = 'aws_secret_access_key: ' + secret_key + '\n'
            lines.append(line)
    with open(config_file, 'w') as f:
        for line in lines:
            f.write(line)

main(sys.argv)
