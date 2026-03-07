from trawpaw import (
    Tfun,
    Trawpaw,
    Tdt,
    Thmr,
)
import urllib.parse
import base64
import hashlib

executor = Trawpaw()

### PRINT ###


@executor.registerCustomModule(
    name="print",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.printManually,
)
def handle_print(arg: str):
    return arg


### STRING.ADDTO ###


@executor.registerCustomModule(
    name="string.addto",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_addto(arg: str):
    return arg + chr(executor.cells[executor.cursor])


### STRING.INSERTTOFIRST ###


@executor.registerCustomModule(
    name="string.inserttofirst",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_inserttofirst(arg: str):
    return chr(executor.cells[executor.cursor]) + arg


### STRING.LENGTH ###


@executor.registerCustomModule(
    name="string.length",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.storeToCurrCell,
)
def handle_string_length(arg: str):
    return len(arg)


### STRING.REVERSE ###


@executor.registerCustomModule(
    name="string.reverse",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_reverse(arg: str):
    return arg[::-1]


### STRING.TOUPPER ###


@executor.registerCustomModule(
    name="string.toupper",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_toupper(arg: str):
    return arg.upper()


### STRING.TOLOWER ###


@executor.registerCustomModule(
    name="string.tolower",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_tolower(arg: str):
    return arg.lower()


### STRING.ENCODEURI ###


@executor.registerCustomModule(
    name="string.encodeuri",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_encodeuri(arg: str):
    return urllib.parse.quote(arg)


### STRING.DECODEURI ###


@executor.registerCustomModule(
    name="string.decodeuri",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
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
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_escape(arg: str):
    for char, esc in escape.items():
        arg = arg.replace(char, esc)
    return arg


### STRING.UNESCAPE ###


@executor.registerCustomModule(
    name="string.unescape",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_unescape(arg: str):
    for char, esc in list(escape.items())[::-1]:
        arg = arg.replace(esc, char)
    return arg


### TOSTRING ###


@executor.registerCustomModule(
    name="tostring",
    availableDatatypes=Tdt.Number | Tdt.Function,
    handleResult=Thmr.assignToVar,
)
def handle_tostring(arg: int | Tfun):
    if isinstance(arg, int):
        return str(arg)
    elif isinstance(arg, Tfun):
        return str(arg.value)


### TOFUNCTION ###


@executor.registerCustomModule(
    name="tofunction", availableDatatypes=Tdt.String, handleResult=Thmr.assignToVar
)
def handle_tofunction(arg: str):
    return Tfun(arg)


### HASH.MD5 ###


@executor.registerCustomModule(
    name="hash.md5",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_hash_md5(arg: str):
    return hashlib.md5(arg.encode()).hexdigest()


### HASH.SHA1 ###


@executor.registerCustomModule(
    name="hash.sha1",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_hash_sha1(arg: str):
    return hashlib.sha1(arg.encode()).hexdigest()


### HASH.SHA224 ###


@executor.registerCustomModule(
    name="hash.sha224",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_hash_sha224(arg: str):
    return hashlib.sha224(arg.encode()).hexdigest()


### HASH.SHA256 ###


@executor.registerCustomModule(
    name="hash.sha256",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_hash_sha256(arg: str):
    return hashlib.sha256(arg.encode()).hexdigest()


### HASH.SHA384 ###


@executor.registerCustomModule(
    name="hash.sha384",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_hash_sha384(arg: str):
    return hashlib.sha384(arg.encode()).hexdigest()


### HASH.SHA512 ###


@executor.registerCustomModule(
    name="hash.sha512",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_hash_sha512(arg: str):
    return hashlib.sha512(arg.encode()).hexdigest()


### BASE64.ENCODE ###


@executor.registerCustomModule(
    name="base64.encode",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_base64_encode(arg: str):
    return base64.b64encode(arg.encode()).decode()


### BASE64.DECODE ###


@executor.registerCustomModule(
    name="base64.decode",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_base64_decode(arg: str):
    return base64.b64decode(arg.encode()).decode()


### STRING.OFFSET.FORWARD ###


@executor.registerCustomModule(
    name="string.offset.forward",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_offset_forward(arg: str):
    new_string = ""
    for char in arg:
        new_string += chr(ord(char) - 1)
    return new_string


### STRING.OFFSET.BACKWARD ###


@executor.registerCustomModule(
    name="string.offset.backward",
    availableDatatypes=Tdt.String,
    handleResult=Thmr.assignToVar,
)
def handle_string_offset_backward(arg: str):
    new_string = ""
    for char in arg:
        new_string += chr(ord(char) + 1)
    return new_string


### NUMBER.PLUSBY ###


@executor.registerCustomModule(
    name="number.plusby",
    availableDatatypes=Tdt.Number,
    handleResult=Thmr.storeToCurrCell,
)
def handle_number_plusby(arg: int):
    return executor.cells[executor.cursor] + arg


### NUMBER.SUBTRACTBY ###


@executor.registerCustomModule(
    name="number.subtractby",
    availableDatatypes=Tdt.Number,
    handleResult=Thmr.storeToCurrCell,
)
def handle_number_subtractby(arg: int):
    return executor.cells[executor.cursor] - arg


### NUMBER.TIMESBY ###


@executor.registerCustomModule(
    name="number.timesby",
    availableDatatypes=Tdt.Number,
    handleResult=Thmr.storeToCurrCell,
)
def handle_number_timesby(arg: int):
    return executor.cells[executor.cursor] * arg


### NUMBER.PLUSBY ###


@executor.registerCustomModule(
    name="number.divideby",
    availableDatatypes=Tdt.Number,
    handleResult=Thmr.storeToCurrCell,
)
def handle_number_divideby(arg: int):
    return executor.cells[executor.cursor] // arg


### NUMBER.PLUSBY ###


@executor.registerCustomModule(
    name="number.powerby",
    availableDatatypes=Tdt.Number,
    handleResult=Thmr.storeToCurrCell,
)
def handle_number_powerby(arg: int):
    return executor.cells[executor.cursor] ** arg
