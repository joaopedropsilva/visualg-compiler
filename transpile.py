from typing import List

from analysers.semantic.semantic import Semantic
from resources.clang_keymap import keys
from utils.readers import DataReader as rd
from utils.translators import Translators as tr



class Transpiler:
    __stdio_include = "#include <stdio.h>\n"

    def __init__(self, symbols: List[List[str]], variables: dict) -> None:
        self.__symbols = symbols
        self.__variables = variables
        self.__output = Transpiler.__stdio_include

    def transpile(self) -> str:
        self.__transpile_main_function()
        self.__transpile_declaration_section()
        self.__transpile_remaining_code()

        self.__output += keys["fimalgoritmo"]

        return self.__output

    def __transpile_main_function(self) -> None:
        token = self.__symbols[0][1]

        if token != "algoritmo":
            raise Exception("Início de algoritmo não reconhecido")

        self.__output += keys[token]
        self.__symbols.pop(0)

    def __transpile_declaration_section(self) -> None:
        lexem, token = self.__symbols[0][0], self.__symbols[0][1]

        if token != "var":
            raise Exception("Falha ao gerar declarações de variáveis")

        if lexem != "var":
            raise Exception("Falha ao gerar declarações de variáveis")


        self.__symbols.pop(0)
        self.__output, pos_read = tr.translate_declaration(self.__symbols,
                                                           self.__output)
        self.__symbols = self.__symbols[pos_read + 1:]

    def __transpile_remaining_code(self) -> None:
        pos = 0

        while self.__symbols[pos][1] != "fimalgoritmo":
            lexem, token = self.__symbols[pos][0], self.__symbols[pos][1]

            match token:
                case "atrib":
                    variable = self.__symbols[pos - 1][0]
                    self.__output += f"{variable} = "
                    self.__output, pos = tr.translate_assignment(
                                pos + 1, self.__symbols, self.__output)
                case "leia":
                    variable = self.__symbols[pos + 2][0]
                    var_type = keys[self.__variables[variable]]

                    self.__output += 'scanf("'
                    self.__output = tr.translate_input_command(variable, var_type, self.__output)

                    pos += 3
                case _:
                    pos += 1


def main() -> None:
    filename = "atribuicao"

    symbols = rd.read_symbols(filename)
    se = Semantic(symbols)
    variables = se.analyse()

    transpiler = Transpiler(symbols, variables)

    output = transpiler.transpile()

    with open(f"{filename}.c", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()

