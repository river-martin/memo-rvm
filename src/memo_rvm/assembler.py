from memo_rvm.vm import Instr


def assemble(rasm_file_name: str) -> list[Instr]:
    """
    Create a list of `Instr` objects from a file containing regex assembly code.
    """
    with open(rasm_file_name) as f:
        prog = []
        for line in f:
            if line == "\n":
                continue
            line = line.replace(",", "")
            op, *args = line.split()
            prog.append(Instr(op, args))
    return prog
