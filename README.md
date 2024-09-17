# memo-rvm

## Installation

```Bash
python3.12 -m venv env
source env/bin/activate
pip install -e .
```

## Testing

Note that `test_run` is expected to fail on `tests/test2.rasm`.

```Bash
pytest tests/test_memo_rvm.py
```

## Execution

```Bash
python3.12 -m memo_rvm.vm tests/test1.rasm ab
```
