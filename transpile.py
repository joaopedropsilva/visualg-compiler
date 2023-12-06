from typing import List

from resources.clang_keymap import keys
from utils.readers import DataReader as rd
from utils.translators import Translators as tr



class Transpiler:
    __stdio_include = "#include <stdio.h>\n"

    def __init__(self, symbols: List[List[str]]) -> None:
        self.__symbols = symbols
        self.__output = Transpiler.__stdio_include

    def transpile(self) -> str:
        self.__transpile_main_function()
        self.__transpile_declaration_section()

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


def main() -> None:
    transpiler = Transpiler(rd.read_symbols("simple"))

    output = transpiler.transpile()

    with open("code.c", "w") as file:
        file.write(output)

if __name__ == "__main__":
    main()

