import os
import shutil
import json
import base64
import struct
import requests
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, BranchStrings, BranchSettings, \
    CommitSettings, LogSettings, PullStrings, PullSettings, PushStrings, PushSettings, RemoteStrings
import lit.util as util


class PullCommand(BaseCommand):
    def __init__(self):
        name = PullStrings.NAME
        help_message = PullStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)
        self.user_token = None
        self.endpoint = None

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        remote_url = settings_serializer.get_value(RemoteStrings.ARG_NAME_CHOICE_URL)

        if not remote_url:
            print('Run \'lit remote set {0}\' first'.format(RemoteStrings.ARG_NAME_CHOICE_URL))
            return False

        remote_repo_id = settings_serializer.get_value(RemoteStrings.ARG_NAME_CHOICE_REPO_ID)

        if not remote_repo_id:
            print('Run \'lit remote set {0}\' first'.format(RemoteStrings.ARG_NAME_CHOICE_REPO_ID))
            return False

        self.endpoint = os.path.join(remote_url, PullSettings.ENDPOINT_SUFFIX_FMT.format(remote_repo_id))

        self.user_token = settings_serializer.get_value('user_token')

        if not self.user_token:
            print('Run \'lit auth\' first')
            return False

        # get current branch name
        current_branch_name = util.get_current_branch_name()

        branch_log_file_path = util.get_branch_log_file_path(current_branch_name)
        current_branch_commits = JSONSerializer(branch_log_file_path).get_all_from_list_item(
            LogSettings.COMMITS_LIST_KEY)

        commits_hashes = []
        for commit in current_branch_commits:
            commit_hash = commit[CommitSettings.LONG_HASH_KEY]
            commits_hashes.append(commit_hash)
        json_data = {'branch_name': current_branch_name, 'commits_hashes': commits_hashes}
        request = requests.post(
            url=self.endpoint,
            json=json_data,
            headers={'Authentication': 'Token ' + self.user_token})
        if request.status_code != requests.codes.ok:
            print('Error' + os.linesep + request.content)
            return False
        try:
            response_json = request.json()
            response_data = response_json['data']
        except:
            print('Failed to get json from response')
            return False

        return self.unpack_commits(response_data, CommitSettings.DIR_PATH, branch_log_file_path)

    def unpack_commits(self, data, unpacked_commits_archives_path, log_file_path):
        """
        Unpacks commits from package.

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

        :param data: base64 encoded binary data
        :param unpacked_commits_archives_path: path where to place commits archives
        :param log_file_path: path to log file where to append commits logs
        :return: success (True) or not (False)
        """

        data = base64.b64decode(data)

        try:
            pmm_len = struct.unpack('Q', data[:8])[0]
        except struct.error:
            print('Failed to get PMM length')
            return False

        try:
            pmm = json.loads(data[8:8 + pmm_len].decode('utf-8'))
            logs_len = pmm['logs']
            commits_hashes_and_len = pmm['commits']

            commits_logs = json.loads(data[8 + pmm_len: 8 + pmm_len + logs_len].decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print('Failed to parse json')
            return False

        try:
            archives_start_offset = 8 + pmm_len + logs_len
            last_offset = archives_start_offset

            for item in commits_hashes_and_len:
                pair = item.popitem()
                commit_hash = pair[0]
                commit_len = pair[1]
                commit_name = commit_hash[:CommitSettings.SHORT_HASH_LENGTH] + CommitSettings.FILE_EXTENSION
                commit_path = os.path.join(unpacked_commits_archives_path, commit_name)
                with open(os.path.join(commit_path), 'wb') as file:
                    file.write(data[last_offset: last_offset + commit_len])
                last_offset = last_offset + commit_len
        except:
            print('Failed to unpack archives')
            return False

        existing_commits_logs_serializer = JSONSerializer(log_file_path)
        for new_commit in commits_logs:
            existing_commits_logs_serializer.append_to_list_item(LogSettings.COMMITS_LIST_KEY, new_commit)

        return True
