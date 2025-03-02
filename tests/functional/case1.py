# autopep8: off
import argparse
import json
import sys
sys.path.append('/home/eliaquim/Documents/individual_projects/python-mantis')

import mantis
# autopep8: on

MANTIS_URL = ''


def configure_args():
    parser = argparse.ArgumentParser(description='MantisBT test case 1')
    parser.add_argument(
        '-c', '--config', help='Config test file', default=False)
    parser.add_argument('-u', '--url', help='MantisBT URL', default=False)
    parser.add_argument('-t', '--token', dest='user_api_token',
                        help='User API Token', default=False)

    return parser


def load_configuration_file(file):
    with open(file, 'r') as f:
        config = json.load(f)

    return config


def parser_args(parser):
    args = parser.parse_args()

    if args.config:
        args = load_configuration_file(args.config)
        if not ('url' in args and 'user_api_token' in args):
            parser.print_help()
            exit(1)

    elif args.url and args.user_api_token:
        args = vars(args)
        args.pop('config')
    else:
        parser.print_help()
        exit(1)

    return args


if '__main__' in __name__:
    parser = configure_args()
    args = parser_args(parser)

    client = mantis.MantisBT(**args)
    print(f'client_object: {client}',
          f'client._auth: {client._auth}',
          f'client._base_url: {client._base_url}',
          f'client.protocol: {client.protocol}',
          sep='\n')

    lista = client.project.list()
    print(lista)
    print(dir(lista))
