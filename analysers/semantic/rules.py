from resources import errors as e

class Rules:
    @classmethod
    def variable_exists(cls, variable: str, variables: dict):
        if variable not in variables.keys():
            raise e.VariableNotDeclared(variable)

