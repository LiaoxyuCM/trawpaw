# Trawpaw

Note: **Some paragraphs translated by AI. Check for mistakes.**

At least it is a Turing complete.

## Usage

### Python

Version: 8.7

#### Use our cli

Now, trawpaw supports Windows, MacOS and Linux. You can use the command line interface
to execute Trawpaw code.

Download the latest release from [our releases](https://github.com/LiaoxyuCM/trawpaw/releases)
and unzip it. Then you can use the following commands in your terminal:

Note: **Do not unzip it to the current directory,
Please create a new folder first!!!**

```sh
##### WINDOWS, MACOS OR LINUX #####
trawpaw # To open Trawpaw REPL
trawpaw --help # For more information
trawpaw --usage # To show trawpaw usage
trawpaw --version # To show trawpaw version
trawpaw --trawpawl OUT_FILE FILE_TO_LISTEN # to call trawpawl
trawpaw filepath # To execute this file
```

After open the REPL, you will see `[c:0 v:0]`. `c:0` means the current address
of this pointer is 0 and `v:0` means there are 0 variables defined.

This REPL will generate file `.tphistories` since v7.2,
if you want to clear your REPL history \(since v7.2\), just delete the file

If you do not want to generate that file, just use `--nohistory`.

**DEPRECATED**: `--nohistories` is deprecated since v8.6.2

#### Execute in-python-program

Notice since 8.0 **Except for `Trawpaw`, other classes moved to `trawpaw.components`.
Also, `__doc__` moved to `trawpaw.doc.DOCUMENT`, `VERSION` moved to `trawpaw.doc.VERSION`**

You need to clone this repository ,
set up venv \(optional but recommended\)
and install the dependencies first.

Just run the following command in your terminal:

Notice: If the previous command doesn't work, you need to check your
installation or your network, then retry.

```sh
## Clone repo
git clone https://github.com/LiaoxyuCM/trawpaw.git
cd trawpaw
## Set up virtual env
python -m venv pyenv # Or custom name of virtual env
pyenv/Scripts/activate
## Install dependencies
pip install --upgrade pip
pip install -r requirements/base.txt
```

Then you can import the `trawpaw` module in your Python code
and use the `Trawpaw` class to execute Trawpaw code.

It requires Python Interpreter v3.10 or higher.

```py
import trawpaw;
executor = trawpaw.Trawpaw(
    # The length of cells, default: 128 (0 < cells <= 65536)
    # it called "memories" before 6.0
    cells=128,
    # The max value per cell, default: 127 (0 < maxvaluepercell <= 65536)
    # it called "maxvaluepermem" before 6.0
    maxvaluepercell=127,
);
result = executor.execute(
    "Your trawpaw source code",
    "Input when this project requires input (optional)",
    
    clearData=False, # clearData: default value is False
    
    startAtCol=0, # Never pass this parameter; let it be handled internally only.

    # You can pass this parameter using one of:
    # - TrawpawExecutionMethod.printManually: to print the result manually (default)
    # - TrawpawExecutionMethod.storeInResult: to store in the result as a string
    #                                  then return it when execution finished
    # - TrawpawExecutionMethod.storeInResultExpression: to store as a result expression
    #                                  then return it when execution finished
    executionMethod=trawpaw.components.Tem.printManually,

    # Quick mode (default value is False)
    # If enabled, Trawpaw won't support
    # - Waiting
    # - Getting input
    quickMode=False,

    # Silent mode (default value is False)
    # If enabled, Trawpaw will ignore all warnings
    silentMode=False
);
```

##### Handle the result

```py
if trawpaw_result.status == 1:
  print(result.message)
else:
  print(result.result)
```

`Treapaw().execute()` will returns a `TrawpawResult` object \(since v6.0\)
with the following keys

- status

| status | meaning   |
| ------ | --------- |
| 0      | OK        |
| 1      | Error     |
| 2      | Interrupt |

- message: If status is 1, this key will contain the error message.
  Else, it's not exist.

- result: If status is 0 or 2, this key will contain the output
  of the Trawpaw code. Else, it's not exist.

- cursor: The current address of the pointer after executing the code.
  \(Not recommended, only for REPL\)

- datalistlength: The length of the datalist after executing the code.
  \(Not recommended, only for REPL\)

### JavaScript (Front-end)

Notice: **We no longer provide support for Trawpaw JavaScript.
Please use Trawpaw Python**

Version: 1.1.1

```js
import { Trawpaw } from "./trawpaw.js";
document.addEventListener("DOMContentLoaded", () => {
  const trawpaw = new Trawpaw();
  let result = trawpaw.execute(
    "Your trawpaw source code",
    "Input when this project requires input (optional)",
    clearHistory=false /* or true */
  );
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

or simplifier

```trawpaw
!!#$ai$as"Hello, world!"!$print$a
```

## Advanced Tutor

### Register your custom module

Your Trawpaw executor has a method to register your custom module.
Here is an example of how to register a custom module:

```py
@trawpaw_executor.registerCustomModule(
    # param name: str: The name of this module.
    # ---- Note: DO NOT contain "$" in the name.
    name="module name",
    # param availableDatatypes: trawpaw.TrawpawDatatypes:
    # ---- The datatypes that this module can handle.
    # ---- Note: TrawpawDatatypes is a flag, so you can
    # ----     combine multiple datatypes using bitwise OR operator (|).
    availableDatatypes=trawpaw.components.Tdt.String | trawpaw.components.Tdt.Number,
    # param handleResult: trawpaw.components.TrawpawHandleModuleResult:
    # ---- Ways to handle the result of this module.
    # ---- Default value is `TrawpawHandleModuleResult.printManually`
    handleResult=trawpaw.components.Thmr.printManually
)
def foo(arg: str | int) -> str: # Your module should receive (only) one argument
    return f"Your input is {arg}"
```

If the newly registered module has the same name as an existing module,
the newly module will override the existing module.

Please read `customModulesExample.py` for examples.

#### Datatypes table

| datatypes in trawpaw |  python class    | enum (flag) TrawpawDatatypes |
| -------------------- | ---------------- | ---------------------------- |
| "string"             | str              | TrawpawDatatypes.String      |
| "number"             | int              | TrawpawDatatypes.Number      |
| "function"           | TrawpawFunction  | TrawpawDatatypes.Function    |
| "linkcell"           | TrawpawLinkCell  | TrawpawDatatypes.LinkCell    |

- We will infer their data type in trawpaw
  based on the return value of your custom modules.
  \(python class =&gt; datatypes in trawpaw\)

  If failed, the executor will throw an error.

- Absolutely, we will infer the type of argument of your custom module based on
  the parameter `availableDatatypes` in `executor.registerCustomModule`

  \(TrawpawDatatypes =&gt; python class\)

  If failed, same, the executor will throw an error.

#### Handle the result of your custom module

Use `TrawpawHandleModuleResult` to handle the result of your custom module.

| Option          | Meaning                                                    |
| --------------- | ---------------------------------------------------------- |
| assignToVar     | Store the result in the argument of your module            |
| storeToCurrCell | Store the result in the current cell of Trawpaw (int only) |
| printManually   | Print the result manually (default)(str \| int only)       |

#### Unregister your custom module

```py
executor.unregisterCustomModule("module name")
```

Yes, the `unregisterCustomModule` is not a decorator.

#### TrawpawFunction and TrawpawLinkCell

Encapsulation (object definition)

```py
TrawpawFunction(function_content: str)
TrawpawLinkCell(cell_address: int)
```

Get content

```py
trawpaw_function.value # trawpaw_function is instance of TrawpawFunction
trawpaw_link_cell.value # trawpaw_link_cell is instance of TrawpawLinkCell
```

### Processing Result Expressions

Due to space limitations, we will not cover the syntax of result expressions,
only the processing methods.

```py
from trawpaw import Trawpaw
from trawpaw.components import Tem

executor = Trawpaw()

res = executor.execute(
    "your code",
    executionMethod=Tem.storeInResultExpression,
)
```

At this point, `res.output` is a result expression.
You can use the functions in `trawpaw.tools` to process them.

```py
from trawpaw.tools import \
    simplifyResultExpression, executeResultExpression, \
    compileResultExpression

# This function used to simplify the result expression
# resultExpression: the result expression
simplifyResultExpression(resultExpression: str) -> str

# This function used to execute the result expression
# resultExpression: the result expression
executeResultExpression(resultExpression: str) -> None

# This function used to convert the result expression to another language
# resultExpr: the result expression
# targetLang: target language, can be python or frontend JavaScript
# javascriptElemName: variable name to use when targetLang is 'javascript'
compileResultExpression(
    resultExpr: str,
    targetLang: Literal["python"] | Literal["javascript"] = "python",
    javascriptElemName: str = "default",
) -> str
```

### Trawpawl

The syntax is as follows:

```tpwl
<|namespace code|>
```

`namespace`: Namespace. If it does not exist,
a new object will be created with this namespace;
otherwise, the object corresponding to this namespace will be used.
To put it simply, to retrieve data from the last executed code
(such as getting a cursor address),
the namespace must be exactly the same as the previous one.

`code`: Needless to say, fill in the source code to be executed here.

#### Example

```tpwl
<p>
    First output
    <|first
        ++++!.
    |>
    
    Second output
    <|second
        [+++]**!.
    |>

    Third output, using data from the first segment of code
    <|first
        ++++!. {Will output 8 instead of 4}
    |>
</p>
```

### Aliases

```txt
Tem = TrawpawExecutionMethod
Thmr = TrawpawHandleModuleResult
Tdt = TrawpawDatatypes
Trst = TrawpawResult
Tfun = TrawpawFunction
Tlc = TrawpawLinkCell
```

## Version rule

### Standard

```versionrule
<major>.<minor_l1>[.<minor_l2>[.<minor_l3>[...]]][_<patch>][-waste<tag>]
```

### Prerelease & Release Candidate

```versionrule
<major>.0-(pre|rc)<minor>[_<patch>][-waste<tag>]
```

## Thanks

- [Waste-Preview](https://github.com/ChenQingMua/WasteLanguage-Preview)
- Brainf\*\*k
