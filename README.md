# Trawpaw

We wish it is humane.

At least it is a turing complete.

## Usage

### Python

Version: 5.6

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
executor = trawpaw.Trawpaw();
result = executor.execute(
    "Your trawpaw source code",
    "Input when this project requires input (optional)",
    clearHistory=False # clearHistory: default value is False
);
if trawpaw_result["status"] == 1:
  print(result.get("message", "ERR: Unknown error occurred."))
else:
  print(result.get("result", ""))

```

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

v4.5 \(or later\)

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
<major>.<minor_l1>[.<minor_l2>[.<minor_l3>[...]]][_<patch>]
```

### Prerelease & Release Candidate

```versionrule
<major>.0-(pre|rc)<minor>
```

## Thanks

- [Waste-Preview](https://github.com/ChenQingMua/WasteLanguage-Preview)
- Brainf\*\*k
