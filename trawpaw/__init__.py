from random import randint
from time import sleep
from prompt_toolkit import prompt
from typing import Callable
from .components import Tem, Tdt, Tfun, Thmr, Tlc, Trst, htmlEscape, methods, methodsInt
import sys
import os
import warnings
############# MAIN #############


class Trawpaw:
    def __init__(
        self,
        cells: int = 128,
        maxvaluepercell: int = 127,
    ) -> None:
        assert cells > 0, "Number of cells must be greater than 0."
        assert maxvaluepercell >= 0, (
            "Max value per cell must be greater than or equals 0."
        )
        assert cells <= 65536, "Number of cells must be less than or equals 65536."
        assert maxvaluepercell < 65536, "Max value per cell must be less than 65536."

        self.cells: list[int] = []
        self.nullmem: list[int] = []

        for _ in range(cells):
            self.cells.append(0)
        self.nullmem = self.cells.copy()

        self.maxvaluepercell = maxvaluepercell + 1

        self.datalist: dict = {}
        self.cursor: int = 0

        self.customModules: dict = {}

    def _gErr(self, msg: str, col: int | None = None) -> Trst:
        return Trst(
            {
                "status": 1,
                "message": f"ERR: {msg}{f' at col {col}' if isinstance(col, int) else ''}",
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        )

    def clearData(self) -> None:
        self.cells = self.nullmem.copy()
        self.datalist = {}
        self.cursor = 0

    def registerCustomModule(
        self,
        name: str,
        availableDatatypes: Tdt,
        handleResult: Thmr = Thmr.printManually,
    ) -> Callable:
        def decorator(func: Callable) -> None:
            self.customModules[name] = {
                "handleResult": handleResult,
                "function": func,
                "availableDataTypes": availableDatatypes,
            }

        if "$" in name:
            raise ValueError("Module name cannot contain '$' character.")

        return decorator

    def unregisterCustomModule(self, name: str) -> None:
        try:
            del self.customModules[name]
        except KeyError:
            raise KeyError(f"Module '{name}' is not exist.")

    def runBrainfk(
        self,
        code: str,
        getinput: str = "",
        startAtCol: int = 0,
        executionMethod: Tem = Tem.printManually,
        quickMode: bool = False,
        silentMode: bool = False,
    ) -> Trst:
        inputcur: int = 0
        bracketlist: list[int] = []
        result: str = ""
        col: int = startAtCol
        while col - startAtCol < len(code):
            match code[col - startAtCol]:
                case "+":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] + 1
                    ) % self.maxvaluepercell
                case "-":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] - 1
                    ) % self.maxvaluepercell
                case "<":
                    self.cursor = (self.cursor - 1) % len(self.cells)
                case ">":
                    self.cursor = (self.cursor + 1) % len(self.cells)
                case ",":
                    if quickMode:
                        if not silentMode:
                            warnings.warn(
                                f"\n[TRAWPAW col:{col}] In quick mode, inputting is not supported. Now ignoring this."
                            )
                    try:
                        self.cells[self.cursor] = (
                            ord(getinput[inputcur]) % self.maxvaluepercell
                        )
                        inputcur += 1
                    except IndexError:
                        ginput = prompt()
                        if ginput:
                            self.cells[self.cursor] = (
                                ord(ginput[0]) % self.maxvaluepercell
                            )
                        else:
                            self.cells[self.cursor] = 0
                case ".":
                    if executionMethod == Tem.printManually:
                        print(chr(self.cells[self.cursor]), end="")
                    elif executionMethod == Tem.storeInResultExpression:
                        result += "d" + chr(self.cells[self.cursor])
                    else:
                        result += chr(self.cells[self.cursor])
                case "[":
                    bracketlist.append(col)
                case "]":
                    if self.cells[self.cursor] != 0:
                        col = bracketlist[-1]
                    else:
                        bracketlist.pop()
            col += 1
        if len(bracketlist) != 0:
            return self._gErr("Bracket is not closed", col=col)
        return Trst(
            {
                "status": 0,
                "result": result,
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        )

    def skipInside(self, code: str, bracket: str, col: int, startAtCol: int) -> dict:
        bracketlist: list[dict] = [
            {
                "type": bracket,
            }
        ]

        try:
            while bracketlist:
                match code[col - startAtCol]:
                    case "[" | "(" | "{":
                        bracketlist.append({"type": code[col - startAtCol]})
                    case "}":
                        if bracketlist:
                            if bracketlist[-1]["type"] == "{":
                                bracketlist.pop()
                            else:
                                return {"status": 1, "col": col}
                        else:
                            return {"status": 1, "col": col}
                    case "]":
                        if bracketlist:
                            if bracketlist[-1]["type"] == "[":
                                bracketlist.pop()
                            else:
                                return {"status": 1, "col": col}
                        else:
                            return {"status": 1, "col": col}
                    case ")":
                        if bracketlist:
                            if bracketlist[-1]["type"] == "(":
                                bracketlist.pop()
                            else:
                                return {"status": 1, "col": col}
                        else:
                            return {"status": 1, "col": col}
                col += 1
        except IndexError:
            return {"status": 1, "col": col - 1}

        return {"status": 0, "col": col}

    def runWaste(
        self,
        code: str,
        saveto: str,
        startAtCol: int = 0,
        executionMethod: Tem = Tem.printManually,
    ) -> Trst:
        if len(self.cells) < 10:
            return self._gErr(
                "To run waste (professional) code, at least 10 cells is required, please change your settings",
            )
        saved: int = 0
        try:
            if self.datalist[saveto]["type"] == "number":
                saved = self.datalist[saveto]["value"]
            else:
                return self._gErr(f"Data '{saveto}' is not a number.")
        except KeyError:
            return self._gErr(f"Data '{saveto}' is not initialized.")
        out: str = ""
        bracketlist: list = []
        col: int = startAtCol
        while col - startAtCol < len(code):
            match code[col - startAtCol]:
                case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    self.cursor = int(code[col - startAtCol])
                case "＜" | "<":
                    saved = self.cells[self.cursor]
                case "＞" | ">":
                    self.cells[self.cursor] = saved
                case "＠" | "@":
                    if executionMethod == Tem.printManually:
                        os.system("cls" if os.name == "nt" else "clear")
                    elif executionMethod == Tem.storeInResultExpression:
                        out += "c"
                    else:
                        out = ""
                case "＃" | "#":
                    self.cells[self.cursor] = 0
                case "+" | "＋":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] + 1
                    ) % self.maxvaluepercell
                case "-" | "－":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] - 1
                    ) % self.maxvaluepercell
                case "*" | "＊":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] * 2
                    ) % self.maxvaluepercell
                case "/" | "／":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] // 2
                    ) % self.maxvaluepercell
                case "＾" | "^":
                    self.cells[self.cursor] = (randint(0, 1)) % self.maxvaluepercell
                case ";" | "；":
                    self.cells[self.cursor] = (
                        self.cells[self.cursor] + randint(0, 1)
                    ) % self.maxvaluepercell
                case "％" | "%":
                    if executionMethod == Tem.printManually:
                        print(str(self.cells[self.cursor]), end="")
                    elif executionMethod == Tem.storeInResultExpression:
                        out += "d" + "d".join(list(str(self.cells[self.cursor])))
                    else:
                        out += str(self.cells[self.cursor])
                case "＆" | "&":
                    prompt("Breakpoint reached. Press Enter to continue...")
                case "．" | ".":
                    try:
                        if executionMethod == Tem.printManually:
                            print(chr(self.cells[self.cursor]), end="")
                        elif executionMethod == Tem.storeInResultExpression:
                            out += "d" + chr(self.cells[self.cursor])
                        else:
                            out += chr(self.cells[self.cursor])
                    except Exception:
                        if executionMethod == Tem.printManually:
                            print("?", end="")
                        elif executionMethod == Tem.storeInResultExpression:
                            out += "d?"
                        else:
                            out += "?"
                case "：" | ":":
                    if executionMethod == Tem.printManually:
                        print("\n", end="")
                    elif executionMethod == Tem.storeInResultExpression:
                        out += "d\n"
                    else:
                        out += "\n"
                case "！" | "!":
                    return Trst(
                        {
                            "status": 2,
                            "result": out,
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    )
                case "［" | "[":
                    bracketlist.append({"type": "]", "position": col, "currranges": 0})
                case "］" | "]":
                    if not bracketlist or bracketlist[-1]["type"] != "]":
                        return self._gErr("Unmatched closing bracket", col=col)
                    else:
                        if bracketlist[-1]["currranges"] > 0:
                            bracketlist.pop()
                        else:
                            bracketlist[-1]["currranges"] += 1
                            col = bracketlist[-1]["position"]
                case "（" | "(":
                    if randint(0, 1):
                        bracketlist.append(
                            {"type": ")", "position": col, "currranges": 0}
                        )
                    else:
                        skipRs = self.skipInside(code, "(", col + 1, 0)
                        if skipRs["status"] == 1:
                            return self._gErr(
                                "Bracket is not properly closed", col=skipRs["col"]
                            )
                        else:
                            col = skipRs["col"] - 1
                case "）" | ")":
                    if not bracketlist:
                        return self._gErr("Unmatched closing bracket", col=col)
                    elif bracketlist[-1]["type"] != ")":
                        return self._gErr("Unmatched closing bracket", col=col)
                    else:
                        bracketlist.pop()
                case "｛" | "{":
                    skipRs = self.skipInside(code, "{", col + 1, 0)
                    if skipRs["status"] == 1:
                        return self._gErr(
                            "Bracket is not properly closed", col=skipRs["col"]
                        )
                    else:
                        col = skipRs["col"] - 1
                case "｝" | "}":
                    if not bracketlist:
                        return self._gErr("Unmatched closing bracket", col=col)
                    elif bracketlist[-1]["type"] != "}":
                        return self._gErr("Unmatched closing bracket", col=col)
                    else:
                        bracketlist.pop()
            col += 1

        if bracketlist:
            return self._gErr("Bracket is not closed", col=col)

        try:
            self.datalist[saveto]["type"] = "number"
            self.datalist[saveto]["value"] = saved
            return Trst(
                {
                    "status": 0,
                    "result": out,
                    "cursor": self.cursor,
                    "datalistlength": len(self.datalist),
                }
            )
        except KeyError:
            return self._gErr(f"Data '{saveto}' is not initialized.")

    def runWastePreview(
        self,
        code: str,
        saveto: str,
        startAtCol: int = 0,
        executionMethod: Tem = Tem.printManually,
        quickMode: bool = False,
        silentMode: bool = False,
    ) -> Trst:
        saved: int = 0
        ptr: int = self.cells[self.cursor]
        try:
            if self.datalist[saveto]["type"] == "number":
                saved = self.datalist[saveto]["value"]
            else:
                return self._gErr(f"Data '{saveto}' is not a number.")
        except KeyError:
            return self._gErr(f"Data '{saveto}' is not initialized.")
        out: str = ""
        bracketlist: list = []
        col: int = startAtCol
        while col - startAtCol < len(code):
            match code[col - startAtCol]:
                case "＜" | "<":
                    saved = ptr
                case "＞" | ">":
                    ptr = saved
                case "＾" | "^":
                    ptr = randint(0, 1)
                case "＠" | "@":
                    if executionMethod == Tem.printManually:
                        os.system("cls" if os.name == "nt" else "clear")
                    elif executionMethod == Tem.storeInResultExpression:
                        out += "c"
                    else:
                        out = ""
                case "，" | ",":
                    if executionMethod == Tem.printManually:
                        print(code[col - startAtCol + 1 :], end="")
                    elif executionMethod == Tem.storeInResultExpression:
                        out += "d" + "d".join(list(code[col - startAtCol + 1 :]))
                    else:
                        out += code[col - startAtCol + 1 :]
                    break
                case "＃" | "#":
                    ptr = 0
                case "+" | "＋":
                    ptr = (ptr + 1) % self.maxvaluepercell
                case "-" | "－":
                    ptr = (ptr - 1) % self.maxvaluepercell
                case "*" | "＊":
                    ptr = (ptr * 2) % self.maxvaluepercell
                case "/" | "／":
                    ptr = (ptr // 2) % self.maxvaluepercell
                case "％" | "%":
                    if executionMethod == Tem.printManually:
                        print(str(ptr), end="")
                    elif executionMethod == Tem.storeInResultExpression:
                        out += "d" + "d".join(list(str(ptr)))
                    else:
                        out += str(ptr)
                case "＆" | "&":
                    prompt("Breakpoint reached. Press Enter to continue...")
                case "．" | ".":
                    try:
                        if executionMethod == Tem.printManually:
                            print(chr(ptr), end="")
                        elif executionMethod == Tem.storeInResultExpression:
                            out += "d" + chr(ptr)
                        else:
                            out += chr(ptr)
                    except Exception:
                        if executionMethod == Tem.printManually:
                            print("?", end="")
                        elif executionMethod == Tem.storeInResultExpression:
                            out += "d?"
                        else:
                            out += "?"
                case "：" | ":":
                    if executionMethod == Tem.printManually:
                        print("\n", end="")
                        sys.stdout.flush()
                    out += "\n"
                case "？" | "?":
                    if quickMode:
                        if not silentMode:
                            warnings.warn(
                                f"\n[TRAWPAW col:{col}] In quick mode, waitting is not supported. Now ignoring this."
                            )
                    if executionMethod == Tem.storeInResultExpression:
                        out += "w_"
                    else:
                        sys.stdout.flush()
                        sleep(0.001)
                case "！" | "!":
                    return Trst(
                        {
                            "status": 2,
                            "result": out,
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    )
                case "［" | "[":
                    bracketlist.append({"type": "]", "position": col, "currranges": 0})
                case "］" | "]":
                    if not bracketlist or bracketlist[-1]["type"] != "]":
                        return self._gErr("Unmatched closing bracket", col=col)
                    else:
                        if bracketlist[-1]["currranges"] > 0:
                            bracketlist.pop()
                        else:
                            bracketlist[-1]["currranges"] += 1
                            col = bracketlist[-1]["position"]
                case "（" | "(":
                    if randint(0, 1):
                        bracketlist.append(
                            {"type": ")", "position": col, "currranges": 0}
                        )
                    else:
                        skipRs = self.skipInside(code, "(", col + 1, 0)
                        if skipRs["status"] == 1:
                            return self._gErr(
                                "Bracket is not properly closed", col=skipRs["col"]
                            )
                        else:
                            col = skipRs["col"] - 1
                case "）" | ")":
                    if not bracketlist:
                        return self._gErr("Unmatched closing bracket", col=col)
                    elif bracketlist[-1]["type"] != ")":
                        return self._gErr("Unmatched closing bracket", col=col)
                    else:
                        bracketlist.pop()
                case "｛" | "{":
                    skipRs = self.skipInside(code, "{", col + 1, 0)
                    if skipRs["status"] == 1:
                        return self._gErr(
                            "Bracket is not properly closed", col=skipRs["col"]
                        )
                    else:
                        col = skipRs["col"] - 1
                case "｝" | "}":
                    if not bracketlist:
                        return self._gErr("Unmatched closing bracket", col=col)
                    elif bracketlist[-1]["type"] != "}":
                        return self._gErr("Unmatched closing bracket", col=col)
                    else:
                        bracketlist.pop()
            col += 1

        if bracketlist:
            return self._gErr("Bracket is not closed", col=col)

        # Save result to datalist
        try:
            self.cells[self.cursor] = ptr
            self.datalist[saveto]["type"] = "number"
            self.datalist[saveto]["value"] = saved
            return Trst(
                {
                    "status": 0,
                    "result": out,
                    "cursor": self.cursor,
                    "datalistlength": len(self.datalist),
                }
            )
        except KeyError:
            return self._gErr(f"Data '{saveto}' is not initialized.")

    def execute(
        self,
        code: str,
        getinput: str = "",
        clearData: bool = False,
        startAtCol: int = 0,
        executionMethod: Tem = Tem.printManually,
        quickMode: bool = False,
        silentMode: bool = False,
    ) -> Trst:
        inputcur: int = 0
        bracketlist: list[dict] = []
        result: str = ""
        col: int = startAtCol
        dataDefinition: bool = False
        special: int = 0
        while col - startAtCol < len(code):
            if not dataDefinition:
                match code[col - startAtCol]:
                    case "+":
                        self.cells[self.cursor] = (
                            self.cells[self.cursor] + 1
                        ) % self.maxvaluepercell
                        special = 0
                    case "-":
                        self.cells[self.cursor] = (
                            self.cells[self.cursor] - 1
                        ) % self.maxvaluepercell
                        special = 0
                    case "*":
                        self.cells[self.cursor] = (
                            self.cells[self.cursor] * 2
                        ) % self.maxvaluepercell
                        special = 0
                    case "/":
                        self.cells[self.cursor] = (
                            self.cells[self.cursor] // 2
                        ) % self.maxvaluepercell
                        special = 0
                    case "#":
                        if special >= 2:
                            self.clearData()
                        elif special == 1:
                            self.cursor = 0
                        else:
                            self.cells[self.cursor] = 0
                        special = 0
                    case "<":
                        self.cursor = (self.cursor - 1) % len(self.cells)
                        special = 0
                    case ">":
                        self.cursor = (self.cursor + 1) % len(self.cells)
                        special = 0
                    case ",":
                        if not quickMode:
                            try:
                                self.cells[self.cursor] = (
                                    ord(getinput[inputcur]) % self.maxvaluepercell
                                )
                                inputcur += 1
                            except IndexError:
                                original_input = prompt()
                                if original_input:
                                    self.cells[self.cursor] = (
                                        ord(original_input[0]) % self.maxvaluepercell
                                    )
                                else:
                                    self.cells[self.cursor] = 0
                        else:
                            if not silentMode:
                                warnings.warn(
                                    f"\n[TRAWPAW col:{col}] In quick mode, inputting is not supported. Now ignoring this."
                                )
                        special = 0
                    case ".":
                        if special:
                            if executionMethod == Tem.printManually:
                                print(str(self.cells[self.cursor]), end="")
                            elif executionMethod == Tem.storeInResultExpression:
                                result += "d" + "d".join(
                                    list(str(self.cells[self.cursor]))
                                )
                            else:
                                result += str(self.cells[self.cursor])
                        else:
                            if executionMethod == Tem.printManually:
                                print(chr(self.cells[self.cursor]), end="")
                            elif executionMethod == Tem.storeInResultExpression:
                                result += "d" + chr(self.cells[self.cursor])
                            else:
                                result += chr(self.cells[self.cursor])
                        special = 0
                    case "$":
                        dataDefinition = True
                    case "_":
                        if quickMode:
                            if not silentMode:
                                warnings.warn(
                                    f"\n[TRAWPAW col:{col}] In quick mode, waitting is not supported. Now ignoring this."
                                )
                        if special:
                            if executionMethod == Tem.storeInResultExpression:
                                result += "w."
                            else:
                                sys.stdout.flush()
                                sleep(0.1)
                        else:
                            if executionMethod == Tem.storeInResultExpression:
                                result += "w1"
                            else:
                                sys.stdout.flush()
                                sleep(1)
                        special = 0
                    case "&":
                        # Breakpoint for debugging
                        if special:
                            return Trst(
                                {
                                    "status": 2,
                                    "result": result,
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                            )
                        else:
                            prompt("Breakpoint reached. Press Enter to continue...")
                        special = 0
                    case "!":
                        special += 1
                    case "@":
                        col += 1
                        try:
                            if code[col - startAtCol].upper() == "V":
                                if executionMethod == Tem.printManually:
                                    print(str(self.datalist), end="")
                                elif executionMethod == Tem.storeInResultExpression:
                                    result += "d" + "d".join(list(str(self.datalist)))
                                else:
                                    result += str(self.datalist)
                            elif code[col - startAtCol].upper() == "C":
                                if executionMethod == Tem.printManually:
                                    print(str(self.cursor), end="")
                                elif executionMethod == Tem.storeInResultExpression:
                                    result += "d" + "d".join(list(str(self.cursor)))
                                else:
                                    result += str(self.cursor)
                            elif code[col - startAtCol].upper() == "M":
                                celldata = (
                                    str(len(self.cells))
                                    + " "
                                    + str(self.maxvaluepercell - 1)
                                )
                                if executionMethod == Tem.printManually:
                                    print(str(celldata), end="")
                                elif executionMethod == Tem.storeInResultExpression:
                                    result += "d" + "d".join(list(str(celldata)))
                                else:
                                    result += str(celldata)
                            elif code[col - startAtCol].upper() == "B":
                                if executionMethod == Tem.printManually:
                                    print(str(bracketlist), end="")
                                elif executionMethod == Tem.storeInResultExpression:
                                    result += "d" + "d".join(list(str(bracketlist)))
                                else:
                                    result += str(bracketlist)
                            else:
                                return self._gErr("Invalid debug mark", col=col)
                            special = 0
                        except IndexError:
                            return self._gErr("Impl didn't match a debug mark")
                    case "[":
                        if bool(special):
                            if randint(0, 1):
                                bracketlist.append(
                                    {"bracket": "[", "col": col, "special": True}
                                )
                            else:
                                skipRs = self.skipInside(code, "[", col + 1, 0)
                                if skipRs["status"] == 1:
                                    return self._gErr(
                                        "Bracket is not properly closed",
                                        col=skipRs["col"],
                                    )
                                else:
                                    col = skipRs["col"] - 1
                        else:
                            bracketlist.append(
                                {
                                    "bracket": "[",
                                    "col": col,
                                    "special": bool(special),
                                    "ranges": 0,
                                }
                            )
                        special = 0
                    case "(":
                        if bool(special):
                            if self.cells[self.cursor] != 0:
                                skipRs = self.skipInside(code, "(", col + 1, 0)
                                if skipRs["status"] == 1:
                                    return self._gErr(
                                        "Bracket is not properly closed",
                                        col=skipRs["col"],
                                    )
                                else:
                                    col = skipRs["col"] - 1
                            else:
                                bracketlist.append(
                                    {
                                        "bracket": "(",
                                        "col": col,
                                    }
                                )
                        else:
                            if self.cells[self.cursor] == 0:
                                skipRs = self.skipInside(code, "(", col + 1, 0)
                                if skipRs["status"] == 1:
                                    return self._gErr(
                                        "Bracket is not properly closed",
                                        col=skipRs["col"],
                                    )
                                else:
                                    col = skipRs["col"] - 1
                            else:
                                bracketlist.append(
                                    {
                                        "bracket": "(",
                                        "col": col,
                                    }
                                )
                        special = 0
                    case ")":
                        if bracketlist:
                            if bracketlist[-1]["bracket"] == "(":
                                bracketlist.pop()
                            else:
                                return self._gErr(
                                    "This bracket is not properly opened", col=col
                                )
                        else:
                            return self._gErr(
                                "This bracket is not properly opened", col=col
                            )
                        special = 0
                    case "{":
                        skipRs = self.skipInside(code, "{", col + 1, 0)
                        if skipRs["status"] == 1:
                            return self._gErr(
                                "Bracket is not properly closed", col=skipRs["col"]
                            )
                        else:
                            col = skipRs["col"] - 1
                        special = 0
                    case "}":
                        if bracketlist:
                            if bracketlist[-1]["bracket"] == "{":
                                bracketlist.pop()
                            else:
                                return self._gErr(
                                    "This bracket is not properly opened", col=col
                                )
                        else:
                            return self._gErr(
                                "This bracket is not properly opened", col=col
                            )
                        special = 0
                    case "]":
                        if not bracketlist:
                            return self._gErr(
                                "This bracket is not properly opened", col=col
                            )
                        elif bracketlist[-1]["bracket"] != "[":
                            return self._gErr(
                                "This bracket is not properly closed", col=col
                            )
                        elif not bracketlist[-1]["special"]:
                            if bracketlist[-1]["ranges"] == 0:
                                col = bracketlist[-1]["col"]
                                bracketlist[-1]["ranges"] += 1
                            else:
                                bracketlist.pop()
                        else:
                            bracketlist.pop()
                        special = 0
            elif dataDefinition:
                if special:
                    dofunction = ""
                    try:
                        while code[col - startAtCol] != "$":
                            dofunction += code[col - startAtCol]
                            col += 1

                        if dofunction in self.customModules.keys():
                            customModule = self.customModules[dofunction]
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                passarg = self.datalist[varname]["value"]

                                if (self.datalist[varname]["type"] == "string") and (
                                    Tdt.String in customModule["availableDataTypes"]
                                ):
                                    moduleResult = customModule["function"](passarg)
                                elif (
                                    self.datalist[varname]["type"] == "function"
                                ) and (
                                    Tdt.Function in customModule["availableDataTypes"]
                                ):
                                    moduleResult = customModule["function"](
                                        Tfun(passarg)
                                    )
                                elif (self.datalist[varname]["type"] == "number") and (
                                    Tdt.Number in customModule["availableDataTypes"]
                                ):
                                    moduleResult = customModule["function"](passarg)
                                elif (
                                    self.datalist[varname]["type"] == "linkcell"
                                ) and (
                                    Tdt.LinkCell in customModule["availableDataTypes"]
                                ):
                                    moduleResult = customModule["function"](
                                        Tlc(passarg)
                                    )
                                else:
                                    return self._gErr("Invalid data type", col=col)

                                try:
                                    match customModule["handleResult"]:
                                        case Thmr.assignToVar:
                                            if isinstance(moduleResult, str):
                                                self.datalist[varname]["value"] = (
                                                    moduleResult
                                                )
                                                self.datalist[varname]["type"] = (
                                                    "string"
                                                )
                                            elif isinstance(moduleResult, int):
                                                self.datalist[varname]["value"] = (
                                                    moduleResult % self.maxvaluepercell
                                                )
                                                self.datalist[varname]["type"] = (
                                                    "number"
                                                )
                                            elif isinstance(moduleResult, Tfun):
                                                self.datalist[varname]["value"] = (
                                                    moduleResult.value
                                                )
                                                self.datalist[varname]["type"] = (
                                                    "function"
                                                )
                                                self.datalist[varname]["startAtCol"] = (
                                                    col + 1
                                                )
                                            elif isinstance(moduleResult, Tlc):
                                                if moduleResult.value < len(self.cells):
                                                    self.datalist[varname]["value"] = (
                                                        moduleResult.value
                                                    )
                                                    self.datalist[varname]["type"] = (
                                                        "linkcell"
                                                    )
                                                else:
                                                    return self._gErr(
                                                        f"Custom module '{dofunction}' returned an invalid address that is out of length of cells",
                                                        col=col,
                                                    )
                                            else:
                                                return self._gErr(
                                                    f"Invalid return type of the custom module '{dofunction}'",
                                                    col=col,
                                                )
                                        case Thmr.storeToCurrCell:
                                            if isinstance(moduleResult, int):
                                                self.cells[self.cursor] = (
                                                    moduleResult % self.maxvaluepercell
                                                )
                                            else:
                                                return self._gErr(
                                                    f"Custom module '{dofunction}' must return an integer if the handleResult was set to storeToCurrCell",
                                                    col=col,
                                                )
                                        case Thmr.printManually:
                                            if isinstance(moduleResult, (str, int)):
                                                if executionMethod == Tem.printManually:
                                                    print(str(moduleResult), end="")
                                                elif (
                                                    executionMethod
                                                    == Tem.storeInResultExpression
                                                ):
                                                    result += "d" + "d".join(
                                                        list(str(moduleResult))
                                                    )
                                                else:
                                                    result += str(moduleResult)
                                            else:
                                                return self._gErr(
                                                    f"Custom module '{dofunction}' must return an integer if the handleResult was set to storeToCurrCell",
                                                    col=col,
                                                )
                                        case _:
                                            return self._gErr(
                                                f"Invalid handleResult setting of the custom module '{dofunction}'",
                                                col=col,
                                            )

                                    self.datalist[varname]["value"] = moduleResult
                                except Exception as e:
                                    return self._gErr(
                                        f"Custom module '{dofunction}' execution failed: {type(e).__name__}: {e}",
                                        col=col,
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "runbf":
                            col += 1
                            name = code[col - startAtCol]
                            try:
                                if self.datalist[name]["type"] == "function":
                                    functionResult = self.runBrainfk(
                                        self.datalist[name]["value"],
                                        startAtCol=self.datalist[name]["startAtCol"],
                                        executionMethod=executionMethod,
                                        quickMode=quickMode,
                                        silentMode=silentMode,
                                    )
                                    if functionResult.status == 1:
                                        return self._gErr(functionResult.message)
                                    else:
                                        result += functionResult.result
                                else:
                                    return self._gErr(
                                        "Variable must be a function", col=col
                                    )
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        elif dofunction == "runwaste":
                            col += 1
                            name = code[col - startAtCol]
                            col += 1
                            try:
                                if code[col - startAtCol] != "$":
                                    return self._gErr(
                                        "Invalid waste module call syntax", col=col
                                    )
                                else:
                                    col += 1
                                    varname = code[col - startAtCol]
                                    try:
                                        if self.datalist[name]["type"] == "function":
                                            functionResult = self.runWaste(
                                                self.datalist[name]["value"],
                                                varname,
                                                startAtCol=self.datalist[name][
                                                    "startAtCol"
                                                ],
                                                executionMethod=executionMethod,
                                            )
                                            if functionResult.status == 1:
                                                return self._gErr(
                                                    functionResult.message
                                                )
                                            else:
                                                result += functionResult.result
                                        else:
                                            return self._gErr(
                                                "Variable must be a function", col=col
                                            )
                                    except KeyError:
                                        return self._gErr(
                                            "(One of) arguments is/are not initialized",
                                            col=col,
                                        )
                            except IndexError:
                                return self._gErr("Missing one argument", col=col)
                        elif dofunction == "runwaste.preview":
                            col += 1
                            name = code[col - startAtCol]
                            col += 1
                            if code[col - startAtCol] != "$":
                                return self._gErr(
                                    "Invalid waste module call syntax", col=col
                                )
                            else:
                                col += 1
                                varname = code[col - startAtCol]
                                try:
                                    if self.datalist[name]["type"] == "function":
                                        functionResult = self.runWastePreview(
                                            self.datalist[name]["value"],
                                            varname,
                                            startAtCol=self.datalist[name][
                                                "startAtCol"
                                            ],
                                            executionMethod=executionMethod,
                                            quickMode=quickMode,
                                            silentMode=silentMode,
                                        )
                                        if functionResult.status == 1:
                                            return self._gErr(functionResult.message)
                                        else:
                                            result += functionResult.result
                                    else:
                                        return self._gErr(
                                            "Variable must be a function", col=col
                                        )
                                except KeyError:
                                    return self._gErr(
                                        "(One of) arguments is/are not initialized",
                                        col=col,
                                    )
                        elif dofunction == "include":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    try:
                                        with open(
                                            self.datalist[varname]["value"],
                                            "r",
                                            encoding="utf-8",
                                        ) as f:
                                            includeCode = f.read()
                                            f.close()
                                        functionResult = self.execute(
                                            includeCode,
                                            startAtCol=0,
                                            executionMethod=executionMethod,
                                            quickMode=quickMode,
                                            silentMode=silentMode,
                                        )
                                        if functionResult.status == 1:
                                            return self._gErr(
                                                functionResult.message
                                                + f" in file {self.datalist[varname]['value']}"
                                            )
                                        else:
                                            result += functionResult.result
                                    except FileNotFoundError:
                                        return self._gErr(
                                            f"File {self.datalist[varname]['value']} not found",
                                            col=col,
                                        )
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "virtual":
                            col += 1
                            varname = code[col - startAtCol]
                            anotherTpwObj = Trawpaw(
                                len(self.cells), self.maxvaluepercell - 1
                            )
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    try:
                                        with open(
                                            self.datalist[varname]["value"],
                                            "r",
                                            encoding="utf-8",
                                        ) as f:
                                            includeCode = f.read()
                                            f.close()
                                        functionResult = anotherTpwObj.execute(
                                            includeCode,
                                            startAtCol=0,
                                            executionMethod=executionMethod,
                                            quickMode=quickMode,
                                            silentMode=silentMode,
                                        )
                                        if functionResult.status == 1:
                                            return self._gErr(
                                                functionResult.message
                                                + f" in file {self.datalist[varname]['value']}"
                                            )
                                        else:
                                            result += functionResult.result
                                    except FileNotFoundError:
                                        return self._gErr(
                                            f"File {self.datalist[varname]['value']} not found",
                                            col=col,
                                        )
                                elif self.datalist[varname]["type"] == "function":
                                    includeCode = self.datalist[varname]["value"]
                                    functionResult = anotherTpwObj.execute(
                                        includeCode,
                                        startAtCol=self.datalist[varname]["startAtCol"],
                                        executionMethod=executionMethod,
                                        quickMode=quickMode,
                                        silentMode=silentMode,
                                    )
                                    if functionResult.status == 1:
                                        return self._gErr(functionResult.message)
                                    else:
                                        result += functionResult.result
                                else:
                                    return self._gErr(
                                        "Variable must be a string or a function",
                                        col=col,
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "print":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    if executionMethod == Tem.printManually:
                                        print(
                                            str(self.datalist[varname]["value"]), end=""
                                        )
                                    elif executionMethod == Tem.storeInResultExpression:
                                        result += "d" + "d".join(
                                            list(str(self.datalist[varname]["value"]))
                                        )
                                    else:
                                        result += str(self.datalist[varname]["value"])
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "getinput":
                            if quickMode:
                                if not silentMode:
                                    warnings.warn(
                                        f"\n[TRAWPAW col:{col}] In quick mode, inputting is not supported. Now ignoring this."
                                    )
                            col += 1
                            hint = code[col - startAtCol]
                            col += 1
                            if code[col - startAtCol] != "$":
                                return self._gErr(
                                    "Invalid waste module call syntax", col=col
                                )
                            else:
                                col += 1
                                storeto = code[col - startAtCol]
                                try:
                                    if self.datalist[hint]["type"] != "string":
                                        return self._gErr(
                                            "Hint must be a string", col=col
                                        )

                                    inp_result = prompt(self.datalist[hint]["value"])
                                    self.datalist[storeto]["type"] = "string"
                                    self.datalist[storeto]["value"] = inp_result
                                except KeyError:
                                    return self._gErr(
                                        "(One of) arguments is/are not initialized",
                                        col=col,
                                    )
                        elif dofunction == "string.addto":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    self.datalist[varname]["value"] += chr(
                                        self.cells[self.cursor]
                                    )
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "string.inserttofirst":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    self.datalist[varname]["value"] = self.datalist[
                                        varname
                                    ]["value"][::-1]
                                    self.datalist[varname]["value"] += chr(
                                        self.cells[self.cursor]
                                    )
                                    self.datalist[varname]["value"] = self.datalist[
                                        varname
                                    ]["value"][::-1]
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )

                        elif dofunction == "string.length":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    string_length = len(self.datalist[varname]["value"])
                                    self.cells[self.cursor] = (
                                        string_length % self.maxvaluepercell
                                    )
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "string.reverse":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = self.datalist[varname]["value"][::-1]
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "string.toupper":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = self.datalist[varname]["value"].upper()
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "string.tolower":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = self.datalist[varname]["value"].lower()
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction in ["string.encodeuri", "string.decodeuri"]:
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = methods["urlparse"][dofunction](
                                        self.datalist[varname]["value"]
                                    )
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "string.escape":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = self.datalist[varname]["value"]
                                    for k, v in htmlEscape.items():
                                        newString = newString.replace(k, v)
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "string.unescape":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = self.datalist[varname]["value"]
                                    for k, v in list(htmlEscape.items())[::-1]:
                                        newString = newString.replace(v, k)
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )

                        elif dofunction.startswith("hash."):
                            col += 1
                            varname = code[col - startAtCol]

                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    try:
                                        newString = methods["hash"][dofunction](
                                            self.datalist[varname]["value"].encode()
                                        ).hexdigest()
                                    except KeyError:
                                        return self._gErr(
                                            "Invalid hash method", col=col
                                        )
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction.startswith("base64."):
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    try:
                                        newString = methods["base64"][dofunction](
                                            self.datalist[varname]["value"].encode()
                                        ).decode()
                                    except KeyError:
                                        return self._gErr(
                                            "Invalid base64 method", col=col
                                        )
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction in [
                            "string.offset.forward",
                            "string.offset.backward",
                        ]:
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    newString = ""
                                    for char in self.datalist[varname]["value"]:
                                        newString += chr(
                                            ord(char) + methodsInt["offset"][dofunction]
                                        )
                                    self.datalist[varname]["value"] = newString
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "number.plusby":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "number":
                                    rs = (
                                        self.cells[self.cursor]
                                        + self.datalist[varname]["value"]
                                    )
                                    self.cells[self.cursor] = rs % self.maxvaluepercell
                                else:
                                    return self._gErr(
                                        "Variable must be a number", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "number.subtractby":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "number":
                                    rs = (
                                        self.cells[self.cursor]
                                        - self.datalist[varname]["value"]
                                    )
                                    self.cells[self.cursor] = rs % self.maxvaluepercell
                                else:
                                    return self._gErr(
                                        "Variable must be a number", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "number.timesby":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "number":
                                    rs = (
                                        self.cells[self.cursor]
                                        * self.datalist[varname]["value"]
                                    )
                                    self.cells[self.cursor] = rs % self.maxvaluepercell
                                else:
                                    return self._gErr(
                                        "Variable must be a number", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "number.divideby":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "number":
                                    rs = (
                                        self.cells[self.cursor]
                                        // self.datalist[varname]["value"]
                                    )
                                    self.cells[self.cursor] = rs % self.maxvaluepercell
                                else:
                                    return self._gErr(
                                        "Variable must be a number", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "number.powerby":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "number":
                                    rs = (
                                        self.cells[self.cursor]
                                        ** self.datalist[varname]["value"]
                                    )
                                    self.cells[self.cursor] = rs % self.maxvaluepercell
                                else:
                                    return self._gErr(
                                        "Variable must be a number", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "tostring":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] in [
                                    "function",
                                    "number",
                                ]:
                                    self.datalist[varname]["type"] = "string"
                                    self.datalist[varname]["value"] = str(
                                        self.datalist[varname]["value"]
                                    )
                                    del self.datalist[varname]["startAtCol"]
                                else:
                                    return self._gErr(
                                        "Variable must be a number or function", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "asnumber":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "linkcell":
                                    self.datalist[varname]["type"] = "number"
                                    self.datalist[varname]["value"] = self.cells[
                                        self.datalist[varname]["value"]
                                    ]
                                else:
                                    return self._gErr(
                                        "Variable must be a reference of cell (linkcell)",
                                        col=col,
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        elif dofunction == "tofunction":
                            col += 1
                            varname = code[col - startAtCol]
                            if self.datalist.get(varname):
                                if self.datalist[varname]["type"] == "string":
                                    self.datalist[varname]["type"] = "function"
                                    self.datalist[varname]["startAtCol"] = col + 1
                                else:
                                    return self._gErr(
                                        "Variable must be a string", col=col
                                    )
                            else:
                                return self._gErr(
                                    f"Data '{varname}' is not initialized", col=col
                                )
                        else:
                            return self._gErr("Unknown module", col=col)
                        special = 0
                    except IndexError:
                        return self._gErr("Module name reached the end of the code")
                else:
                    name: str = code[col - startAtCol]
                    col += 1
                    controller: str = code[col - startAtCol]

                    match controller.upper():
                        case "I":
                            self.datalist[name] = {"type": "number", "value": 0}
                        case "W":
                            try:
                                self.datalist[name]["type"] = "number"
                                self.datalist[name]["value"] = self.cells[self.cursor]
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case "R":
                            try:
                                if self.datalist[name]["type"] == "number":
                                    self.cells[self.cursor] = self.datalist[name][
                                        "value"
                                    ]
                                elif self.datalist[name]["type"] == "linkcell":
                                    self.cells[self.cursor] = self.cells[
                                        self.datalist[name]["value"]
                                    ]
                                elif self.datalist[name]["type"] == "function":
                                    functionResult = self.execute(
                                        self.datalist[name]["value"],
                                        startAtCol=self.datalist[name]["startAtCol"],
                                        executionMethod=executionMethod,
                                        quickMode=quickMode,
                                        silentMode=silentMode,
                                    )
                                    if functionResult.status == 1:
                                        return self._gErr(functionResult.message)
                                    else:
                                        result += functionResult.result
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case "L":
                            try:
                                self.datalist[name]["type"] = "linkcell"
                                self.datalist[name]["value"] = self.cursor
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case "D":
                            # delete data
                            try:
                                del self.datalist[name]
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case "F":
                            try:
                                col += 1

                                # next, we receive a character.
                                endChar = code[col - startAtCol]
                                functionBody = ""
                                self.datalist[name]["startAtCol"] = col + 1
                                while True:
                                    try:
                                        col += 1
                                        if code[col - startAtCol] == endChar:
                                            break
                                        functionBody += code[col - startAtCol]
                                    except IndexError:
                                        return self._gErr(
                                            "The function definition is not properly closed",
                                            col=col,
                                        )
                                self.datalist[name]["type"] = "function"
                                self.datalist[name]["value"] = functionBody
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case "S":
                            try:
                                col += 1

                                endChar = code[col - startAtCol]
                                stringBody = ""
                                while True:
                                    try:
                                        col += 1
                                        if code[col - startAtCol] == endChar:
                                            break
                                        if code[col - startAtCol] == "\\":
                                            col += 1
                                            match code[col - startAtCol]:
                                                case "e":
                                                    stringBody += endChar
                                                case "n":
                                                    stringBody += "\n"
                                                case "t":
                                                    stringBody += "\t"
                                                case "r":
                                                    stringBody += "\r"
                                                case "\\":
                                                    stringBody += "\\"
                                                case _:
                                                    if not silentMode:
                                                        warnings.warn(
                                                            f"\n[TRAWPAW col:{col}] Do not use escape char '\\' in string definition anymore.\nSuggestion: use '\\\\' instead"
                                                        )
                                                    stringBody += (
                                                        "\\" + code[col - startAtCol]
                                                    )
                                        else:
                                            stringBody += code[col - startAtCol]

                                    except IndexError:
                                        return self._gErr(
                                            "The function definition is not properly closed",
                                            col=col,
                                        )
                                self.datalist[name]["type"] = "string"
                                self.datalist[name]["value"] = stringBody
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case "=":
                            try:
                                try:
                                    col += 1
                                    if code[col - startAtCol] == "$":
                                        col += 1
                                        try:
                                            self.datalist[name] = self.datalist[
                                                code[col - startAtCol]
                                            ].copy()
                                        except KeyError:
                                            return self._gErr(
                                                f"Data '{code[col - startAtCol]}' is not initialized",
                                                col=col,
                                            )
                                    elif code[col - startAtCol] == "@":
                                        col += 1
                                        if code[col - startAtCol].upper() == "C":
                                            self.datalist[name]["type"] = "number"
                                            self.datalist[name]["value"] = self.cursor
                                        else:
                                            return self._gErr("Storeable only")
                                    else:
                                        return self._gErr(
                                            f'Follow "$" or "@ after controller "=" at col {col}.'
                                        )
                                except IndexError:
                                    return self._gErr(
                                        f'Follow "$" or "@" after controller "=", not null at col {col}.'
                                    )
                            except KeyError:
                                return self._gErr(
                                    f"Data '{name}' is not initialized", col=col
                                )
                        case _:
                            return self._gErr("Invalid data controller", col=col)

                dataDefinition = False
            col += 1
        if bracketlist:
            return self._gErr("Bracket is not closed", col=col)
        if clearData:
            self.clearData()
        return Trst(
            {
                "status": 0,
                "result": result,
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        )
