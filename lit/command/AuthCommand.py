import os
import json
import requests
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, BranchStrings, BranchSettings, RemoteStrings, AuthStrings, AuthSettings
import lit.util as util


class AuthCommand(BaseCommand):
    def __init__(self):
        name = AuthStrings.NAME
        help_message = AuthStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        remote_url = settings_serializer.get_value(RemoteStrings.ARG_NAME_CHOICE_URL)
        if not remote_url:
            print('Run \'lit remote set url\' command first')
            return False
        remote_url = os.path.join(remote_url, AuthSettings.ENDPOINT_SUFFIX)
        print('Authorization for remote {0}'.format(remote_url))
        username = input('Enter login: ')
        password = input('Enter password: ')

        payload = {'username': username, 'password': password}

        response = requests.post(url=remote_url, json=payload)

        if response.status_code == 400:
            print('Error', end='')
            response_json = response.json()
            if 'non_field_errors' in response_json:
                print(': ' + response_json['non_field_errors'][0])
            else:
                print()
            return False
        elif response.status_code == requests.codes.ok:
            response_json = response.json()
            if 'key' in response_json:
                user_token = response_json['key']
                settings_serializer.set_value('user_token', user_token)
                print('OK')
                return True
            else:
                print('\'token\' key not found')
                return False
        else:
            return False
        # print(str(response) + os.linesep + response.text)
