# Trawpaw

We wish it is humane.

At least it is a Turing complete.

## Usage

### Python

Version: 6.0_1-waste1.0.1

#### Use our cli

Now supports Windows, MacOS and Linux. You can use the command line interface
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
    executionMethod=TrawpawExecutionMethod.printManually


); # Returns dict before v6.0, returns TrawpawResult since v6.0
```

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
<major>.<minor_l1>[.<minor_l2>[.<minor_l3>[...]]][_<patch>]-waste<tag>
```

### Prerelease & Release Candidate

```versionrule
<major>.0-(pre|rc)<minor>-waste<tag>
```

## Thanks

- [Waste-Preview](https://github.com/ChenQingMua/WasteLanguage-Preview)
- Brainf\*\*k
