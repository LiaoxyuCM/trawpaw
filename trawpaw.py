VERSION: str = "1.1"
DOCUMENT: str = """
REQUIREMENTS:

Python 3.10+

------------------------------
Code         :Source                :Type             :Usage
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
+            :Brainfk,Waste         :                 :Increment current memory cell value by 1 (mod maxvaluepermem+1)
-            :Brainfk,Waste         :                 :Decrement current memory cell value by 1 (mod maxvaluepermem+1)
*            :Waste                 :                 :Multiply current memory cell value by 2 (mod maxvaluepermem+1)
/            :Waste                 :                 :Divide current memory cell value by 2 (integer division, mod maxvaluepermem+1)
#            :Waste (Modded)        :                 :Set current memory cell value to 0 (normal) or move cursor to memory 0 (! modifier)
<            :Brainfk               :                 :Move cursor left by 1 (circular)
>            :Brainfk               :                 :Move cursor right by 1 (circular)
,            :Brainfk               :                 :Read a character input, store its ASCII code in current cell
.            :Brainfk (Modded)      :                 :Output cell as ASCII char (normal) or number (! modifier)
$            :N/A                   :                 :Enter data definition mode (followed by [name][controller])
_            :Waste (Modded)        :                 :Pause execution for 1s (normal) or 0.1s (! modifier)
&            :N/A                   :                 :Breakpoint for debugging (waits for user input to continue) (normal) Quit program and return result (! modifier)
!            :N/A                   :Special          :Modify next command's behavior (special mode)
[pattern]    :Waste (Modded)        :Bracket          :Loop twice (normal) 50% chance skip all inside (! modifier)
(pattern)    :Brainfk (Modded)      :Bracket          :Normal: skip if cell=0; !: skip if cell≠0
{pattern}    :Waste                 :Bracket          :Comment
I            :N/A                   :VarController    :Init/reset variable (used after $[name])
W            :N/A                   :VarController    :Write current cell value to variable (used after $[name])
R            :N/A                   :VarController    :Read variable value to current cell (used after $[name])
L            :N/A                   :VarController    :Link variable to current cursor position (used after $[name])
D            :N/A                   :VarController    :Delete variable (used after $[name])
------------------------------
ADDITIONAL NOTES:
1. Bracket commands ([ ( {) must be properly closed with ] ) } respectively
2. Variablr definition syntax: $[single char name][variable controller]
3. clearHistory=True in execute() resets memories and datalist to initial state
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

    def clearHistory(self):
        self.memories = self.nullmem.copy()
        self.datalist = {}
        self.cursor = 0


    def execute(self, code: str, getinput: str = "", clearHistory: bool = False) -> dict:
        inputcur: int = 0
        bracketlist: list[dict] = []
        result: str = ""
        col:int = 0
        data_definition: bool = False
        special: Literal[0 | 1 | 2] = 0
        while col < len(code):
            if special == 1:
                special = 2
            elif special == 2:
                special = 0
            
            if not data_definition:
                match code[col]:
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
                        if special:
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
                        special = 0
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
                        special = 1
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
                                    if code[col] in ["[", "{", "("]:
                                        token += 1
                                    if code[col] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col] != "]":
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
                                    if code[col] in ["[", "{", "("]:
                                        token += 1
                                    if code[col] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col] != ")":
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
                                    if code[col] in ["[", "{", "("]:
                                        token += 1
                                    if code[col] in ["]", "}", ")"]:
                                        if token == 1:
                                            if code[col] != ")":
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
                            if code[col] in ["[", "{", "("]:
                                token += 1
                            if code[col] in ["]", "}", ")"]:
                                if token == 1:
                                    if code[col] != "}":
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
            elif data_definition:
                #Define a single-character data constant, the next character is the data controller I means init and reset W means write R means read
                name: str = code[col]
                col += 1
                controller: str = code[col]
                if not controller.upper() in ["I", "W", "R", "L", "D"]:
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
                            except:
                                return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                        case "L":
                            self.datalist[name]["type"] = "linkmemory"
                            self.datalist[name]["value"] = self.cursor
                        case "D":
                            # delete data
                            try:
                                del self.datalist[name]
                            except:
                                return {"status": 1, "message": f"ERR: Data '{name}' is not initialized at col {col}.", "cursor": self.cursor, "datalistlength": len(self.datalist)}
                data_definition = False
                #col += 1
                
            col += 1
        if (clearHistory):
            self.clearHistory()
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
