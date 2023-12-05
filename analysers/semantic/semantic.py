from typing import List

from analysers.semantic.rules import VariableRules as vr, LoopRules as lr
from resources.keywords import (
    types,
    valid_tokens_for_variable_assignment,
    non_numeric_expressions,
)

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

        symbols = self.__symbols[program_start + 1: program_end]

        pos = 0
        while pos < len(symbols):
            lexem, token = symbols[pos][0], symbols[pos][1]

            match token:
                case "leia":
                    pos = self.__analyse_variable_to_read(
                            pos, symbols)
                case "var":
                    pos = \
                        self.__analyse_variable_assignment(
                                pos, symbols)
                case "se":
                    pass
                case "para":
                    pass


    def __analyse_variable_to_read(self,
                                   pos: int,
                                   symbols: List[List[str]]) -> int:
        variable_pos = pos + 2
        variable = symbols[variable_pos][0]

        vr.exists(variable, self.__variables)
        vr.is_readable(variable, self.__variables)

        return pos + 2

    def __validate_next_token(self,
                              pos: int,
                              symbols: List[List[str]],
                              expected_types: List[str]) -> int:
        lexem, token = symbols[pos][0], symbols[pos][1]

        if token in non_numeric_expressions:
            prev_token = symbols[pos - 1][1]
            if prev_token == "atrib":
                variable = symbols[pos - 2][0]
                expected_type = [self.__variables[variable]]
                received_type = "logico" if token != "msg" else "caractere"

                vr.is_type_valid(received_type, expected_type)

        if token == "var":
            prev_token = symbols[pos - 1][1]
            if  prev_token != "op_arit":
                return pos

            vr.is_type_valid(self.__variables[lexem], expected_types)

        next_token_pos = pos + 1
        if next_token_pos == len(symbols):
            return next_token_pos

        next_token = symbols[next_token_pos][1]
        if next_token not in valid_tokens_for_variable_assignment:
            return next_token_pos

        return self.__validate_next_token(next_token_pos,
                                          symbols, expected_types)

    def __analyse_variable_assignment(
            self,
            pos: int,
            symbols: List[List[str]]) -> int:
        variable_found = symbols[pos][0]

        vr.exists(variable_found, self.__variables)


        next_token_pos = pos + 2
        allowed_types_in_expression = [self.__variables[variable_found]]

        if "real" in allowed_types_in_expression:
            allowed_types_in_expression.append("inteiro")

        return self.__validate_next_token(next_token_pos,
                                          symbols,
                                          allowed_types_in_expression)

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
