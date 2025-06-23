import sys

if sys.platform == "win32":
    FILE_REG_EXP = r"^[A-Za-z]:?\\?((\w| |-)+\\)*(\w| |-)+\.csv$"
elif sys.platform in {"linux", "darwin"}:
    FILE_REG_EXP = r"^/*(\w+-*\w+/)*\w+-*\w+\.csv$"

WHERE_REG_EXP = r"^\w+[><=][\w.]+$"

AGGREGATE_REG_EXP = r"^\w+[=]\w+$"

AGGREGATE_FUNCS = {"avg", "min", "max"}
