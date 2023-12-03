class CannotRedeclareVariable(Exception):
    def __init__(self, variable: str):
        self.__variable = variable

    def __str__(self):
        return f'Não é possível redeclarar a variável "{self.__variable}"'

class VariableNotDeclared(Exception):
    def __init__(self, variable: str):
        self.__variable = variable

    def __str__(self):
        return f'Variável "{self.__variable}" não declarada'

class CannotReadFromBooleanType(Exception):
    def __init__(self, variable: str):
        self.__variable = variable

    def __str__(self):
        return f'Não é possível ler da variável "{self.__variable}" ' \
                'de tipo "logico"'

class InvalidTypeInExpression(Exception):
    def __init__(self, received_type: str, expected_type: str):
        self.__type = received_type
        self.__expected = expected_type

    def __str__(self):
        return f'Variável de tipo "{self.__type}" não ' \
            'pode ser utilizada na expressão, ' \
            f'era esperado um tipo "{self.__expected}"'

class InvalidRange(Exception):
    def __str__(self):
        return f'Primeiro operando no laço "para" deve ser menor ' \
                'ou igual que o segundo operando'

