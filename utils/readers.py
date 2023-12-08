import os

class DataReader:
    """
        Classe acessória para leitura de dados
    """

    @classmethod
    def read_symbols(cls, filename: str):
        """
            Função que lê um arquivo em examples com os
            símbolos a reconhecer e converte em uma lista
            de listas com duas strings cada representando
            um lexema e um token, respectivamente
        """

        with open(f"{os.getcwd()}/examples/{filename}.txt", "r") as file:
            return list(map(lambda x: x.replace("\n", "").split(','),
                               file.readlines()))
