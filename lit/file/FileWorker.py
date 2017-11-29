class FileWorker():
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_object = open(self.__file_path, 'r+')

    def __del__(self):
        self.__file_object.close()

    def __enter__(self):
        return self.__file_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type != None or exc_val != None or exc_tb != None:
            print('Exception happened:\n' + exc_type + '\n' + exc_val + '\n' + exc_tb)
            return False
        return True
