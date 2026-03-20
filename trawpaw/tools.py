import time
import os
import sys
from typing import Literal
from . import Trawpaw
from .components import Tem


def compileTrawpawl(source: str, cells: int = 128, maxvaluepercell: int = 127) -> str:
    col = 0
    out = ""
    objs: dict[str, Trawpaw] = {}
    while len(source) > col:
        try:
            if source[col] == "<" and source[col + 1] == "|":
                col += 2
                name = ""
                while source[col] not in [" ", "\n", "\t"]:
                    name += source[col]
                    col += 1

                if not objs.get(name, None):
                    objs[name] = Trawpaw(cells=cells, maxvaluepercell=maxvaluepercell)

                code = ""

                while not (source[col] == "|" and source[col + 1] == ">"):
                    code += source[col]
                    col += 1

                col += 1

                result = objs[name].execute(
                    code, executionMethod=Tem.storeInResult, quickMode=True
                )

                if result.status == 1:
                    out += result.message
                else:
                    out += result.result

            else:
                out += source[col]
        except Exception:
            raise SyntaxError("Invalid trawpawl syntax")

        col += 1

    return out


def simplifyResultExpression(resultExpression: str) -> str:
    return resultExpression.replace("w_" * 100, "w.").replace("w." * 10, "w1")


def executeResultExpression(resultExpression: str) -> None:
    col = 0

    try:
        while len(resultExpression) > col:
            match resultExpression[col]:
                case "d":
                    col += 1
                    print(resultExpression[col], end="")
                case "c":
                    os.system("cls" if os.name == "nt" else "clear")
                case "w":
                    col += 1
                    if resultExpression[col] == "1":
                        sys.stdout.flush()
                        time.sleep(1)
                    elif resultExpression[col] == ".":
                        sys.stdout.flush()
                        time.sleep(0.1)
                    elif resultExpression[col] == "_":
                        sys.stdout.flush()
                        time.sleep(0.001)
                    else:
                        raise SyntaxError("Invalid result expression")

            col += 1
    except IndexError:
        raise SyntaxError("Invalid result expression")

    print()


def compileResultExpression(
    resultExpr: str,
    targetLang: Literal["python"] | Literal["javascript"] = "python",
    javascriptElemName: str = "default",
) -> str:
    col = 0
    if targetLang == "python":
        try:
            out = ""
            code = ""
            while len(resultExpr) > col:
                match resultExpr[col]:
                    case "d":
                        col += 1
                        out += resultExpr[col]
                    case "c":
                        if out:
                            code += f'print({repr(out)}, end="")\n'
                            out = ""

                        if "import os\n" not in code:
                            code = "import os\n" + code

                        code += 'os.system("cls" if os.name == "nt" else "clear")\n'
                    case "w":
                        if out:
                            if "import sys\n" not in code:
                                code = "import sys\n" + code
                            code += f'print({repr(out)}, end="")\nsys.stdout.flush()\n'
                            out = ""
                        if "import time\n" not in code:
                            code = "import time\n" + code

                        col += 1
                        if resultExpr[col] == "1":
                            code += "time.sleep(1)\n"
                        elif resultExpr[col] == ".":
                            code += "time.sleep(.1)\n"
                        elif resultExpr[col] == "_":
                            code += "time.sleep(.001)\n"
                        else:
                            raise SyntaxError("Invalid result expression")
                    case _:
                        raise SyntaxError("Invalid result expression")
                col += 1
            if out:
                code += f"print({repr(out)})\n"
                out = ""
            return code

        except IndexError:
            raise SyntaxError("Invalid result expression")

    elif targetLang == "javascript":
        try:
            out = ""
            code = ""
            last_control = ""
            timeouts = []
            while len(resultExpr) > col:
                match resultExpr[col]:
                    case "d":
                        col += 1
                        out += resultExpr[col]
                        last_control = "d"
                    case "c":
                        if out:
                            code += f"{' ' * len(timeouts) * 2}{javascriptElemName}.textContent += {repr(out)};\n"
                            out = ""
                        code += (
                            " " * len(timeouts) * 2
                            + f'{javascriptElemName}.textContent = "";\n'
                        )
                        last_control = "c"
                    case "w":
                        if out:
                            code += f"{' ' * len(timeouts) * 2}{javascriptElemName}.textContent += {repr(out)};\n"
                            out = ""
                        col += 1
                        code += " " * len(timeouts) * 2 + "setTimeout(function () {\n"
                        if resultExpr[col] == "1":
                            timeouts.append(1000)
                        elif resultExpr[col] == ".":
                            timeouts.append(100)
                        elif resultExpr[col] == "_":
                            timeouts.append(1)
                        else:
                            raise SyntaxError("Invalid result expression")
                        if last_control == "w":
                            code = "\n".join(code.split("\n")[:-2]) + "\n"
                            timeouts.append(timeouts.pop() + timeouts.pop())
                        last_control = "w"
                    case _:
                        raise SyntaxError("Invalid result expression")
                col += 1
            if out:
                code += f"{' ' * len(timeouts) * 2}{javascriptElemName}.textContent += {repr(out)};\n"
                out = ""
            if timeouts:
                for i in timeouts.copy()[::-1]:
                    timeouts.pop()
                    code += " " * len(timeouts) * 2 + "}, " + str(i) + ");\n"
            return code

        except IndexError:
            raise SyntaxError("Invalid result expression")
