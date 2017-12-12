"""
    Run only if strings file is absent or needs an update
"""
from lit.file.JSONSerializer import JSONSerializer
from lit.file.SettingsManager import SettingsManager
import lit.paths

SETTINGS = {
    'INIT_LIT': lit.paths.DIR_PATH,
    'INIT_LIT_INITED': 'LIT has been already inited in this directory',
    'INIT_COMMIT_DIR': 'commits',
    'INIT_TRACKED_FILE': 'tracked_files.json',
    'INIT_COMMIT_LOG': 'commits_log.json',
    'INIT_TRACKED_FILE_INIT': '{"files": []}',
    'INIT_COMMIT_LOG_INIT': '{"commits":[]}',


    'TRACKED_FILE_PATH': '.lit/tracked_files.json',
    'COMMIT_LOG_PATH': '.lit/commits_log.json',



    'LOG_COMMIT': 'Commit: ',
    'LOG_COMMIT_MESSAGE': 'Commit message: ',
    'LOG_USERNAME': 'Username: ',
    'LOG_DATE': 'Date: ',



    'COMMIT_FILES_IN_COMMIT_DIR': '.lit/commits/',
    'COMMIT_ZIP_FILE_NAME': '.lit/commits/hash',
    'COMMIT_ZIP_EXTENCION': '.zip',
    'COMMIT_USER': 'user',
    'COMMIT_LONG_HASH': 'long_hash',
    'COMMIT_SHORT_HASH': 'short_hash',
    'COMMIT_DATETIME': 'datetime',
    'COMMIT_COMMENT': 'comment',


}

if __name__ == '__main__':
    settings_serializer = JSONSerializer(lit.paths.SETTINGS_PATH)
    SettingsManager.init(settings_serializer)
    for k, v in SETTINGS.items():
        SettingsManager.set_var_value(k, v)
