# trawpaw
At least it is an turing complete.

[Try Trawpaw online](https://tools.liaoxyucm.xyz/trawpaw)

## Requirements

- Python 3.10+

## How to use trawpaw.py?

```sh
python trawpaw.py # To open Trawpaw REPL
python trawpaw.py --help # To show trawpaw usage
python trawpaw.py filepath # To execute this file
```
After open the REPL, you will see `[c:0 v:0]`. `c:0` means the current address of this pointer is 0 and `v:0` means there are 0 variables defined.

## Hello World in Trawpaw

```trawpaw
!##[[[[[[+]]]+]]].>#[[[[[[+]+]]]+]]+.[[+]+]+..[+]+.>#[[[[[+]]+]+]].[[[-]-]].<[[[+]]].[[[-]]].[+]+.[[-]-].[[[-]]].>+.#<#<#
```

## Trawpaw Usage

| Code | Source               | Type          | Usage                                                                 |
|------|----------------------|---------------|-----------------------------------------------------------------------|
| +    | Brainfk,Waste        |               | Increment current memory cell value by 1 (mod maxvaluepermem+1)       |
| -    | Brainfk,Waste        |               | Decrement current memory cell value by 1 (mod maxvaluepermem+1)       |
| *    | Waste                |               | Multiply current memory cell value by 2 (mod maxvaluepermem+1)        |
| /    | Waste                |               | Divide current memory cell value by 2 (integer division, mod maxvaluepermem+1) |
| #    | Waste (Modded)       |               | Set current memory cell value to 0 (normal) or move cursor to memory 0 (! modifier) |
| <    | Brainfk              |               | Move cursor left by 1 (circular)                                      |
| >    | Brainfk              |               | Move cursor right by 1 (circular)                                     |
| ,    | Brainfk              |               | Read a character input, store its ASCII code in current cell          |
| .    | Brainfk (Modded)     |               | Output cell as ASCII char (normal) or number (! modifier)             |
| $    | N/A                  |               | Enter data definition mode (followed by \[name\]\[controller\])           |
| _    | Waste (Modded)       |               | Pause execution for 1s (normal) or 0.1s (! modifier)                  |
| &    | N/A                  |               | Breakpoint for debugging (waits for user input to continue) (normal) Quit program and return result (! modifier) |
| !    | N/A                  | Special       | Modify next command's behavior (special mode)                         |
| \[pattern\] | Waste (Modded)     | Bracket       | Loop twice (normal) 50% chance skip all inside (! modifier)          |
| (pattern) | Brainfk (Modded)   | Bracket       | Normal: skip if cell=0; !: skip if cell≠0                             |
| {pattern} | Waste              | Bracket       | Comment                                                               |
| I    | N/A                  | VarController | Init/reset variable (used after $\[name\])                              |
| W    | N/A                  | VarController | Write current cell value to variable (used after $\[name\])             |
| R    | N/A                  | VarController | Read variable value to current cell (used after $\[name\])              |
| L    | N/A                  | VarController | Link variable to current cursor position (used after $\[name\])         |
| D    | N/A                  | VarController | Delete variable (used after $\[name\])                                  |

### Additional Notes

1. Bracket commands `[ ( {` must be properly closed with \] \) \} respectively
2. Variablr definition syntax: $\[single char name\]\[variable controller\]

## Thanks

- (Waste)[https://github.com/ChenQingMua/WasteLanguage]
- Brainfuck
