# autopep8: off
import argparse
import json
from os import path
import sys

project_path = path.join(path.abspath(__file__).rsplit(path.sep, 3)[0])
sys.path.append(project_path)

import mantis
# autopep8: on


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

    print('### MantisBT Client Object ###')
    client = mantis.MantisBT(**args)
    print(f'client_object: {client}',
          f'client._auth: {client._auth}',
          f'client._base_url: {client._base_url}',
          f'client.protocol: {client.protocol}',
          sep='\n')

    print('\n\n\n### Projects ###')
    projects = client.projects.get_all()
    print('FOR LOG OVER PROJECTS LIST')
    for project in projects:
        print(f'    - {project}')
    print(f'projects list: {projects}',
          f'projects sorted by name: {projects.sort(key="name")}',
          f'dir of first project obj: {dir(projects[0])}',
          f'dict of first project: {projects[0].to_dict()}',
          f'first project > second project?: {projects[0] > projects[1]}',
          f'first project id: {projects[0]._id} vs second project id: {projects[1]._id}',
          sep='\n')

    print('\n\n\n### Issues ###')
    issues = projects[0].get_issues()
    print(f'issues list: {issues}',
          f'dir of first issue obj: {dir(issues[0])}',
          f'dict of first issue: {issues[0].to_dict()}',
          f'first issue > second issue?: {issues[0] > issues[1]}',
          f'first issue id: {issues[0]._id} vs second issue id: {issues[1]._id}',
          sep='\n')

    print('\n\n\n### Notes ###')
    notes = issues[0].get_notes()
    print(f'notes list: {notes}',
          f'dir of first note obj: {dir(notes[0])}',
          f'dict of first note: {notes[0].to_dict()}',
          f'first note > second note?: {notes[0] > notes[1]}',
          f'first note id: {notes[0]._id} vs second note id: {notes[1]._id}',
          sep='\n')

    original_note = notes[0]

    fake_note = client.notes._obj_cls(
        client.notes, {'id': original_note._id, 'text': 'fake note'})
    print(f'fake note in notes? {fake_note in notes}',
          f'original_note hash_string: {original_note._hash_string()}',
          f'fake_note hash_string    : {fake_note._hash_string()}',
          sep='\n')
