#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import print_function

import argparse
import base64
import configparser
import hashlib
import sys
from os import path
from os import urandom

import pyotp

import pyperclip

__version__ = '0.0.2'

CONFIG_FILE = '.softtoken.conf'


def load_config():
    dir_path = path.join(path.expanduser('~'), CONFIG_FILE)
    cfg = configparser.SafeConfigParser()
    cfg.read(dir_path)
    return cfg


def save_config(cfg):
    dir_path = path.join(path.expanduser('~'), CONFIG_FILE)
    try:
        with open(dir_path, 'w+') as configfile:
            cfg.write(configfile)
    except Exception:
        print('ERROR: Cannot write config file')
        sys.exit(2)


def create_token(name, hash_function='sha256', digits=6, seed_length=16):
    cfg = load_config()
    if cfg.has_section(name):
        print('Token %s already exists. Delete it first' % name)
        sys.exit(2)

    seed = pyotp.random_base32(length=seed_length)

    cfg.add_section(name)
    cfg.set(name, 'hash_function', hash_function)
    cfg.set(name, 'digits', str(digits))
    cfg.set(name, 'seed', seed)

    save_config(cfg)

    print('\nNew Token created:\n\n%s\n-------------' % name)
    print('Seed (hex): %s\n' % base64.b32decode(seed).hex())
    print('Seed (b32): %s\n' % seed)


def delete_token(name):
    cfg = load_config()
    if not cfg.has_section(name):
        print('Token %s does not exist' % name)
        sys.exit(2)
    cfg.remove_section(name)
    save_config(cfg)
    print("Token %s successfully deleted" % name)


def print_tokens():
    cfg = load_config()
    for section in cfg.sections():
        print("[*] %s" % section)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--new', action='store_true', default=False,
                        dest='new_token', help='Generate a new Soft Token')
    parser.add_argument('--delete', action='store_true', default=False,
                        dest='delete_token', help='Delete a Soft Token')
    parser.add_argument('--list', action='store_true', default=False,
                        dest='list_tokens', help='List configured tokens')
    parser.add_argument('--token', '-t', required=False, dest='token_name',
                        help='Soft Token name')
    parser.add_argument('--hash', default='sha256', dest='hash_function',
                        choices=('sha1', 'sha256', 'sha512'), help='Hash '
                        'function to use (default is sha256)')
    parser.add_argument('--digits', '-d', type=int, default=6, dest='digits',
                        help='OTP Length (default is 6)')
    parser.add_argument('--length', '-l', type=int, default=16,
                        dest='seed_length', help='Seed length in bytes '
                        '(default is 16)')
    parser.add_argument('-X', action='store_true', default=False,
                        dest='print_focus', help='Output the OTP where '
                        'the current focus is')
    parser.add_argument('-C', action='store_true', default=False,
                        dest='copy_clipboard', help='Copy OTP to clipboard')

    args = parser.parse_args()

    if args.list_tokens:
        print_tokens()
        sys.exit(0)

    if args.token_name is None:
        print("A Token name is required for this action")
        parser.print_help()
        sys.exit(-1)

    if args.new_token:
        create_token(args.token_name,
                     args.hash_function,
                     args.digits,
                     args.seed_length)
        sys.exit(0)

    if args.delete_token:
        delete_token(args.token_name)
        sys.exit(0)

    if args.list_tokens:
        print_tokens()
        sys.exit(0)

    # Generate new OTP if the token exists
    cfg = load_config()
    if not cfg.has_section(args.token_name):
        print('Token %s does not exist' % args.token_name)
        sys.exit(2)

    hash_function = cfg.get(args.token_name, 'hash_function')
    if hash_function == 'sha1':
        hf = hashlib.sha1
    elif hash_function == 'sha256':
        hf = hashlib.sha256
    elif hash_function == 'sha512':
        hf = hashlib.sha512

    seed = cfg.get(args.token_name, 'seed')
    totp = pyotp.TOTP(seed, digest=hf, digits=args.digits)

    otp = totp.now()

    if args.print_focus:
        from pykeyboard import PyKeyboard
        k = PyKeyboard()
        k.type_string(otp)
    elif args.copy_clipboard:
        pyperclip.copy(otp.encode('ascii'))
    else:
        print(otp)


if __name__ == "__main__":
    main()
