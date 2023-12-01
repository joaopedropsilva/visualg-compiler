
simbolos = [['algoritmo', 'algoritmo'], ['var', 'var'], 
            ['a', 'var'], ['inteiro', 'inteiro'], 
            ['b', 'var'], ['logico', 'logico'], 
            ['c', 'var'], ['real', 'real'], 
            ['d', 'var'], ['caractere', 'caractere'], 
            ['b', 'var'], ['logico', 'logico'], 
            ['f', 'var'], ['logico', 'token_invalido'], 
            ['inicio', 'inicio'], ['a', 'var'], 
            ['=', 'atrib'], ['20', 'valor'], 
            ['fimalgoritmo', 'fimalgoritmo']]

tipos_validos = ["inteiro", "real",  "caractere",  "logico"]

variaveis = {}
ultima_variavel = ""
declaracao = False

for simbolo in simbolos:
    lexema, token = simbolo[0], simbolo[1]

    if lexema == "inicio":
        declaracao = False

    if declaracao:
        classificacao = ""

        if token == "var":
            classificacao = "variavel"
            ultima_variavel = lexema
        elif token in tipos_validos:
            classificacao = "tipo"
        else:
            print(f"Definição de lexema '{lexema}' e token '{token}' incorreta")

            variaveis.popitem()
            continue

        match classificacao:
            case "variavel":
                if lexema not in variaveis.keys():
                    variaveis[lexema] = token
                else:
                    print(f"Variável '{lexema}' ({lexema}:{variaveis[lexema]}) não pode ser redeclarada")
            case "tipo":
                if variaveis[ultima_variavel] == "var":
                    variaveis[ultima_variavel] = token
    else:
        if lexema == "var":
            declaracao = True


print(variaveis)
