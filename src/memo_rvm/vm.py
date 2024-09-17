import numpy as np


class Instr:
    """An instruction for the regex virtual machine (VM)."""

    def __init__(self, op: str, args: list[str]):
        self.op = op
        self.args = args

    def __repr__(self):
        return f"{self.op} {', '.join(self.args)}".strip()


class Thread:
    """A metaphorical thread for the VM to execute."""

    def __init__(
        self, ip, sp, saved_sps: np.ndarray, eps_sps: np.ndarray, eps_stack: list[int]
    ):
        self.ip = ip
        self.sp = sp
        self.saved_sps = saved_sps
        self.eps_sps = eps_sps
        self.eps_stack = eps_stack


def run(prog: list[Instr], text: str) -> str | None:
    """Run `prog` with the `text` input and return the matched text (or `None`)."""
    thread_stack: list[Thread] = []
    num_saves = sum(1 for instr in prog if instr.op == "save")
    num_epssets = sum(1 for instr in prog if instr.op == "epsset")
    nmemo_instrs = sum(1 for instr in prog if instr.op == "memo")
    memo_table = np.zeros((nmemo_instrs, len(text) + 1, 2), dtype=bool)
    thread = Thread(0, 0, -1 * np.ones(num_saves), -1 * np.ones(num_epssets), [-1])
    while thread is not None or len(thread_stack) > 0:
        thread = thread_stack.pop() if thread is None else thread
        instr = prog[thread.ip]
        print(f"{thread.ip:>2}: {instr}")
        match instr.op:
            case "epsset":
                j = int(instr.args[0]) // 8
                thread.eps_sps[j] = thread.sp
                if thread.eps_stack[-1] != j:
                    # We are entering a new loop
                    thread.eps_stack.append(j)
            case "epspop":
                thread.eps_stack.pop()
            case "epschk":
                j = int(instr.args[0]) // 8
                if thread.eps_sps[j] == thread.sp:
                    thread = None
                    print("---thread killed---")
                    continue
            case "memo":
                j = int(instr.args[0])
                if thread.eps_stack[-1] != -1:
                    i = thread.eps_sps[thread.eps_stack[-1]]
                    loop_will_repeat = 1 if i < thread.sp else 0
                else:
                    # dummy value used when we are not in a loop
                    loop_will_repeat = 0
                if memo_table[j, thread.sp, loop_will_repeat]:
                    thread = None
                    print("---thread killed---")
                    continue
                else:
                    memo_table[j, thread.sp, loop_will_repeat] = 1
            case "save":
                j = int(instr.args[0])
                thread.saved_sps[j] = thread.sp
            case "jmp":
                dest = int(instr.args[0])
                thread.ip = dest
                continue
            case "split":
                d1, d2 = map(int, instr.args)
                thread_stack.append(
                    Thread(
                        d2,
                        thread.sp,
                        thread.saved_sps.copy(),
                        thread.eps_sps.copy(),
                        thread.eps_stack.copy(),
                    )
                )
                thread.ip = d1
                continue
            case "match":
                return text[: thread.sp]
            case "char":
                if thread.sp >= len(text) or text[thread.sp] != instr.args[0]:
                    print("---thread killed---")
                    thread = None
                    continue  # kill thread
                else:
                    thread.sp += 1
            case _:
                raise ValueError(f"Unknown instruction: {instr.op}")
        thread.ip += 1
    return None


if __name__ == "__main__":
    import sys
    from memo_rvm import assembler

    try:
        rasm_file_name, query_text = sys.argv[1], sys.argv[2]
    except IndexError:
        print("Usage: python -m memo_rvm.vm <rasm_file_name> <text_to_match>")
        sys.exit(1)
    prog = assembler.assemble(rasm_file_name)
    matched_text = run(prog, query_text)
    print(f"Matched text: '{matched_text}'")
