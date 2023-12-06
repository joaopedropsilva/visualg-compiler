import os

class DataReader:
    @classmethod
    def read_symbols(cls, filename: str):
        with open(f"{os.getcwd()}/examples/{filename}.txt", "r") as file:
            return list(map(lambda x: x.replace("\n", "").split(','),
                               file.readlines()))
