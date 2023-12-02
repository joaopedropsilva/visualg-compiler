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

    @classmethod
    def check_expected_type(cls, received_type: str,  expected_type: str):
        if received_type != expected_type:
            raise e.InvalidTypeInExpression(received_type, expected_type)

    @classmethod
    def check_if_last_operand_greater_than_first(cls, first: str, last: str):
        if int(first) > int(last):
            raise e.InvalidRange

