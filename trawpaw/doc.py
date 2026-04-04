VERSION: str = "8.6"

CREDITS: str = """
-------THANKS-TO--------
Waste & Waste Preview
  Made by: ChenQingMua, MoKing Studio

Brainf**k
  Author: Urban

Python
  Owned by: The Python Software Foundation

And more

-FOR-PROVIDING-SUPPORTS-

"""

DOCUMENT = r"""
REQUIREMENT:

Python 3.10+ (If execute in-python-program)

------------------------------
Code         :Type             :Usage
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
+            :                 :Increment current memory cell value by 1 (mod maxvaluepercell+1)
-            :                 :Decrement current memory cell value by 1 (mod maxvaluepercell+1)
*            :                 :Multiply current memory cell value by 2 (mod maxvaluepercell+1)
/            :                 :Divide current memory cell value by 2 (integer division, mod maxvaluepercell+1)
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

I            :VarController    :Init/reset variable and set it's type to number (used after $[name])
W            :VarController    :Set it's type to number and write current cell value to variable (used after $[name])
R            :VarController    :Read variable value to current cell (used after $[name])
L            :VarController    :Link variable to current cursor position (used after $[name])
D            :VarController    :Delete variable (used after $[name])
F            :VarController    :Define a function (used after $[name])
S            :VarController    :Define a string variable (used after $[name])
=            :VarController    :Copy b's value and datatype into a (syntax `$a=$b`) or copy debug mark's value (Storeable/St.able only)

V            :DebugMark        :Show current list of variables
C            :DebugMark&St.able:Show current address of cursor
M            :DebugMark        :Show count of cells and max value per cell.
B            :DebugMark        :Show current datalist (variables)

runbf        :Module           :Run a Brainfuck code stored in a function variable
| Syntax: `!$runbf[bf_code: variable<function>]`

runwaste
    @          :Module           :Set the cursor address to 0, run a Waste code (preview) stored in a function variable, another arg is the save of waste
    | Syntax: `!$runwaste[waste_code: variable<function>][save_in_waste_storeto: variable<number>]`

    preview    :Module           :Run a Waste code (preview) stored in a function variable, another arg is the save of waste
    | Syntax: `!$runwaste.preview[waste_code: variable<function>][save_in_waste_storeto: variable<number>]`

include      :Module           :Include and run a Trawpaw code from a file (influences current data)
| Syntax: `!$include[file_path: variable<string>]`

virtual      :Module           :Create a virtual Trawpaw object to run a Trawpaw code <typeof variable is function> or from a file <typeof variable is string> (isolated data)
| Syntax: `!$virtual[code_or_filepath: variable<string | function>]`

print        :Module           :Print a string variable
| Syntax: `!$print[value: variable<string>]`

getinput     :Module           :Get user input and store it in a string variable
| Syntax: `!$getinput[hint: variable<string>][result_storeto: variable<any>]`

tostring     :Module           :Convert variable to string
| Syntax: `!$print[value: variable<function|number>]`

tofunction   :Module           :Convert variable to function
| Syntax: `!$print[value: variable<string>]`

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

    offset
        forward     :Module       :The ASCII of each character will be subtracted by 1, store the result in a string variable (e.g. "bcd" -> "abc")
        | Syntax: `!$string.offset.forward[original_str: variable<string>]`

        backward    :Module       :The ASCII of each character will be added by 1, store the result in a string variable (e.g. "abc" -> "bcd")
        | Syntax: `!$string.offset.backward[original_str: variable<string>]`

number
    plusby     :Module           :Calculate (value of) the current cell plus this variable, store result to the current cell
    | Syntax: `!$number.plusby[plus_whom: variable<number>]


    subtractby :Module           :Calculate (value of) the current cell subtract this variable, store result to the current cell
    | Syntax: `!$number.subtractby[subtract_whom: variable<number>]


    timesby    :Module           :Calculate (value of) the current cell times this variable, store result to the current cell
    | Syntax: `!$number.timesby[times_whom: variable<number>]


    divideby   :Module           :Calculate (value of) the current cell divide this variable (floor result), store result to the current cell
    | Syntax: `!$number.divideby[divide_whom: variable<number>]


    powerby    :Module           :Calculate (value of) the current cell power this variable, store result to the current cell
    | Syntax: `!$number.powerby[power_whom: variable<number>]

hash
    md5        :Module           :MD5-hash a string variable
    | Syntax: `!$hash.md5[original_str: variable<string>]`

    sha1       :Module           :SHA1-hash a string variable
    | Syntax: `!$hash.sha1[original_str: variable<string>]`

    sha224     :Module           :SHA224-hash a string variable
    | Syntax: `!$hash.sha224[original_str: variable<string>]`

    sha256     :Module           :SHA256-hash a string variable
    | Syntax: `!$hash.sha256[original_str: variable<string>]`

    sha384     :Module           :SHA384-hash a string variable
    | Syntax: `!$hash.sha384[original_str: variable<string>]`

    sha512     :Module           :SHA512-hash a string variable
    | Syntax: `!$hash.sha512[original_str: variable<string>]`

base64
    encode     :Module           :Base64-encode a string variable
    | Syntax: `!$base64.encode[original_str: variable<string>]`

    decode     :Module           :Base64-decode a string variable
    | Syntax: `!$base64.decode[original_str: variable<string>]`

------------------------------
ADDITIONAL NOTES:
1. Bracket commands ([ ( {) must be properly closed with ] ) } respectively
2. Variable definition syntax: "$[one-length char name][variable controller]"
3. Function syntax & String syntax: "$[x]["f"|"s"][y][body][y]" x: variable name, y: EOS (End of setence) Character (One length), body: function body
4. Debug syntax: "@[debug mark]"
5. clearData=True in execute() resets cells and datalist to initial state
6. Variable in module calling must syntaxed "$[name]" (no controller)
7. In string definition, "\" is an escape char since 7.2,
    \e        :End-char (Note: if you type an end-char manually, trawpaw will think the content of string is end)
    \t        :Tab
    \n        :New line
    \r        :Enter
    \\        :Backslash
"""
