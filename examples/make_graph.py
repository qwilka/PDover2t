

# from ast import literal_eval as make_tuple
# https://stackoverflow.com/questions/9763116/parse-a-tuple-from-a-string
# https://stackoverflow.com/questions/36330860/pythoncially-check-if-a-variable-name-is-valid/36331242

import importlib
import inspect
import keyword

import pdover2t

mod = importlib.import_module("pdover2t.dnvgl_st_f101.press_contain")

def valid_identifier(name):
    avoidlist = ["int", "float", "str", "list", "tuple", "dict", "set"]
    if (str.isidentifier(name) and 
        not keyword.iskeyword(name) and
        name not in avoidlist):
        return True
    else:
        return False


CHECK_MOD = False

if CHECK_MOD:
    for itm in dir(mod):
        print(itm, end="")
        obj = getattr(mod, itm)
        print(" callable", callable(obj), end="")
        print(" isfunction", inspect.isfunction(obj))
        if callable(obj):
            #print(itm)
            try:
                _sig = inspect.signature(obj)
            except (ValueError, TypeError) as err:
                print("inspect.signature: cannot find sig:", itm)
                continue
            #print(list(_sig.parameters.items()))
            print(obj.__annotations__)
            if obj.__name__ == (lambda: None).__name__:   # '<lambda>'
                print("is lambda:", itm)
