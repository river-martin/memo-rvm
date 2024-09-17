import pytest
from memo_rvm import assembler, vm


@pytest.mark.parametrize("prog_name", ["tests/test1.rasm", "tests/test2.rasm"])
def test_assemble(prog_name):
    prog = assembler.assemble(prog_name)
    with open(prog_name, "r") as f:
        for assembled_line in prog:
            assert str(assembled_line) == f.readline().strip()


@pytest.mark.parametrize(
    "prog_name, text, expected",
    [["tests/test1.rasm", "ab", "a"], ["tests/test2.rasm", "ab", "a"]],
)
def test_run(prog_name, text, expected):
    prog = assembler.assemble(prog_name)
    matched_text = vm.run(prog, text)
    assert matched_text == expected


if __name__ == "__main__":
    pytest.main()
