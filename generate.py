"""
    Módulo principal que executa a
    análise semântica e a geração de código
"""

import os

from analysers.semantic.semantic import Semantic
from code_generation.transpiler import Transpiler
from utils.readers import DataReader as rd


def main() -> None:
    print("=" * 44)
    print("\t Visualg Transpiler to C")
    print("=" * 44)
    print("Digite o nome do arquivo (sem a extensão .txt) de exemplo"\
          " da pasta examples/ que deseja gerar")
    print(f"Arquivos disponíveis: {os.listdir('./examples')}")
    filename = input(">>> ")

    symbols = rd.read_symbols(filename)

    se = Semantic(symbols)
    variables = se.analyse()

    trp = Transpiler(symbols, variables)
    output = trp.transpile()

    if not os.path.exists("./output"):
        os.mkdir("./output")

    with open(f"output/{filename}.c", "w") as file:
        file.write(output)

    print("Geração realizada com sucesso!")
    print(f"O arquivo {filename}.c pode ser acessado na pasta output/")

if __name__ == "__main__":
    main()

