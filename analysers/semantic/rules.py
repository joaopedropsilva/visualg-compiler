from copy import deepcopy
from typing import List

from resources import errors as e
from resources.keywords import types

class VariableRules:
    """
        Classe mantenedora das regras
        utilizadas pela análise semântica
    """
    @classmethod
    def is_redeclaration(cls, variable: str, variables: dict):
        if variable in variables.keys():
            raise e.CannotRedeclareVariable(variable)

    @classmethod
    def exists(cls, variable: str, variables: dict):
        if variable not in variables.keys():
            raise e.VariableNotDeclared(variable)

    @classmethod
    def is_readable(cls, variable: str, variables: dict):
        readable_types = deepcopy(types)
        readable_types.remove("logico")

        if variables[variable] not in readable_types:
            raise e.CannotReadFromBooleanType(variable)

    @classmethod
    def is_type_valid(cls, received_type: str,  expected_types: List[str]):
        if received_type not in expected_types:
            raise e.InvalidTypeInExpression(received_type, expected_types)

class LoopRules:
    @classmethod
    def is_last_operand_greater_than_first(cls, first: str, last: str):
        if int(first) > int(last):
            raise e.InvalidRange

    @classmethod
    def is_valid_loop_token(cls, token: str):
        if token != "valor":
            raise e.InvalidTypeInLoopControllers
