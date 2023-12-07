from analysers.semantic.semantic import Semantic
from code_generation.transpiler import Transpiler
from utils.readers import DataReader as rd


def main() -> None:
    filename = "complete"

    symbols = rd.read_symbols(filename)

    se = Semantic(symbols)
    variables = se.analyse()

    trp = Transpiler(symbols, variables)
    output = trp.transpile()

    with open(f"output/{filename}.c", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()

