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

    def analyse(self) -> dict:
        self.__read_variables()

        program_start = self.__symbols.index(["inicio", "inicio"])
        program_end = self.__symbols.index(["fimalgoritmo", "fimalgoritmo"])

        symbols = self.__symbols[program_start + 1: program_end]

        pos = 0
        while pos < len(symbols):
            token = symbols[pos][1]

            match token:
                case "leia":
                    pos = self.__analyse_variable_to_read(pos, symbols)
                case "var":
                    pos = \
                        self.__analyse_variable_assignment(pos, symbols)
                case "se":
                    pos = self.__analyse_conditional(pos, symbols)
                case "para":
                    pos = self.__analyse_loop(pos, symbols)
                case _:
                    pos += 1

        return self.__variables

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

    def __analyse_variable_to_read(self,
                                   pos: int,
                                   symbols: List[List[str]]) -> int:
        variable_pos = pos + 2
        variable = symbols[variable_pos][0]

        vr.exists(variable, self.__variables)
        vr.is_readable(variable, self.__variables)

        return pos + 2

    def __validate_assignment_expression(self,
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

        return self.__validate_assignment_expression(next_token_pos,
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

        return self.__validate_assignment_expression(next_token_pos,
                                          symbols,
                                          allowed_types_in_expression)

    def __validate_logical_expression(self,
                              pos: int,
                              symbols: List[List[str]],
                              expected_types: List[str]) -> int:
        lexem, token = symbols[pos][0], symbols[pos][1]

        if token in non_numeric_expressions:
                received_type = "logico" if token != "msg" else "caractere"

                vr.is_type_valid(received_type, expected_types)

        if token == "var":
            vr.is_type_valid(self.__variables[lexem], expected_types)

        next_token_pos = pos + 1
        if next_token_pos == len(symbols):
            return next_token_pos

        next_token = symbols[next_token_pos][1]
        if next_token == "entao":
            return next_token_pos + 1

        return self.__validate_logical_expression(next_token_pos,
                                                  symbols,
                                                  expected_types)

    def __analyse_conditional(self, pos: int, symbols: List[List[str]]) -> int:
        allowed_types = ["logico"]

        expression_pos = pos + 2
        while True:
            expression_pos += 1
            token_in_expression = symbols[expression_pos][1]

            if token_in_expression == "entao":
                break
            elif token_in_expression == "compara":
                allowed_types = ["inteiro", "real"]
                break

        first_operand_pos = pos + 2

        return self.__validate_logical_expression(first_operand_pos,
                                                  symbols,
                                                  allowed_types)
    def __analyse_loop(self, pos: int, symbols: List[List[str]]) -> int:
        allowed_types = ["inteiro"]
        expression_pos = pos + 1
        loop_begin = ""
        loop_limit = ""

        variable = symbols[expression_pos][0]
        vr.is_type_valid(self.__variables[variable], allowed_types)

        while True:
            if expression_pos - pos > 9:
                break

            expression_pos += 1
            token_in_expression = symbols[expression_pos][1]

            if token_in_expression == "de":
                next_token = symbols[expression_pos + 1][1]
                lr.is_valid_loop_token(next_token)

                loop_begin = symbols[expression_pos + 1][0]
            elif token_in_expression == "ate":
                next_token = symbols[expression_pos + 1][1]
                lr.is_valid_loop_token(next_token)

                loop_limit = symbols[expression_pos + 1][0]
            elif token_in_expression == "passo":
                next_token = symbols[expression_pos + 1][1]

                lr.is_valid_loop_token(next_token)
            elif token_in_expression == "faca":
                break

        lr.is_last_operand_greater_than_first(loop_begin, loop_limit)

        return expression_pos
