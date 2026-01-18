# Trawpaw
At least it is a turing complete.

[Try Trawpaw online](https://tools.liaoxyucm.xyz/trawpaw)

## How to use trawpaw?

### Python

#### Use our cli

To use Trawpaw in Python, we require the version of interpreter at least 3.10
```sh
python trawpaw.py # To open Trawpaw REPL
python trawpaw.py --usage # To show trawpaw usage
python trawpaw.py filepath # To execute this file
```
After open the REPL, you will see `[c:0 v:0]`. `c:0` means the current address of this pointer is 0 and `v:0` means there are 0 variables defined.

#### Execute in-python-program

```py
import trawpaw;
executor = trawpaw.Trawpaw();
result = executor.execute("Your trawpaw source code", "Input when this project requires input (optional)", clearHistory=False); # clearHistory: default value is False
if trawpaw_result["status"] == 1:
  print(result.get("message", "ERR: Unknown error occurred."))
else:
  print(result.get("result", ""))

```

### JavaScript (Front-end)
```js
import { Trawpaw } from "./trawpaw.js";
document.addEventListener("DOMContentLoaded", async() => {
  const trawpaw = new Trawpaw();
  // To execute trawpaw code, async-await is required.
  let result = await trawpaw.execute("Your trawpaw source code", "Input when this project requires input (optional)", clearHistory=false /* or true */);
  if (result["status"] === 1) {
    console.error(result["message"]);
  } else {
    console.log(result["result"]);
  };
});
```

## Hello World in Trawpaw

```trawpaw
!##[[[[[[+]]]+]]].>#[[[[[[+]+]]]+]]+.[[+]+]+..[+]+.>#[[[[[+]]+]+]].[[[-]-]].<[[[+]]].[[[-]]].[+]+.[[-]-].[[[-]]].>+.#<#<#
```

## Trawpaw Usage

| Code | Type          | Usage                                                                 |
|------|---------------|-----------------------------------------------------------------------|
| +    |               | Increment current memory cell value by 1 (mod maxvaluepermem+1)       |
| -    |               | Decrement current memory cell value by 1 (mod maxvaluepermem+1)       |
| *    |               | Multiply current memory cell value by 2 (mod maxvaluepermem+1)        |
| /    |               | Divide current memory cell value by 2 (integer division, mod maxvaluepermem+1) |
| #    |               | Set current memory cell value to 0 (normal) or move cursor to memory 0 (! modifier) |
| <    |               | Move cursor left by 1 (circular)                                      |
| >    |               | Move cursor right by 1 (circular)                                     |
| ,    |               | Read a character input, store its ASCII code in current cell          |
| .    |               | Output cell as ASCII char (normal) or number (! modifier)             |
| $    |               | Enter data definition mode (followed by \[name\]\[controller\])       |
| _    |               | Pause execution for 1s (normal) or 0.1s (! modifier)                  |
| &    |               | Breakpoint for debugging (waits for user input to continue) (normal) Quit program and return result (! modifier) |
| !    | Special       | Modify next command's behavior (special mode)                         |
| \[pattern\] | Bracket       | Loop twice (normal) 50% chance skip all inside (! modifier)          |
| (pattern) |  Bracket       | Normal: skip if cell=0; !: skip if cell≠0                             |
| {pattern} |  Bracket       | Comment                                                               |
| I    | VarController | Init/reset variable (used after $\[name\])                              |
| W    | VarController | Write current cell value to variable (used after $\[name\])             |
| R    | VarController | Read variable value to current cell (used after $\[name\])              |
| L    | VarController | Link variable to current cursor position (used after $\[name\])         |
| D    | VarController | Delete variable (used after $\[name\])                                  |

### Additional Notes

1. Bracket commands `[ ( {` must be properly closed with \] \) \} respectively
2. Variablr definition syntax: $\[single char name\]\[variable controller\]

## Thanks

- [Waste](https://github.com/ChenQingMua/WasteLanguage)
- Brainfuck
