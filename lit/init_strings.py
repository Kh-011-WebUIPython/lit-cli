"""
    Run only if strings file is absent
"""
from lit.file.JSONSerializer import JSONSerializer
from lit.file.StringManager import StringManager
import lit.paths

STRINGS = {
    'COMMAND_INIT_HELP': 'Initializes repository in the current directory',
}

if __name__ == '__main__':
    strings_serializer = JSONSerializer(lit.paths.STRINGS_SERIALIZED_PATH)
    StringManager.init(strings_serializer)
    # TODO write values using single file opening
    for key, value in STRINGS.items():
        StringManager.set_string(key, value)
