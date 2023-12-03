from typing import List

from analysers.semantic.rules import VariableRules as vr, LoopRules as lr
from resources.keywords import types

class Semantic:
    """
        Classe responsável pela análise semântica do código
    """

    def __init__(self, symbols: List[List[str]]) -> None:
        self.__variables = {}
        self.__symbols = symbols
        self.__variable_declaration = False
        self.__last_variable = ""

    def analyse(self) -> None:
        self.__read_variables()

        program_start = self.__symbols.index(["inicio", "inicio"])
        program_end = self.__symbols.index(["fimalgoritmo", "fimalgoritmo"])

        program_symbols = self.__symbols[program_start + 1: program_end]

        for pos, symbol in enumerate(program_symbols):
            lexem, token = symbol[0], symbol[1]

            match token:
                case "leia":
                    variable = program_symbols[pos + 2][0]

                    self.__analyse_variable_to_read(variable)
                case "var":
                    pass
                case "se":
                    pass
                case "para":
                    pass


    def __analyse_variable_to_read(self, variable: str) -> None:
        vr.exists(variable, self.__variables)
        vr.is_readable(variable, self.__variables)

    """
        Função que percorre uma lista de símbolos e popula 
        um dict com as variáveis válidas declaradas 
    """
    def __read_variables(self) -> None:
        for symbol in self.__symbols:
            lexem, token = symbol[0], symbol[1]

            if lexem == "inicio":
                self.__variable_declaration = False

            if self.__variable_declaration:
                match token:
                    case "var":
                        self.__last_variable = lexem
                        vr.is_redeclaration(lexem, self.__variables)

                        self.__variables[lexem] = token
                    case _:
                        if token in types \
                         and self.__variables[self.__last_variable] == "var":
                            self.__variables[self.__last_variable] = token
            else:
                if lexem == "var":
                    self.__variable_declaration = True
