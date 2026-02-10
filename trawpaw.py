"""
REQUIREMENT:

Python 3.12+

------------------------------
Code         :Type             :Usage
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
+            :                 :Increment current memory cell value by 1 (mod maxvaluepermem+1)
-            :                 :Decrement current memory cell value by 1 (mod maxvaluepermem+1)
*            :                 :Multiply current memory cell value by 2 (mod maxvaluepermem+1)
/            :                 :Divide current memory cell value by 2 (integer division, mod maxvaluepermem+1)
#            :                 :Set current memory cell value to 0 (normal) or move cursor to memory 0 (! modifier) or clear data (including variables) (!! modifier)
<            :                 :Move cursor left by 1 (circular)
>            :                 :Move cursor right by 1 (circular)
,            :                 :Read a character input, store its ASCII code in current cell <if got input> or store 0 <otherwise>
.            :                 :Output cell as ASCII char (normal) or number (! modifier)
$            :                 :Define/Call data (followed by [name][controller], normal) or call module (! modifier)
@            :                 :Debug (~debug mark)
_            :                 :Pause execution for 1s (normal) or 0.1s (! modifier)
&            :                 :Breakpoint for debugging (waits for user input to continue) (normal) Quit program and return result (! modifier)
!            :Special          :Modify next command's behavior (special mode)
[pattern]    :Bracket          :Loop twice (normal) 50% chance skip all inside (! modifier)
(pattern)    :Bracket          :Normal: skip if cell=0; !: skip if cell≠0
{pattern}    :Bracket          :Comment
I            :VarController    :Init/reset variable (used after $[name])
W            :VarController    :Write current cell value to variable (used after $[name])
R            :VarController    :Read variable value to current cell (used after $[name])
L            :VarController    :Link variable to current cursor position (used after $[name])
D            :VarController    :Delete variable (used after $[name])
F            :VarController    :Define a function (used after $[name])
S            :VarController    :Define a string variable (used after $[name])
V            :DebugMark        :Show current list of variables
C            :DebugMark        :Show current address of cursor

runbf        :Module           :Run a Brainfuck code stored in a function variable
| Syntax: `!$runbf[bf_code: variable<function>]`

runwaste     :Module           :Run a Waste code stored in a function variable, save result to a variable
| Syntax: `!$runwaste[waste_code: variable<function>][save_in_waste_storeto: variable]`

include      :Module           :Include and run a Trawpaw code from a file (influences current data)
| Syntax: `!$include[file_path: variable<string>]`

virtual      :Module           :Create a virtual Trawpaw object to run a Trawpaw code <typeof variable is function> or from a file <typeof variable is string> (isolated data)
| Syntax: `!$virtual[code_or_filepath: variable<string | function>]`

print        :Module           :Print a string variable
| Syntax: `!$print[value: variable<string>]`

getinput     :Module           :Get user input and store it in a string variable
| Syntax: `!$getinput[hint: variable<string>][result_storeto: variable<any>]`

string
    addto      :Module           :Add this cell's value to a string variable as a character (appending)
    | Syntax: `!$string.addto[addto: variable<string>]`

    inserttofirst :Module        :Add this cell's value to the beginning of a string variable as a character
    | Syntax: `!$string.inserttofirst[addto: variable<string>]`

    length     :Module           :Get the length of a string variable, store it in current cell
    | Syntax: `!$string.length[original_str: variable<string>]`

    reverse    :Module           :Reverse a string variable
    | Syntax: `!$string.reverse[original_str: variable<string>]`

    toupper    :Module           :Convert a string variable to uppercase
    | Syntax: `!$string.toupper[original_str: variable<string>]`

    tolower    :Module           :Convert a string variable to lowercase
    | Syntax: `!$string.tolower[original_str: variable<string>]`

    encodeuri  :Module           :URL-encode a string variable
    | Syntax: `!$string.encodeuri[original_str: variable<string>]`

    decodeuri  :Module           :URL-decode a string variable
    | Syntax: `!$string.decodeuri[original_str: variable<string>]`

    escape     :Module           :HTML-escape a string variable
    | Syntax: `!$string.escape[original_str: variable<string>]`

    unescape   :Module           :HTML-unescape a string variable
    | Syntax: `!$string.unescape[original_str: variable<string>]`

hash
    md5        :Module           :MD5-hash a string variable
    | Syntax: `!$hash.md5[original_str: variable<string>]`

    sha1       :Module           :SHA1-hash a string variable
    | Syntax: `!$hash.sha1[original_str: variable<string>]`

    sha224     :Module           :SHA224-hash a string variable
    | Syntax: `!$hash.sha224[original_str: variable<string>]`

    sha256     :Module           :SHA256-hash a string variable
    | Syntax: `!$hash.sha256[original_str: variable[string>]`

    sha384     :Module           :SHA384-hash a string variable
    | Syntax: `!$hash.sha384[original_str: variable[string>]`

    sha512     :Module           :SHA512-hash a string variable
    | Syntax: `!$hash.sha512[original_str: variable[string>]`

base64
    encode     :Module           :Base64-encode a string variable
    | Syntax: `!$base64.encode[original_str: variable[string>]`

    decode     :Module           :Base64-decode a string variable
    | Syntax: `!$base64.decode[original_str: variable[string>]`

------------------------------
ADDITIONAL NOTES:
1. Bracket commands ([ ( {) must be properly closed with ] ) } respectively
2. Variable definition syntax: "$[one-length char name][variable controller]"
3. Function syntax & String syntax: "$[x]["f"|"s"][y][body][y]" x: variable name, y: EOS (End of setence) Character (One length), body: function body
4. Debug syntax: "@[debug mark]"
5. clearData=True in execute() resets memories and datalist to initial state
6. Variable in module calling must syntaxed "$[name]" (no controller)

"""

VERSION: str = "5.2_1"

############# THE BEGINNING OF THE SOURCE #############

from random import randint
from time import sleep
import sys, os, enum, urllib.parse, hashlib, base64


class TrawpawExecutionMethod(enum.Enum):
    printManually = 0
    storeInResult = 1


class Trawpaw:
    def __init__(self, memories: int = 128, maxvaluepermem: int = 127) -> None:
        assert memories > 0, "Number of memories must be greater than 0."
        assert maxvaluepermem >= 0, (
            "Max value per memory must be greater than or equals 0."
        )
        assert memories <= 65536, (
            "Number of memories must be less than or equals 65536."
        )
        assert maxvaluepermem < 65536, "Max value per memory must be less than 65536."

        self.memories: list[int] = []
        self.nullmem: list[int] = []

        for _ in range(memories):
            self.memories.append(0)
        self.nullmem = self.memories.copy()

        self.maxvaluepermem = maxvaluepermem + 1

        self.datalist = {}
        self.cursor: int = 0

    def clearData(self):
        self.memories = self.nullmem.copy()
        self.datalist = {}
        self.cursor = 0

    def runBrainfk(
        self,
        code: str,
        getinput: str = "",
        startAtCol: int = 0,
        execution_method: TrawpawExecutionMethod = TrawpawExecutionMethod.printManually,
    ) -> dict:
        inputcur: int = 0
        bracketlist: list[int] = []
        result: str = ""
        col: int = startAtCol
        while col - startAtCol < len(code):
            match code[col - startAtCol]:
                case "+":
                    self.memories[self.cursor] = (
                        self.memories[self.cursor] + 1
                    ) % self.maxvaluepermem
                case "-":
                    self.memories[self.cursor] = (
                        self.memories[self.cursor] - 1
                    ) % self.maxvaluepermem
                case "<":
                    self.cursor = (self.cursor - 1) % len(self.memories)
                case ">":
                    self.cursor = (self.cursor + 1) % len(self.memories)
                case ",":
                    try:
                        self.memories[self.cursor] = (
                            ord(getinput[inputcur]) % self.maxvaluepermem
                        )
                        inputcur += 1
                    except:
                        ginput = input("[input<char>] ")
                        if ginput:
                            self.memories[self.cursor] = (
                                ord(ginput[0]) % self.maxvaluepermem
                            )
                        else:
                            self.memories[self.cursor] = 0
                case ".":
                    if execution_method == TrawpawExecutionMethod.printManually:
                        print(chr(self.memories[self.cursor]), end="")
                        sys.stdout.flush()
                    result += chr(self.memories[self.cursor])
                case "[":
                    bracketlist.append(col)
                case "]":
                    if self.memories[self.cursor] != 0:
                        col = bracketlist[-1]
                    else:
                        bracketlist.pop()
            col += 1
        if len(bracketlist) != 0:
            return {
                "status": 1,
                "message": f"ERR: Bracket is not closed at col {col}.",
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        return {
            "status": 0,
            "result": result,
            "cursor": self.cursor,
            "datalistlength": len(self.datalist),
        }

    def runWaste(
        self,
        code: str,
        saveto: str,
        startAtCol: int = 0,
        execution_method: TrawpawExecutionMethod = TrawpawExecutionMethod.printManually,
    ) -> dict:
        """
        Waste esolang executor, ported from JS, using match-case.
        """
        saved: int = 0
        ptr: int = self.memories[self.cursor]
        try:
            saved = self.datalist.get(saveto, 0)
        except:
            return {
                "status": 1,
                "message": f"ERR: Data '{saveto}' is not initialized.",
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        out: str = ""
        bracketStack = []
        col: int = startAtCol
        while col - startAtCol < len(code):
            match code[col - startAtCol]:
                case "＜" | "<":
                    saved = ptr
                case "＞" | ">":
                    ptr = saved
                case "＾" | "^":
                    ptr = 0 if randint(0, 1) == 0 else 1
                case "＠" | "@":
                    if execution_method == TrawpawExecutionMethod.printManually:
                        os.system("cls" if os.name == "nt" else "clear")
                    out = ""
                case "，" | ",":
                    if execution_method == TrawpawExecutionMethod.printManually:
                        print(code[col - startAtCol + 1 :], end="")
                        sys.stdout.flush()
                    out += code[col - startAtCol + 1 :]
                    break
                case "＃" | "#":
                    ptr = 0
                case "+":
                    self.memories[self.cursor] = (
                        self.memories[self.cursor] + 1
                    ) % self.maxvaluepermem
                case "-":
                    self.memories[self.cursor] = (
                        self.memories[self.cursor] - 1
                    ) % self.maxvaluepermem
                case "*":
                    self.memories[self.cursor] = (
                        self.memories[self.cursor] * 2
                    ) % self.maxvaluepermem
                case "/":
                    self.memories[self.cursor] = (
                        self.memories[self.cursor] // 2
                    ) % self.maxvaluepermem
                case "％" | "%":
                    if execution_method == TrawpawExecutionMethod.printManually:
                        print(str(ptr), end="")
                        sys.stdout.flush()
                    out += str(ptr)
                case "＆" | "&":
                    input("Breakpoint reached. Press Enter to continue...")
                case "．" | ".":
                    try:
                        if execution_method == TrawpawExecutionMethod.printManually:
                            print(chr(ptr), end="")
                            sys.stdout.flush()
                        out += chr(ptr)
                    except Exception:
                        if execution_method == TrawpawExecutionMethod.printManually:
                            print("?", end="")
                            sys.stdout.flush()
                        out += "?"
                case "：" | ":":
                    if execution_method == TrawpawExecutionMethod.printManually:
                        print("\n", end="")
                        sys.stdout.flush()
                    out += "\n"
                case "？" | "?":
                    sleep(0.001)
                case "！" | "!":
                    return {
                        "status": 2,
                        "result": out,
                        "cursor": self.cursor,
                        "datalistlength": len(self.datalist),
                    }
                case "［" | "[":
                    bracketStack.append({"type": "]", "position": col, "currranges": 0})
                case "］" | "]":
                    if not bracketStack or bracketStack[-1]["type"] != "]":
                        return {
                            "status": 1,
                            "message": f"Unmatched closing bracket at position {col}",
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    else:
                        if bracketStack[-1]["currranges"] > 0:
                            bracketStack.pop()
                        else:
                            bracketStack[-1]["currranges"] += 1
                            col = bracketStack[-1]["position"]
                case "（" | "(":
                    bracketStack.append({"type": ")", "position": col})
                    # 50% chance skip all inside
                    if randint(0, 1) == 0:
                        innerBrackets = [{"type": "(", "position": col}]
                        while innerBrackets:
                            col += 1
                            if col - startAtCol >= len(code):
                                return {
                                    "status": 1,
                                    "message": "Unclosed bracket",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                            c = code[col - startAtCol]
                            match c:
                                case "（" | "(":
                                    innerBrackets.append({"type": "(", "position": col})
                                case "｛" | "{":
                                    innerBrackets.append({"type": "}", "position": col})
                                case "［" | "[":
                                    innerBrackets.append({"type": "]", "position": col})
                                case "）" | ")" | "］" | "]" | "｝" | "}":
                                    lb = innerBrackets.pop()
                                    if not innerBrackets:
                                        if lb["type"] != ")":
                                            return {
                                                "status": 1,
                                                "message": f"Mismatched brackets at position {col}",
                                                "cursor": self.cursor,
                                                "datalistlength": len(self.datalist),
                                            }
                case "）" | ")":
                    if not bracketStack or bracketStack[-1]["type"] != ")":
                        return {
                            "status": 1,
                            "message": f"Unmatched closing bracket at position {col}",
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    else:
                        bracketStack.pop()
                case "｛" | "{":
                    innerBrackets = [{"type": "{", "position": col}]
                    while innerBrackets:
                        col += 1
                        if col - startAtCol >= len(code):
                            return {
                                "status": 1,
                                "message": f"Unclosed bracket at position {col}",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        c = code[col - startAtCol]
                        match c:
                            case "（" | "(":
                                innerBrackets.append({"type": "(", "position": col})
                            case "｛" | "{":
                                innerBrackets.append({"type": "}", "position": col})
                            case "［" | "[":
                                innerBrackets.append({"type": "]", "position": col})
                            case "）" | ")" | "］" | "]" | "｝" | "}":
                                lb = innerBrackets.pop()
                                if not innerBrackets:
                                    if lb["type"] != "}":
                                        return {
                                            "status": 1,
                                            "message": f"Mismatched brackets at position {col}",
                                            "cursor": self.cursor,
                                            "datalistlength": len(self.datalist),
                                        }
                case "｝" | "}":
                    if not bracketStack or bracketStack[-1]["type"] != "}":
                        return {
                            "status": 1,
                            "message": f"Unmatched closing bracket at position {col}",
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    else:
                        bracketStack.pop()
            col += 1

        # Save result to datalist
        try:
            self.memories[self.cursor] = ptr
            self.datalist[saveto]["type"] = "number"
            self.datalist[saveto]["value"] = saved
            return {
                "status": 0,
                "result": out,
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        except:
            return {
                "status": 1,
                "message": f"ERR: Data '{saveto}' is not initialized.",
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }

    def execute(
        self,
        code: str,
        getinput: str = "",
        clearData: bool = False,
        startAtCol: int = 0,
        execution_method: TrawpawExecutionMethod = TrawpawExecutionMethod.printManually,
    ) -> dict:
        inputcur: int = 0
        bracketlist: list[dict] = []
        result: str = ""
        col: int = startAtCol
        data_definition: bool = False
        special: int = 0
        while col - startAtCol < len(code):
            if not data_definition:
                match code[col - startAtCol]:
                    case "+":
                        self.memories[self.cursor] = (
                            self.memories[self.cursor] + 1
                        ) % self.maxvaluepermem
                        special = 0
                    case "-":
                        self.memories[self.cursor] = (
                            self.memories[self.cursor] - 1
                        ) % self.maxvaluepermem
                        special = 0
                    case "*":
                        self.memories[self.cursor] = (
                            self.memories[self.cursor] * 2
                        ) % self.maxvaluepermem
                        special = 0
                    case "/":
                        self.memories[self.cursor] = (
                            self.memories[self.cursor] // 2
                        ) % self.maxvaluepermem
                        special = 0
                    case "#":
                        if special >= 2:
                            self.clearData()
                        elif special == 1:
                            self.cursor = 0
                        else:
                            self.memories[self.cursor] = 0
                        special = 0
                    case "<":
                        self.cursor = (self.cursor - 1) % len(self.memories)
                        special = 0
                    case ">":
                        self.cursor = (self.cursor + 1) % len(self.memories)
                        special = 0
                    case ",":
                        try:
                            self.memories[self.cursor] = (
                                ord(getinput[inputcur]) % self.maxvaluepermem
                            )
                            inputcur += 1
                        except:
                            original_input = input("[input<char>] ")
                            if original_input:
                                self.memories[self.cursor] = (
                                    ord(original_input[0]) % self.maxvaluepermem
                                )
                            else:
                                self.memories[self.cursor] = 0
                        special = 0
                    case ".":
                        if special:
                            if execution_method == TrawpawExecutionMethod.printManually:
                                print(str(self.memories[self.cursor]), end="")
                                sys.stdout.flush()  # F**k your IO buffer
                            result += str(self.memories[self.cursor])
                        else:
                            if execution_method == TrawpawExecutionMethod.printManually:
                                print(chr(self.memories[self.cursor]), end="")
                                sys.stdout.flush()
                            result += chr(self.memories[self.cursor])
                        special = 0
                    case "$":
                        data_definition = True
                    case "_":
                        if special:
                            sleep(0.1)
                        else:
                            sleep(1)
                        special = 0
                    case "&":
                        # Breakpoint for debugging
                        if special:
                            return {
                                "status": 2,
                                "result": result,
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        else:
                            input("Breakpoint reached. Press Enter to continue...")
                        special = 0
                    case "!":
                        special += 1
                    case "@":
                        col += 1
                        if code[col - startAtCol].upper() == "V":
                            if execution_method == TrawpawExecutionMethod.printManually:
                                print(str(self.datalist), end="")
                                sys.stdout.flush()
                            result += str(self.datalist)
                        elif code[col - startAtCol].upper() == "C":
                            if execution_method == TrawpawExecutionMethod.printManually:
                                print(str(self.cursor), end="")
                                sys.stdout.flush()
                            result += str(self.cursor)
                        else:
                            return {
                                "status": 1,
                                "message": "ERR: Invalid debug mark",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        special = 0
                    case "[":
                        bracketlist.append(
                            {
                                "bracket": "[",
                                "col": col,
                                "special": bool(special),
                                "ranges": 0,
                            }
                        )
                        if bool(special):
                            if not randint(0, 1):
                                token = 1
                                while token:
                                    col += 1
                                    if code[col - startAtCol] in ["[", "{", "("]:
                                        token += 1
                                    if code[col - startAtCol] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col - startAtCol] != "]":
                                                return {
                                                    "status": 1,
                                                    "message": f"ERR: This bracket is not properly closed at col {col}.",
                                                    "cursor": self.cursor,
                                                    "datalistlength": len(
                                                        self.datalist
                                                    ),
                                                }
                                            else:
                                                token -= 1
                                        else:
                                            token -= 1
                                bracketlist.pop()
                        special = 0
                    case "(":
                        bracketlist.append(
                            {"bracket": "(", "col": col, "special": bool(special)}
                        )
                        if bool(special):
                            if self.memories[self.cursor] != 0:
                                token = 1
                                while token:
                                    col += 1
                                    if code[col - startAtCol] in ["[", "{", "("]:
                                        token += 1
                                    if code[col - startAtCol] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col - startAtCol] != ")":
                                                return {
                                                    "status": 1,
                                                    "message": f"ERR: This bracket is not properly closed at col {col}.",
                                                    "cursor": self.cursor,
                                                    "datalistlength": len(
                                                        self.datalist
                                                    ),
                                                }
                                            else:
                                                token -= 1
                                        else:
                                            token -= 1
                                bracketlist.pop()
                        else:
                            if self.memories[self.cursor] == 0:
                                token = 1
                                while token:
                                    col += 1
                                    if code[col - startAtCol] in ["[", "{", "("]:
                                        token += 1
                                    if code[col - startAtCol] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col - startAtCol] != ")":
                                                return {
                                                    "status": 1,
                                                    "message": f"ERR: This bracket is not properly closed at col {col}.",
                                                    "cursor": self.cursor,
                                                    "datalistlength": len(
                                                        self.datalist
                                                    ),
                                                }
                                            else:
                                                token -= 1
                                        else:
                                            token -= 1
                                bracketlist.pop()
                        special = 0
                    case "{":
                        bracketlist.append(
                            {"bracket": "{", "col": col, "special": bool(special)}
                        )

                        token = 1
                        while token:
                            col += 1
                            if code[col - startAtCol] in ["[", "{", "("]:
                                token += 1
                            if code[col - startAtCol] in ["]", "}", ")"]:
                                if token == 1:
                                    if code[col - startAtCol] != "}":
                                        return {
                                            "status": 1,
                                            "message": f"ERR: This bracket is not properly closed at col {col}.",
                                            "cursor": self.cursor,
                                            "datalistlength": len(self.datalist),
                                        }
                                    else:
                                        token -= 1
                                else:
                                    token -= 1
                        bracketlist.pop()
                        special = 0
                    case "]":
                        if not bracketlist:
                            return {
                                "status": 1,
                                "message": f"ERR: This bracket is not properly opened at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        elif bracketlist[-1]["bracket"] != "[":
                            return {
                                "status": 1,
                                "message": f"ERR: This bracket is not properly closed at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        elif bracketlist[-1]["special"]:
                            pass
                        elif bracketlist[-1]["ranges"] == 0:
                            col = bracketlist[-1]["col"]
                            bracketlist[-1]["ranges"] += 1
                        else:
                            bracketlist.pop()
                        special = 0
            elif data_definition:
                if special:
                    dofunction = ""
                    while code[col - startAtCol] != "$":
                        dofunction += code[col - startAtCol]
                        col += 1
                    if dofunction == "runbf":
                        col += 1
                        name = code[col - startAtCol]
                        try:
                            if self.datalist[name]["type"] == "function":
                                function_result = self.runBrainfk(
                                    self.datalist[name]["value"],
                                    startAtCol=self.datalist[name]["startAtCol"],
                                    execution_method=execution_method,
                                )
                                if function_result["status"] == 1:
                                    return {
                                        "status": 1,
                                        "message": function_result["message"],
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                                else:
                                    result += function_result["result"]
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a function at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        except:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "runwaste":
                        col += 1
                        name = code[col - startAtCol]
                        col += 1
                        if code[col - startAtCol] != "$":
                            return {
                                "status": 1,
                                "message": f"ERR: Invalid waste module call syntax at col {col}",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        else:
                            col += 1
                            varname = code[col - startAtCol]
                            try:
                                if self.datalist[name]["type"] == "function":
                                    function_result = self.runWaste(
                                        self.datalist[name]["value"],
                                        varname,
                                        startAtCol=self.datalist[name]["startAtCol"],
                                        execution_method=execution_method,
                                    )
                                    if function_result["status"] == 1:
                                        return {
                                            "status": 1,
                                            "message": function_result["message"],
                                            "cursor": self.cursor,
                                            "datalistlength": len(self.datalist),
                                        }
                                    else:
                                        result += function_result["result"]
                                else:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Variable must be a function at col {col}",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            except:
                                return {
                                    "status": 1,
                                    "message": f"ERR: (One of) arguments is not initialized at col {col}.",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
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
                                        include_code = f.read()
                                        f.close()
                                    function_result = self.execute(
                                        include_code, startAtCol=0
                                    )
                                    if function_result["status"] == 1:
                                        return {
                                            "status": 1,
                                            "message": function_result["message"]
                                            + f" in file {self.datalist[varname]['value']}",
                                            "cursor": self.cursor,
                                            "datalistlength": len(self.datalist),
                                        }
                                    else:
                                        result += function_result["result"]
                                except FileNotFoundError:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Included file {self.datalist[varname]['value']} not found at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "virtual":
                        col += 1
                        varname = code[col - startAtCol]
                        another_trawpaw_object = Trawpaw(
                            len(self.memories), self.maxvaluepermem - 1
                        )
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                try:
                                    with open(
                                        self.datalist[varname]["value"],
                                        "r",
                                        encoding="utf-8",
                                    ) as f:
                                        include_code = f.read()
                                        f.close()
                                    function_result = another_trawpaw_object.execute(
                                        include_code,
                                        startAtCol=0,
                                        execution_method=execution_method,
                                    )
                                    if function_result["status"] == 1:
                                        return {
                                            "status": 1,
                                            "message": function_result["message"]
                                            + f" in file {self.datalist[varname]['value']}",
                                            "cursor": self.cursor,
                                            "datalistlength": len(self.datalist),
                                        }
                                    # else:
                                    #     result += function_result["result"]
                                except FileNotFoundError:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Included file '{self.datalist[varname]['value']}' not found at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            elif self.datalist[varname]["type"] == "function":
                                include_code = self.datalist[varname]["value"]
                                function_result = another_trawpaw_object.execute(
                                    include_code,
                                    startAtCol=self.datalist[varname]["startAtCol"],
                                    execution_method=execution_method,
                                )
                                if function_result["status"] == 1:
                                    return {
                                        "status": 1,
                                        "message": function_result["message"],
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                                else:
                                    result += function_result["result"]
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string or a function at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "print":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                if (
                                    execution_method
                                    == TrawpawExecutionMethod.printManually
                                ):
                                    print(self.datalist[varname]["value"], end="")
                                    sys.stdout.flush()
                                result += self.datalist[varname]["value"]
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "getinput":
                        col += 1
                        hint = code[col - startAtCol]
                        col += 1
                        if code[col - startAtCol] != "$":
                            return {
                                "status": 1,
                                "message": f"ERR: Invalid waste module call syntax at col {col}",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                        else:
                            col += 1
                            storeto = code[col - startAtCol]
                            try:
                                if self.datalist[hint]["type"] != "string":
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Hint must be a string at col {col}",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }

                                inp_result = input(self.datalist[hint]["value"])
                                self.datalist[storeto]["type"] = "string"
                                self.datalist[storeto]["value"] = inp_result
                            except:
                                return {
                                    "status": 1,
                                    "message": f"ERR: (One of) arguments is not initialized at col {col}.",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                    elif dofunction == "string.addto":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                self.datalist[varname]["value"] += chr(
                                    self.memories[self.cursor]
                                )
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.inserttofirst":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                self.datalist[varname]["value"] = self.datalist[
                                    varname
                                ]["value"][::-1]
                                self.datalist[varname]["value"] += chr(
                                    self.memories[self.cursor]
                                )
                                self.datalist[varname]["value"] = self.datalist[
                                    varname
                                ]["value"][::-1]
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }

                    elif dofunction == "string.length":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                string_length = len(self.datalist[varname]["value"])
                                self.memories[self.cursor] = (
                                    string_length % self.maxvaluepermem
                                )
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.reverse":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = self.datalist[varname]["value"][::-1]
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.toupper":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = self.datalist[varname]["value"].upper()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.tolower":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = self.datalist[varname]["value"].lower()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.encodeuri":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = urllib.parse.quote(
                                    self.datalist[varname]["value"]
                                )
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.decodeuri":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = urllib.parse.unquote(
                                    self.datalist[varname]["value"]
                                )
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.escape":
                        escape = {
                            "&": "&amp;",
                            "<": "&lt;",
                            ">": "&gt;",
                            "©": "&copy;",
                            "®": "&reg;",
                            '"': "&quot;",
                            " ": "&nbsp;",
                            "\n": "<br>",
                        }
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = self.datalist[varname]["value"]
                                for k, v in escape.items():
                                    new_string = new_string.replace(k, v)
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "string.unescape":
                        escape = {
                            "®": "&reg;",
                            " ": "&nbsp;",
                            '"': "&quot;",
                            "\n": "<br>",
                            "&": "&amp;",
                            "<": "&lt;",
                            ">": "&gt;",
                            "©": "&copy;",
                        }
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = self.datalist[varname]["value"]
                                for k, v in list(escape.items())[::-1]:
                                    new_string = new_string.replace(v, k)
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "hash.md5":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = hashlib.md5(
                                    self.datalist[varname]["value"].encode()
                                ).hexdigest()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "hash.sha1":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = hashlib.sha1(
                                    self.datalist[varname]["value"].encode()
                                ).hexdigest()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "hash.sha224":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = hashlib.sha224(
                                    self.datalist[varname]["value"].encode()
                                ).hexdigest()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "hash.sha256":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = hashlib.sha256(
                                    self.datalist[varname]["value"].encode()
                                ).hexdigest()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "hash.sha384":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = hashlib.sha384(
                                    self.datalist[varname]["value"].encode()
                                ).hexdigest()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "hash.sha512":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = hashlib.sha512(
                                    self.datalist[varname]["value"].encode()
                                ).hexdigest()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "base64.encode":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = base64.b64encode(
                                    self.datalist[varname]["value"].encode()
                                ).decode()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    elif dofunction == "base64.decode":
                        col += 1
                        varname = code[col - startAtCol]
                        if self.datalist.get(varname):
                            if self.datalist[varname]["type"] == "string":
                                new_string = base64.b64decode(
                                    self.datalist[varname]["value"].encode()
                                ).decode()
                                self.datalist[varname]["value"] = new_string
                            else:
                                return {
                                    "status": 1,
                                    "message": f"ERR: Variable must be a string at col {col}",
                                    "cursor": self.cursor,
                                    "datalistlength": len(self.datalist),
                                }
                        else:
                            return {
                                "status": 1,
                                "message": f"ERR: Data '{varname}' is not initialized at col {col}.",
                                "cursor": self.cursor,
                                "datalistlength": len(self.datalist),
                            }
                    else:
                        return {
                            "status": 1,
                            "message": f"ERR: Unknown module at col {col}",
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    special = 0
                else:
                    # Define a single-character data constant, the next character is the data controller I means init and reset W means write R means read
                    name: str = code[col - startAtCol]
                    col += 1
                    controller: str = code[col - startAtCol]
                    if controller.upper() not in ["I", "W", "R", "L", "D", "F", "S"]:
                        return {
                            "status": 1,
                            "message": f"ERR: Invalid data controller at col {col}.",
                            "cursor": self.cursor,
                            "datalistlength": len(self.datalist),
                        }
                    else:
                        match controller.upper():
                            case "I":
                                self.datalist[name] = {"type": "number", "value": 0}
                            case "W":
                                try:
                                    self.datalist[name]["type"] = "number"
                                    self.datalist[name]["value"] = self.memories[
                                        self.cursor
                                    ]
                                except:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            case "R":
                                try:
                                    if self.datalist[name]["type"] == "number":
                                        self.memories[self.cursor] = self.datalist[
                                            name
                                        ]["value"]
                                    elif self.datalist[name]["type"] == "linkmemory":
                                        self.memories[self.cursor] = self.memories[
                                            self.datalist[name]["value"]
                                        ]
                                    elif self.datalist[name]["type"] == "function":
                                        function_result = self.execute(
                                            self.datalist[name]["value"],
                                            startAtCol=self.datalist[name][
                                                "startAtCol"
                                            ],
                                            execution_method=execution_method,
                                        )
                                        if function_result["status"] == 1:
                                            return {
                                                "status": 1,
                                                "message": function_result["message"],
                                                "cursor": self.cursor,
                                                "datalistlength": len(self.datalist),
                                            }
                                        else:
                                            result += function_result["result"]
                                except:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            case "L":
                                try:
                                    self.datalist[name]["type"] = "linkmemory"
                                    self.datalist[name]["value"] = self.cursor
                                except:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            case "D":
                                # delete data
                                try:
                                    del self.datalist[name]
                                except:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            case "F":
                                try:
                                    col += 1

                                    # next, we receive a character.
                                    end_char = code[col - startAtCol]
                                    function_body = ""
                                    self.datalist[name]["startAtCol"] = col + 1
                                    while True:
                                        try:
                                            col += 1
                                            if code[col - startAtCol] == end_char:
                                                break
                                            else:
                                                function_body += code[col - startAtCol]
                                        except IndexError:
                                            return {
                                                "status": 1,
                                                "message": f"ERR: The function definition is not properly closed at col {col}.",
                                                "cursor": self.cursor,
                                                "datalistlength": len(self.datalist),
                                            }
                                    self.datalist[name]["type"] = "function"
                                    self.datalist[name]["value"] = function_body
                                except KeyError:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }
                            case "S":
                                try:
                                    col += 1

                                    # next, we receive a character.
                                    end_char = code[col - startAtCol]
                                    string_body = ""
                                    while True:
                                        try:
                                            col += 1
                                            if code[col - startAtCol] == end_char:
                                                break
                                            else:
                                                string_body += code[col - startAtCol]

                                        except IndexError:
                                            return {
                                                "status": 1,
                                                "message": f"ERR: The function definition is not properly closed at col {col}.",
                                                "cursor": self.cursor,
                                                "datalistlength": len(self.datalist),
                                            }
                                    self.datalist[name]["type"] = "string"
                                    self.datalist[name]["value"] = string_body
                                except KeyError:
                                    return {
                                        "status": 1,
                                        "message": f"ERR: Data '{name}' is not initialized at col {col}.",
                                        "cursor": self.cursor,
                                        "datalistlength": len(self.datalist),
                                    }

                data_definition = False
                # col += 1
            col += 1
        if bracketlist:
            return {
                "status": 1,
                "message": f"ERR: Bracket is not closed at col {col}.",
                "cursor": self.cursor,
                "datalistlength": len(self.datalist),
            }
        if clearData:
            self.clearData()
        return {
            "status": 0,
            "result": result,
            "cursor": self.cursor,
            "datalistlength": len(self.datalist),
        }


def main():
    try:
        from argparse import ArgumentParser, RawTextHelpFormatter, Namespace

        # F**k your ^[[D on linux, to fix this sh*t, I have to spend a lot of times to fix it, it will makes my program SLOWER + I didnt know will it work.
        from prompt_toolkit import prompt  # type: ignore

        parser = ArgumentParser(
            usage="trawpaw.py [options] <file>",
            description="Trawpaw Interpreter v" + VERSION,
            formatter_class=RawTextHelpFormatter,
        )
        parser.add_argument(
            "--usage",
            "-u",
            action="store_true",
            help="Show usage information and quit.",
        )
        parser.add_argument(
            "file", nargs="?", help="Path to the Trawpaw source code file."
        )
        parser.add_argument(
            "--memories",
            "-m",
            type=int,
            default=128,
            help="Number of memory cells to use (1 <= memories <= 65536) (default: 128).",
        )
        parser.add_argument(
            "--maxvaluepermem",
            "-v",
            type=int,
            default=127,
            help="Maximum value per memory cell (0 <= maxvaluepermem <= 65535) (default: 127).",
        )
        parser.add_argument("--waste", action="store_true", help="Run waste code")

        args: Namespace = parser.parse_args()
        trawpaw: Trawpaw
        try:
            trawpaw = Trawpaw(args.memories, args.maxvaluepermem)
        except AssertionError as e:
            print(f"ERR: {e}")
            sys.exit(1)

        if args.usage:
            print(__doc__)
            sys.exit(0)
        elif args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                code: str = f.read()
                if args.waste:
                    trawpaw.datalist["a"] = {"type": "number", "value": 0}
                    trawpaw_result = trawpaw.runWaste(code, "a")
                else:
                    trawpaw_result = trawpaw.execute(code)
                print(end="\n")
                if trawpaw_result["status"] == 1:
                    print(trawpaw_result.get("message", "ERR: Unknown error occurred."))
                # else:
                #     print(trawpaw_result.get("result", ""))
                f.close()
            sys.exit(0)
        else:
            print("Run `~ --usage` (~ means trawpaw src) for more information")
            print("Press Ctrl+C to exit.")
            if args.waste:
                trawpaw.datalist["a"] = {"type": "number", "value": 0}
                code = prompt("[waste] ")
            else:
                code = prompt("[c:0 v:0] ")
            while True:
                if args.waste:
                    trawpaw_result = trawpaw.runWaste(code, "a")
                else:
                    trawpaw_result = trawpaw.execute(code)
                print(end="\n")
                if trawpaw_result["status"] == 1:
                    print(trawpaw_result.get("message", "ERR: Unknown error occurred."))
                # else:
                #     print(trawpaw_result.get("result", ""))
                if args.waste:
                    code = prompt("[waste] ")
                else:
                    code = prompt(
                        f"[c:{trawpaw_result['cursor']} v:{trawpaw_result['datalistlength']}] "
                    )
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
