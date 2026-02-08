# Trawpaw

Now supports EXE!!!

At least it is a turing complete.

## Usage

### Python

Version: 4.5

#### Use our cli

Now supports Windows, MacOS and Linux. You can use the command line interface to execute Trawpaw code.

Download the latest release from [our releases](https://github.com/LiaoxyuCM/trawpaw/releases) and unzip it. Then you can use the following commands in your terminal:

```sh
##### WINDOWS, MACOS OR LINUX #####
trawpaw # To open Trawpaw REPL
trawpaw --usage # To show trawpaw usage
trawpaw filepath # To execute this file
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

**We no longer provide support for Trawpaw JavaScript. Please use Trawpaw Python**

Version: 1.1.1

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

## Thanks

- [Waste](https://github.com/ChenQingMua/WasteLanguage-Preview)
- Brainf\*\*k
