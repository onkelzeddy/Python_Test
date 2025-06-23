class Reader:

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__opened_file = None

    @property
    def file_path(self):
        return self.__file_path

    @property
    def opened_file(self):
        return self.__opened_file

    def open_file(self):
        try:
            self.__opened_file = open(self.file_path, "r")
        except Exception as e:
            raise FileNotFoundError(e) from e

    def close_file(self):
        self.__opened_file.close()

    def __del__(self):
        if self.__opened_file:
            self.close_file()
