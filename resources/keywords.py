types = ["inteiro", "real",  "caractere",  "logico"]

aritmethic_types = [t for t in types if \
                    t != "caractere" and t != "logico"]

valid_tokens_for_variable_assignment = [
    "var",
    "valor",
    "op_arit",
    "(",
    ")",
]
