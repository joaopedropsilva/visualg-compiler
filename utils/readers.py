class DataReader:
    @classmethod
    def read_from_file(cls, path: str):
        with open(path, "r") as file:
            return file.readlines()

