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

        # get current branch name
        current_branch_name = util.get_current_branch_name()

        # obtain list of necessary commits to send, get session token
        commits_hashes_to_send, session_token = self.send_available_branch_commits_hashes(current_branch_name)

        if not session_token:
            print('Bad server response')
            return False

        # prepare package of necessary commits
        packed_commits_to_send = self.pack_commits(commits_hashes_to_send)

        # send packed commits using previous session token
        self.send_commits(packed_commits_to_send, session_token)

    def send_available_branch_commits_hashes(self, branch_name):
        branch_log_file_path = util.get_branch_log_file_path(branch_name)
        commits = JSONSerializer(branch_log_file_path).get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
        commits_hashes = []
        for commit in commits:
            commit_hash = commit[CommitSettings.LONG_HASH_KEY]
            commits_hashes.append(commit_hash)
        json_data = json.dumps({'branch_name': branch_name, 'commits_hashes': commits_hashes})
        request = requests.post(url=PushSettings.ENDPOINT, json=json_data)
        if request.status_code != requests.codes.ok:
            return [], ''
        try:
            response_json = request.json()
            commits_hashes_to_send = response_json['commits_hashes']
            session_token = response_json['session_token']
        except:
            return [], ''
        return commits_hashes_to_send, session_token

    def send_commits(self, packed_commits, session_token):
        encoded_package = base64.b64encode(packed_commits)
        body = {'session_token': session_token, 'data': encoded_package}
        json_data = json.dumps(body)
        request = requests.post(url=PushSettings.ENDPOINT, json=json_data)
        return True if request.status_code == requests.codes.ok else False

    def pack_commits(self, commits_logs, commits_hashes):
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

        commits_logs_bytes = commits_logs.encode('utf-8')

        commits_archives_bytes = bytearray()
        archives_lengths = {}
        for commit_hash in commits_hashes:
            archive_name = commit_hash + CommitSettings.FILE_EXTENSION
            archive_path = os.path.join(CommitSettings.DIR_PATH, archive_name)
            with open(archive_path, 'rb') as archive_file:
                file_bytes = archive_file.read()
                archives_lengths[commit_hash] = len(file_bytes)
                commits_archives_bytes.extend(file_bytes)

        memory_map = {'logs': len(commits_logs_bytes), 'commits': list()}
        for k, v in archives_lengths:
            memory_map['commits'].append({k: v})

        memory_map_bytes = json.dumps(memory_map).encode('utf-8')

        package_bytes = bytearray()
        package_bytes.extend(struct.pack('Q', len(memory_map_bytes)))
        package_bytes.extend(memory_map_bytes)
        package_bytes.extend(commits_logs_bytes)
        package_bytes.extend(commits_archives_bytes)

        return package_bytes