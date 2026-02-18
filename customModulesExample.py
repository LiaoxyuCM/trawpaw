from trawpaw import (
    Trawpaw,
    TrawpawDatatypes,
    TrawpawHandleModuleResult,
)
import urllib.parse
import base64
import hashlib

executor = Trawpaw()

### PRINT ###


@executor.registerCustomModule(
    name="print",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.printManually,
)
def handle_print(arg: str):
    return arg


### STRING.ADDTO ###


@executor.registerCustomModule(
    name="string.addto",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_addto(arg: str):
    return arg + chr(executor.cells[executor.cursor])


### STRING.INSERTTOFIRST ###


@executor.registerCustomModule(
    name="string.inserttofirst",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_inserttofirst(arg: str):
    return chr(executor.cells[executor.cursor]) + arg


### STRING.LENGTH ###


@executor.registerCustomModule(
    name="string.length",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.storeToCurrCell,
)
def handle_string_length(arg: str):
    return len(arg)


### STRING.REVERSE ###


@executor.registerCustomModule(
    name="string.reverse",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_reverse(arg: str):
    return arg[::-1]


### STRING.TOUPPER ###


@executor.registerCustomModule(
    name="string.toupper",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_toupper(arg: str):
    return arg.upper()


### STRING.TOLOWER ###


@executor.registerCustomModule(
    name="string.tolower",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_tolower(arg: str):
    return arg.lower()


### STRING.ENCODEURI ###


@executor.registerCustomModule(
    name="string.encodeuri",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_encodeuri(arg: str):
    return urllib.parse.quote(arg)


### STRING.DECODEURI ###


@executor.registerCustomModule(
    name="string.decodeuri",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_decodeuri(arg: str):
    return urllib.parse.unquote(arg)


##### STRING.ESCAPE AND STRING.UNESCAPE #####

escape = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "©": "&copy;",
    "®": "&reg;",
    '"': "&quot;",
    " ": "&nbsp;",
    "\n": "<br>",
}

### STRING.ESCAPE ###


@executor.registerCustomModule(
    name="string.escape",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_escape(arg: str):
    for char, esc in escape.items():
        arg = arg.replace(char, esc)
    return arg


### STRING.UNESCAPE ###


@executor.registerCustomModule(
    name="string.unescape",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_unescape(arg: str):
    for char, esc in list(escape.items())[::-1]:
        arg = arg.replace(esc, char)
    return arg


### HASH.MD5 ###


@executor.registerCustomModule(
    name="hash.md5",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_hash_md5(arg: str):
    return hashlib.md5(arg.encode()).hexdigest()


### HASH.SHA1 ###


@executor.registerCustomModule(
    name="hash.sha1",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_hash_sha1(arg: str):
    return hashlib.sha1(arg.encode()).hexdigest()


### HASH.SHA224 ###


@executor.registerCustomModule(
    name="hash.sha224",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_hash_sha224(arg: str):
    return hashlib.sha224(arg.encode()).hexdigest()


### HASH.SHA256 ###


@executor.registerCustomModule(
    name="hash.sha256",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_hash_sha256(arg: str):
    return hashlib.sha256(arg.encode()).hexdigest()


### HASH.SHA384 ###


@executor.registerCustomModule(
    name="hash.sha384",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_hash_sha384(arg: str):
    return hashlib.sha384(arg.encode()).hexdigest()


### HASH.SHA512 ###


@executor.registerCustomModule(
    name="hash.sha512",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_hash_sha512(arg: str):
    return hashlib.sha512(arg.encode()).hexdigest()


### BASE64.ENCODE ###


@executor.registerCustomModule(
    name="base64.encode",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_base64_encode(arg: str):
    return base64.b64encode(arg.encode()).decode()


### BASE64.DECODE ###


@executor.registerCustomModule(
    name="base64.decode",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_base64_decode(arg: str):
    return base64.b64decode(arg.encode()).decode()


### STRING.OFFSET.FORWARD ###


@executor.registerCustomModule(
    name="string.offset.forward",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_offset_forward(arg: str):
    new_string = ""
    for char in arg:
        new_string += chr(ord(char) - 1)
    return new_string


### STRING.OFFSET.BACKWARD ###


@executor.registerCustomModule(
    name="string.offset.backward",
    avaliableDatatypes=TrawpawDatatypes.String,
    handleResult=TrawpawHandleModuleResult.assignToVar,
)
def handle_string_offset_backward(arg: str):
    new_string = ""
    for char in arg:
        new_string += chr(ord(char) + 1)
    return new_string


### NUMBER.PLUSBY ###


@executor.registerCustomModule(
    name="number.plusby",
    avaliableDatatypes=TrawpawDatatypes.Number,
    handleResult=TrawpawHandleModuleResult.storeToCurrCell,
)
def handle_number_plusby(arg: int):
    return executor.cells[executor.cursor] + arg


### NUMBER.SUBTRACTBY ###


@executor.registerCustomModule(
    name="number.subtractby",
    avaliableDatatypes=TrawpawDatatypes.Number,
    handleResult=TrawpawHandleModuleResult.storeToCurrCell,
)
def handle_number_subtractby(arg: int):
    return executor.cells[executor.cursor] - arg


### NUMBER.TIMESBY ###


@executor.registerCustomModule(
    name="number.timesby",
    avaliableDatatypes=TrawpawDatatypes.Number,
    handleResult=TrawpawHandleModuleResult.storeToCurrCell,
)
def handle_number_timesby(arg: int):
    return executor.cells[executor.cursor] * arg


### NUMBER.PLUSBY ###


@executor.registerCustomModule(
    name="number.divideby",
    avaliableDatatypes=TrawpawDatatypes.Number,
    handleResult=TrawpawHandleModuleResult.storeToCurrCell,
)
def handle_number_divideby(arg: int):
    return executor.cells[executor.cursor] // arg


### NUMBER.PLUSBY ###


@executor.registerCustomModule(
    name="number.powerby",
    avaliableDatatypes=TrawpawDatatypes.Number,
    handleResult=TrawpawHandleModuleResult.storeToCurrCell,
)
def handle_number_powerby(arg: int):
    return executor.cells[executor.cursor] ** arg
