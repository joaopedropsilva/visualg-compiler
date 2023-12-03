from typing import List

from analysers.semantic.rules import Rules as rl
from resources.keywords import types

class Semantic:
    """
        Classe responsável pela análise semântica do código
    """

    def __init__(self, symbols: List[List[str]]) -> None:
        self.__variables = {}
        self.__last_variable = ""
        self.__declaration = False
        self.__symbols = symbols

    def analyse(self) -> None:
        #rl.variable_exists("r", { "a": "1"})
        #rl.check_if_readable("a", { "a": "logico"})
        #rl.check_expected_type("inteiro", "logico")
        #rl.check_if_last_operand_greater_than_first("10", "5")
        pass

    """
        Função que percorre uma lista de símbolos e popula 
        um dict com as variáveis válidas declaradas 
    """
    def read_variables(self) -> None:
        for symbol in self.__symbols:
            lexem, token = symbol[0], symbol[1]

            if lexem == "inicio":
                self.__declaration = False

            if self.__declaration:
                match token:
                    case "var":
                        self.__last_variable = lexem
                        rl.check_variable_redeclaration(lexem, self.__variables)

                        self.__variables[lexem] = token
                    case _:
                        if token in types \
                         and self.__variables[self.__last_variable] == "var":
                            self.__variables[self.__last_variable] = token
            else:
                if lexem == "var":
                    self.__declaration = True
