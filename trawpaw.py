VERSION: str = "2.0"
DOCUMENT: str = """
REQUIREMENTS:

Python 3.10+

------------------------------
Code         :Type             :Usage
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
+            :                 :Increment current memory cell value by 1 (mod maxvaluepermem+1)
-            :                 :Decrement current memory cell value by 1 (mod maxvaluepermem+1)
*            :                 :Multiply current memory cell value by 2 (mod maxvaluepermem+1)
/            :                 :Divide current memory cell value by 2 (integer division, mod maxvaluepermem+1)
#            :                 :Set current memory cell value to 0 (normal) or move cursor to memory 0 (! modifier) or clear data (!! modifier)
<            :                 :Move cursor left by 1 (circular)
>            :                 :Move cursor right by 1 (circular)
,            :                 :Read a character input, store its ASCII code in current cell
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
F            :VarController    :Define a function
V            :DebugMark        :Show current list of variables
C            :DebugMark        :Show current address of cursor
runbf        :Module           :Run a Brainfuck code stored in a function variable (syntax !$runbf$[var name: function])]
------------------------------
ADDITIONAL NOTES:
1. Bracket commands ([ ( {) must be properly closed with ] ) } respectively
2. Variable definition syntax: "$[one-length char name][variable controller]"
3. Function syntax: "$[x]f[y][body][y]" x: variable name, y: EOS (End of setence) Character (One length), body: function body
4. Debug syntax: "@[debug mark]"
5. Module syntax: "!$[module name]$[variable name]"
6. clearData=True in execute() resets memories and datalist to initial state
"""

from typing import Literal
from random import randint
from time import sleep

class Trawpaw:
    def __init__(self, memories: Literal[128 | 1024 | 65536] = 128, maxvaluepermem: Literal[127 | 1023 | 65535] = 127) -> None:
        self.memories: list[int] = []
        self.nullmem: list[int] = []

        for _ in range(memories):
            self.memories.append(0)
        self.nullmem = self.memories.copy()

        self.maxvaluepermem = maxvaluepermem+1

        self.datalist = {}
        self.cursor: int = 0

    def clearData(self):
        self.memories = self.nullmem.copy()
        self.datalist = {}
        self.cursor = 0


    def runBrainfk(self, code: str, getinput: str = "", clearData: bool = False, startAtCol: int = 0) -> dict:
        inputcur: int = 0
        bracketlist: list[int] = []
        result: str = ""
        col:int = startAtCol
        while col-startAtCol < len(code):
            match code[col-startAtCol]:
                case "+":
                    self.memories[self.cursor] = (self.memories[self.cursor] + 1) % self.maxvaluepermem
                case "-":
                    self.memories[self.cursor] = (self.memories[self.cursor] - 1) % self.maxvaluepermem
                case "<":
                    self.cursor = (self.cursor - 1) % len(self.memories)
                case ">":
                    self.cursor = (self.cursor + 1) % len(self.memories)
                case ",":
                    try:
                        self.memories[self.cursor] = ord(getinput[inputcur]) % self.maxvaluepermem
                        inputcur += 1
                    except:
                        self.memories[self.cursor] = ord(input("Input a character: ")[0]) % self.maxvaluepermem
                case ".":
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
            return {"status": 1, "message": f"ERR: Bracket is not closed at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
        if (clearData):
            self.clearData()
        return {"status": 0, "result": result, "cursor": self.cursor, "datalistlength": len(self.datalist)}

    def execute(self, code: str, getinput: str = "", clearData: bool = False, startAtCol: int = 0) -> dict:
        inputcur: int = 0
        bracketlist: list[dict] = []
        result: str = ""
        col:int = startAtCol
        data_definition: bool = False
        special: Literal[0 | 1 | 2] = 0
        while col-startAtCol < len(code):
            
            if not data_definition:
                match code[col-startAtCol]:
                    case "+":
                        self.memories[self.cursor] = (self.memories[self.cursor] + 1) % self.maxvaluepermem
                        special = 0
                    case "-":
                        self.memories[self.cursor] = (self.memories[self.cursor] - 1) % self.maxvaluepermem
                        special = 0
                    case "*":
                        self.memories[self.cursor] = (self.memories[self.cursor] * 2) % self.maxvaluepermem
                        special = 0
                    case "/":
                        self.memories[self.cursor] = (self.memories[self.cursor] // 2) % self.maxvaluepermem
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
                            self.memories[self.cursor] = ord(getinput[inputcur]) % self.maxvaluepermem
                            inputcur += 1
                        except:
                            self.memories[self.cursor] = ord(input("Input a character: ")[0]) % self.maxvaluepermem
                        special = 0
                    case ".":
                        if special:
                            result += str(self.memories[self.cursor])
                        else:
                            result += chr(self.memories[self.cursor])
                        special = 0
                    case "$":
                        data_definition = True
                    case "_":
                        if special:
                            sleep(.1)
                        else:
                            sleep(1)
                        special = 0
                    case "&":
                        #Breakpoint for debugging
                        if special:
                            return {"status": 2, "result": result, "cursor": self.cursor, "datalistlength": len(self.datalist)}
                        else:
                            input("Breakpoint reached. Press Enter to continue...")
                        special = 0
                    case "!":
                        special += 1
                    case "@":
                        col += 1;
                        if code[col-startAtCol].upper() == "V":
                            result += str(self.datalist)
                        elif code[col-startAtCol].upper() == "C":
                            result += str(self.cursor)
                        else:
                            return {"status": 1, "message": "ERR: Invalid debug mark", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                        special = 0
                    case "[":
                        bracketlist.append({
                            "bracket": "[",
                            "col": col,
                            "special": bool(special),
                            "ranges": 0
                        })
                        if bool(special):
                            if not randint(0, 1):
                                token = 1
                                while token:
                                    col += 1
                                    if code[col-startAtCol] in ["[", "{", "("]:
                                        token += 1
                                    if code[col-startAtCol] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col-startAtCol] != "]":
                                                return {"status": 1, "message": f"ERR: This bracket is not properly closed at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                                            else:
                                                token -= 1
                                        else:
                                            token -= 1
                                bracketlist.pop()
                        special = 0
                    case "(":
                        bracketlist.append({
                            "bracket": "(",
                            "col": col,
                            "special": bool(special)
                        })
                        if bool(special):
                            if self.memories[self.cursor] != 0:
                                token = 1
                                while token:
                                    col += 1
                                    if code[col-startAtCol] in ["[", "{", "("]:
                                        token += 1
                                    if code[col-startAtCol] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col-startAtCol] != ")":
                                                return {"status": 1, "message": f"ERR: This bracket is not properly closed at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
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
                                    if code[col-startAtCol] in ["[", "{", "("]:
                                        token += 1
                                    if code[col-startAtCol] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col-startAtCol] != ")":
                                                return {"status": 1, "message": f"ERR: This bracket is not properly closed at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                                            else:
                                                token -= 1
                                        else:
                                            token -= 1
                                bracketlist.pop()
                        special = 0
                    case "{":
                        bracketlist.append({
                            "bracket": "{",
                            "col": col,
                            "special": bool(special)
                        })

                        token = 1
                        while token:
                            col += 1
                            if code[col-startAtCol] in ["[", "{", "("]:
                                token += 1
                            if code[col-startAtCol] in ["]", "}", ")"]:
                                if token == 1:
                                    if code[col-startAtCol] != "}":
                                        return {"status": 1, "message": f"ERR: This bracket is not properly closed at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                                    else:
                                        token -= 1
                                else:
                                    token -= 1
                        bracketlist.pop()
                        special = 0
                    case "]":
                        if bracketlist[-1]["bracket"] != "[":
                            return {"status": 1, "message": f"ERR: This bracket is not properly closed at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
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
                    while code[col-startAtCol] != "$":
                        dofunction += code[col-startAtCol]
                        col += 1
                    if dofunction == "runbf":
                        col += 1
                        name = code[col-startAtCol]
                        try:
                            if self.datalist[name]["type"] == "function":
                                function_result = self.runBrainfk(self.datalist[name]["value"], startAtCol=self.datalist[name]["startAtCol"])
                                if function_result["status"] == 1:
                                    return {"status": 1, "message": function_result["message"], "cursor": self.cursor, "datalistlength": len(self.datalist)}
                                else:
                                    result += function_result["result"]
                            else:
                                return {"status": 1, "message": f"ERR: Variable must be a function at col {col}", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                        except:
                            return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                    else:
                        return {"status": 1, "message": f"ERR: Unknown module at col {col}", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                    special = 0
                else:
                    #Define a single-character data constant, the next character is the data controller I means init and reset W means write R means read
                    name: str = code[col-startAtCol]
                    col += 1
                    controller: str = code[col-startAtCol]
                    if not controller.upper() in ["I", "W", "R", "L", "D", "F"]:
                        #F for function definition (not implemented yet)
                        return {"status": 1, "message": f"ERR: Invalid data controller at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                    else:
                        match controller.upper():
                            case "I":
                                self.datalist[name] = {
                                    "type": "number",
                                    "value": 0
                                }
                            case "W":
                                try:
                                    self.datalist[name]["type"] = "number"
                                    self.datalist[name]["value"] = self.memories[self.cursor]
                                except:
                                    return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                            case "R":
                                try:
                                    if self.datalist[name]["type"] == "number":
                                        self.memories[self.cursor] = self.datalist[name]["value"]
                                    elif self.datalist[name]["type"] == "linkmemory":
                                        self.memories[self.cursor] = self.memories[self.datalist[name]["value"]]
                                    elif self.datalist[name]["type"] == "function":
                                        function_result = self.execute(self.datalist[name]["value"], startAtCol=self.datalist[name]["startAtCol"])
                                        if function_result["status"] == 1:
                                            return {"status": 1, "message": function_result["message"], "cursor": self.cursor, "datalistlength": len(self.datalist)}
                                        else:
                                            result += function_result["result"]
                                except:
                                    return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                            case "L":
                                try:
                                    self.datalist[name]["type"] = "linkmemory"
                                    self.datalist[name]["value"] = self.cursor
                                except:
                                    return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                            case "D":
                                # delete data
                                try:
                                    del self.datalist[name]
                                except:
                                    return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                            case "F":
                                try:
                                    col += 1

                                    # next, we receive a character.
                                    end_char = code[col-startAtCol]
                                    function_body = ""
                                    self.datalist[name]["startAtCol"] = col+1
                                    if end_char in ["{", "[", "(", ")", "]", "}"]:
                                        return {"status": 1, "message": "Invalid EOS (End Of setence) character", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                                    else:
                                        while True:
                                            col += 1
                                            if code[col-startAtCol] == end_char:
                                                break
                                            else:
                                                function_body += code[col-startAtCol]
                                        
                                        self.datalist[name]["type"] = "function";
                                        self.datalist[name]["value"] = function_body;
                                except:
                                    return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}

                data_definition = False
                    #col += 1
            col += 1
        if (clearData):
            self.clearData()
        return {"status": 0, "result": result, "cursor": self.cursor, "datalistlength": len(self.datalist)}


def main():
    from argparse import ArgumentParser, RawTextHelpFormatter, Namespace
    
    parser = ArgumentParser(usage="trawpaw.py [options] <file>", description="Trawpaw Interpreter v" + VERSION, formatter_class=RawTextHelpFormatter)
    parser.add_argument("--usage", '-u', action="store_true", help="Show usage information and quit.")
    parser.add_argument("file", nargs="?", help="Path to the Trawpaw source code file.")
    
    args: Namespace = parser.parse_args()

    trawpaw = Trawpaw()
    
    if args.usage:
        print(DOCUMENT)
        quit()
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code: str = f.read()
            trawpaw_result = trawpaw.execute(code)
            if trawpaw_result["status"] == 1:
                print(trawpaw_result.get("message", "ERR: Unknown error occurred."))
            else:
                print(trawpaw_result.get("result", ""))
            f.close()
        quit()
    else:
        print("Run `python trawpaw.py --usage` for more information")
        print("Press Ctrl+C to exit.")
        code = input("[c:0 v:0] ")
        while True:
            try:
                trawpaw_result = trawpaw.execute(code)
                if trawpaw_result["status"] == 1:
                    print(trawpaw_result.get("message", "ERR: Unknown error occurred."))
                else:
                    print(trawpaw_result.get("result", ""))
                code = input(f"[c:{trawpaw_result['cursor']} v:{trawpaw_result['datalistlength']}] ")
            except KeyboardInterrupt:
                print("\nExiting Trawpaw REPL.")
                break

if __name__ == "__main__":
    main()
