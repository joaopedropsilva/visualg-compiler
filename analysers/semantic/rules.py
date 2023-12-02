from copy import deepcopy

from resources import errors as e


class Rules:
    __types = ["inteiro", "real",  "caractere",  "logico"]

    @classmethod
    def variable_exists(cls, variable: str, variables: dict):
        if variable not in variables.keys():
            raise e.VariableNotDeclared(variable)

    @classmethod
    def check_if_readable(cls, variable: str, variables: dict):
        readable_types = deepcopy(cls.__types)
        readable_types.remove("logico")

        if variables[variable] not in readable_types:
            raise e.CannotReadFromBooleanType(variable)
