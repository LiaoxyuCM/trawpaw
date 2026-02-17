## Only for testing purposes, not meant to be used in production

from trawpaw import Trawpaw, TrawpawDatatypes, TrawpawHandleModuleResult
import random

executor = Trawpaw()


@executor.registerCustomModule(
    "random",
    avaliableDatatypes=TrawpawDatatypes.Number,
    handleResult=TrawpawHandleModuleResult.printManually,
)
def handle_rand(limit: int) -> int:
    return random.randint(0, limit)


executor.unregisterCustomModule("random")


code = "+++++$ai$aw!$random$a"
result = executor.execute(code)

print(result.message)
