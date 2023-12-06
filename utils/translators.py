from typing import List, Tuple
from resources.clang_keymap import keys

class Translators:
    @classmethod
    def translate_declaration(cls,
                              symbols: List[List[str]],
                              output: str) -> Tuple[str, int]:
        pos = 0
        while True:
            lexem, token = symbols[pos][0], symbols[pos][1]

            if token == "inicio":
                return output, pos
            elif token == "var":
                next_token = symbols[pos + 1][1]
                var_type = keys[next_token]

                output += f"{var_type} {lexem};\n"

            pos += 1



    @classmethod
    def translate_assignment(cls):
        pass
