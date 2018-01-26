import os
import shutil
import json
import base64
import struct
import requests
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, BranchStrings, BranchSettings, \
    CommitSettings, LogSettings, PushStrings, PushSettings, RemoteStrings
import lit.util as util


class PushCommand(BaseCommand):
    def __init__(self):
        name = PushStrings.NAME
        help_message = PushStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)
        self.user_token = ''

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        remote_url = settings_serializer.get_value(RemoteStrings.ARG_NAME_CHOICE_URL)

        if not remote_url:
            print('{0} value is not set'.format(RemoteStrings.ARG_NAME_CHOICE_URL))
            return False

        if not settings_serializer.get_value('user_token'):
            print('Run \'lit auth\' first')
            return False

        self.user_token = settings_serializer.get_value('user_token')

        # get current branch name
        current_branch_name = util.get_current_branch_name()

        branch_log_file_path = util.get_branch_log_file_path(current_branch_name)
        current_branch_commits = JSONSerializer(branch_log_file_path).get_all_from_list_item(
            LogSettings.COMMITS_LIST_KEY)

        # obtain list of necessary commits to send, get session token
        commits_hashes_to_send, session_token = self.send_available_branch_commits_hashes(
            current_branch_name, current_branch_commits)

        if not session_token:
            print('Bad server response')
            return False

        commits_logs_to_send = self.get_logs_by_commits_hashes(commits_hashes_to_send, current_branch_commits)

        # prepare package of necessary commits
        packed_commits_to_send = self.pack_commits(commits_hashes_to_send, commits_logs_to_send)

        # send packed commits using previous session token
        return self.send_commits(packed_commits_to_send, session_token, current_branch_name)

    def send_available_branch_commits_hashes(self, branch_name, branch_commits):
        commits_hashes = []
        for commit in branch_commits:
            commit_hash = commit[CommitSettings.LONG_HASH_KEY]
            commits_hashes.append(commit_hash)
        data = {'branch_name': branch_name, 'commits_hashes': commits_hashes}
        request = requests.post(
            url=PushSettings.ENDPOINT_1,
            json=data,
            headers={'Authentication': 'Token ' + self.user_token})
        if request.status_code != requests.codes.ok:
            print('Error status code')
            return [], ''
        try:
            response_json = request.json()
            commits_hashes_to_send = response_json['commits']
            session_token = response_json['session_token']
        except:
            print('Failed to parse response json')
            return [], ''

        return commits_hashes_to_send, session_token

    def get_logs_by_commits_hashes(self, commits_hashes, commits):
        commits_logs = []
        for commit in commits:
            if commit[CommitSettings.LONG_HASH_KEY] in commits_hashes:
                commits_logs.append(commit)
        return commits_logs

    def send_commits(self, packed_commits, session_token, branch_name):
        encoded_package = base64.b64encode(packed_commits).decode('utf-8')
        body = {'session_token': session_token, 'branch_name': branch_name, 'data': encoded_package}
        json_data = json.dumps(body)
        request = requests.post(
            url=PushSettings.ENDPOINT_2,
            json=json_data,
            headers={'Authentication': 'Token ' + self.user_token})
        print('Commits data sent')
        return request.status_code == requests.codes.ok

    def pack_commits(self, commits_hashes, commits_logs):
        """
        Combines commits to single package.

        Package structure:
        |package memory map (PMM) length in bytes (8 bytes)|PMM|commits json logs|commit_archive_1 (CA1)|CA2|...|CAn|

        Package memory map structure:
        {'logs':<logs length in bytes>,
         'commits':[
            <commit_1_hash>:<commit_1_length_in bytes>,
            <commit_2_hash>:<commit_2_length_in bytes>,
            ...,
            <commit_n_hash>:<commit_n_length_in bytes>
        ]}

        :param commits_logs: commits logs to pack
        :param commits_hashes: commits hashes to pack
        :return: binary package
        """

        commits_logs_bytes = json.dumps(commits_logs).encode('utf-8')

        commits_archives_bytes = bytearray()
        archives_lengths = {}
        for commit_hash in commits_hashes:
            archive_name = commit_hash[:CommitSettings.SHORT_HASH_LENGTH] + CommitSettings.FILE_EXTENSION
            archive_path = os.path.join(CommitSettings.DIR_PATH, archive_name)
            with open(archive_path, 'rb') as archive_file:
                file_bytes = archive_file.read()
                archives_lengths[commit_hash] = len(file_bytes)
                commits_archives_bytes.extend(file_bytes)

        memory_map = {'logs': len(commits_logs_bytes), 'commits': list()}
        for k, v in archives_lengths.items():
            memory_map['commits'].append({k: v})

        memory_map_bytes = json.dumps(memory_map).encode('utf-8')

        package_bytes = bytearray()
        package_bytes.extend(struct.pack('Q', len(memory_map_bytes)))
        package_bytes.extend(memory_map_bytes)
        package_bytes.extend(commits_logs_bytes)
        package_bytes.extend(commits_archives_bytes)

        return package_bytes
