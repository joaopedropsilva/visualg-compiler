class VariableNotDeclared(Exception):
    def __init__(self, variable: str):
        self.__variable = variable

    def __str__(self):
        return f'Variável "{self.__variable}" não declarada'


