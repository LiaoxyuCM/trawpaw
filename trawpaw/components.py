import enum
from typing import Callable
import urllib.parse
import hashlib
import base64


class TrawpawExecutionMethod(enum.Enum):
    printManually = 0
    storeInResult = 1
    storeInResultExpression = 2


class TrawpawHandleModuleResult(enum.Enum):
    assignToVar = 0
    storeToCurrCell = 1
    printManually = 2


class TrawpawDatatypes(enum.Flag):
    Number = enum.auto()
    LinkCell = enum.auto()
    String = enum.auto()
    Function = enum.auto()


class TrawpawResult:
    def __init__(self, result: dict) -> None:
        self.status: int = result.get("status", -1)
        if self.status == 1:
            self.message: str = result.get("message", "Unknown error occurred")
        else:
            self.result: str = result.get("result", "")
        self.cursor: int = result.get("cursor", -1)
        self.datalistlength: int = result.get("datalistlength", -1)

    def __str__(self) -> str:
        return f"TrawpawResult(status={self.status}, ...)"


class TrawpawFunction:
    def __init__(self, body: str) -> None:
        self.value = body

    def __str__(self) -> str:
        return self.value

    relates_to = TrawpawDatatypes.Function


class TrawpawLinkCell:
    def __init__(self, cellIndex: int) -> None:
        self.value = cellIndex

    def __str__(self) -> str:
        return str(self.value)

    relates_to = TrawpawDatatypes.LinkCell


methods: dict[str, dict[str, Callable]] = {
    "urlparse": {
        "string.encodeuri": urllib.parse.quote,
        "string.decodeuri": urllib.parse.unquote,
    },
    "hash": {
        "hash.md5": hashlib.md5,
        "hash.sha1": hashlib.sha1,
        "hash.sha224": hashlib.sha224,
        "hash.sha256": hashlib.sha256,
        "hash.sha384": hashlib.sha384,
        "hash.sha512": hashlib.sha512,
    },
    "base64": {
        "base64.encode": base64.b64encode,
        "base64.decode": base64.b64decode,
    },
}

methodsInt: dict[str, dict[str, int]] = {
    "offset": {
        "string.offset.forward": 1,
        "string.offset.backward": -1,
    }
}

# Module string.[un]escape
htmlEscape = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "©": "&copy;",
    "®": "&reg;",
    '"': "&quot;",
    " ": "&nbsp;",
    "\n": "<br>",
}

# aliases

Tem = TrawpawExecutionMethod
Thmr = TrawpawHandleModuleResult
Tdt = TrawpawDatatypes
Trst = TrawpawResult
Tfun = TrawpawFunction
Tlc = TrawpawLinkCell
