class FileWorker():
    def __init__(self, file_path):
        self.__file_path = file_path
        try:
            __file_object = open(self.file_path, 'r')
        except FileNotFoundError:
            '''If file was not found, create an empty file'''
            __file_object = open(self.file_path, 'w')
        __file_object.close()

    @property
    def file_path(self):
        return self.__file_path
