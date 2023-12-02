from analysers.semantic.rules import Rules as rl

# leitura de uma tabela de simbolos

class Semantic:
    @classmethod
    def analyse(cls):
        # existência de uma variável
        rl.variable_exists("r", { "a": "1"})
