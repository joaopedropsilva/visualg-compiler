from typing import List, Tuple
from resources.clang_keymap import keys
from resources.keywords import valid_tokens_for_variable_assignment, non_numeric_expressions

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
    def translate_assignment(cls,
                             pos: int,
                             symbols: List[List[str]],
                             output: str) -> Tuple[str, int]:
        return cls.__translate_expression(pos, symbols, output)
        
    @classmethod
    def __translate_expression(cls, 
                               pos: int, 
                               symbols: List[List[str]],
                               output: str) -> Tuple[str, int]:
        lexem, token = symbols[pos][0], symbols[pos][1]

        if token not in valid_tokens_for_variable_assignment\
            and token not in non_numeric_expressions:
            output += ";\n"

            return output, pos - 1

        if token == "var":
            next_token = symbols[pos + 1][1]

            if next_token == "atrib":
                output += ";\n"
                return output, pos - 1

            output += f"{lexem} "

            output, pos = cls.__translate_expression(pos + 1, symbols, output)
            return output, pos

        if token == "op_arit"\
                or token == "valor"\
                or token == "("\
                or token == ")":
            output += f"{lexem} "

            output, pos = cls.__translate_expression(pos + 1, symbols, output)
            return output, pos

        if token == "msg":
            output += f'"{lexem}" '

            output, pos = cls.__translate_expression(pos + 1, symbols, output)
            return output, pos

        output += f"{keys[token]} "

        output, pos = cls.__translate_expression(pos + 1, symbols, output)
        return output, pos

    @classmethod
    def translate_input_command(cls,
                                variable: str,
                                var_type: str,
                                output: str) -> str:
        match var_type:
            case "int":
                output += f'%d", &{variable});\n'
            case "float":
                output += f'%f", &{variable});\n'
            case "char*":
                output += f'%s", {variable});\n'

        return output

    @classmethod
    def translate_conditional(cls,
                              pos: int,
                              symbols: List[List[str]],
                              output: str) -> Tuple[str, int]:
        return cls.__translate_logical_expression(pos, symbols, output)

    @classmethod
    def __translate_logical_expression(cls,
                                       pos: int,
                                       symbols: List[List[str]],
                                       output: str) -> Tuple[str, int]:
        lexem, token = symbols[pos][0], symbols[pos][1]

        if token == "entao":
            output += keys[token]

            return output, pos

        if token in non_numeric_expressions:
            output += f"{keys[token]} "

            output, pos = cls.__translate_logical_expression(pos + 1, symbols, output)
            return output, pos

        output += f"{lexem} "

        output, pos = cls.__translate_logical_expression(pos + 1, symbols, output)
        return output, pos

    @classmethod
    def translate_loop(cls,
                       pos: int,
                       symbols: List[List[str]],
                       output: str) -> Tuple[str, int]:
        variable = symbols[pos + 1][0]

        while True:
            lexem, token = symbols[pos][0], symbols[pos][1]

            match token:
                case "faca":
                    output += f'{variable}++ {keys[token]}'
                    break
                case "valor":
                    output += f"{lexem}; "
                case "ate":
                    output += f"{variable} < "

            pos += 1

        return output, pos
