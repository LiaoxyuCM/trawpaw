# Trawpaw

At least it is a Turing complete.

## Usage

### Python

Version: 7.0_1

#### Use our cli

Now, trawpaw supports Windows, MacOS and Linux. You can use the command line interface
to execute Trawpaw code.

Download the latest release from [our releases](https://github.com/LiaoxyuCM/trawpaw/releases)
and unzip it. Then you can use the following commands in your terminal:

```sh
##### WINDOWS, MACOS OR LINUX #####
trawpaw # To open Trawpaw REPL
trawpaw --help # For more information
trawpaw --usage # To show trawpaw usage
trawpaw --version # To show trawpaw version
trawpaw filepath # To execute this file
```

After open the REPL, you will see `[c:0 v:0]`. `c:0` means the current address
of this pointer is 0 and `v:0` means there are 0 variables defined.

#### Execute in-python-program

You need to clone this repository and install the dependencies first.

Just run the following command in your terminal:

Notice: If the previous command doesn't work, you need to check your
installation or your network, then retry.

```sh
git clone https://github.com/LiaoxyuCM/trawpaw.git
cd trawpaw
pip install --upgrade pip
pip install -r requirements.txt
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
    
    clearHistory=False, # clearHistory: default value is False
    
    startAtCol=0, # Never pass this parameter; let it be handled internally only.

    # Name of this parameter uses camel case since 6.0
    # before 6.0, it uses snake case.
    # You can pass this parameter using one of:
    # - TrawpawExecutionMethod.printManually: to print the result manually (default)
    #                                         and do `~.storeInResult` (see below)
    # - TrawpawExecutionMethod.storeInResult: to store in the result as a string
    #                                  then return it when execution is finished
    executionMethod=trawpaw.TrawpawExecutionMethod.printManually
); # Returns dict before v6.0, returns TrawpawResult since v6.0
```

##### Handle the result

Before v6.0

```py
if trawpaw_result["status"] == 1:
  print(result.get("message", "ERR: Unknown error occurred."))
else:
  print(result.get("result", ""))

```

Since v6.0

```py
if trawpaw_result.status == 1:
  print(result.message)
else:
  print(result.result)
```

`Treapaw().execute()` will returns a dictionary \(before v6.0\)
or returns a `TrawpawResult` object \(since v6.0\)
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

Before v4.5

```trawpaw
!##[[[[[[+]]]+]]].>#[[[[[[+]+]]]+]]+.[[+]+]+..[+]+.>#[[[[[+]]+]+]].[[[-]-]].<[[[+]]].[[[-]]].[+]+.[[-]-].[[[-]]].>+.#<#<#
```

Since v4.5

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
    # param avaliableDatatypes: trawpaw.TrawpawDatatypes:
    # ---- The datatypes that this module can handle.
    # ---- Note: TrawpawDatatypes is a flag, so you can
    # ----     combine multiple datatypes using bitwise OR operator (|).
    avaliableDatatypes=trawpaw.TrawpawDatatypes.String | trawpaw.TrawpawDatatypes.Number,
    # param handleResult: trawpaw.TrawpawHandleModuleResult:
    # ---- Ways to handle the result of this module.
    # ---- Default value is `TrawpawHandleModuleResult.printManually`
    handleResult=trawpaw.TrawpawHandleModuleResult.printManually
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

Notice: Before v7.0, "linkcell" is called "linkmemory".

- We will infer their data type in trawpaw
  based on the return value of your custom modules.
  \(python class =&gt; datatypes in trawpaw\)

  If failed, the executor will throw an error.

- Absolutely, we will infer the type of argument of your custom module based on
  the parameter `avaliableDatatypes` in `executor.registerCustomModule`

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

But before 7.0_1, please use `del executor.customModules["module name"]` instead.

#### Something about TrawpawFunction and TrawpawLinkCell

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

## Help

- Q: One of release assets said it's ubuntu-latest, are you sure this supports Linux?
  
  A: Absolutely. The `ubuntu-latest` means the packagements is using the latest
  version of Ubuntu, which is a Linux  distribution. So you can use the Linux version
  of Trawpaw on your Linux system without any problem.

- Q: Why don't you provide support for JavaScript anymore?
  
  A: I’ve made the difficult decision to discontinue official support for JavaScript
  to allow me to focus our development and maintenance resources on our core supported
  language \(python\). This ensures we can deliver higher-quality features, faster
  bug fixes, and more robust performance for the vast majority of our users who
  rely on these primary languages. We understand this may inconvenience some users,
  and we appreciate your understanding as we prioritize the long-term stability
  and improvement of Trawpaw.

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
