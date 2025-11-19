"""

https://stackoverflow.com/questions/26180528/convert-a-namedtuple-into-a-dictionary/26180604#26180604
"""
from collections import namedtuple
import inspect
import logging

logger = logging.getLogger(__name__)



def make_return_namedtuple(field_names, typename=None, prepend_name=False):

    # https://github.com/python/cpython/blob/main/Lib/collections/__init__.py
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))

    # https://docs.python.org/3/library/inspect.html#inspect.currentframe
    # https://stackoverflow.com/a/900404
    if not typename:
        typename = inspect.currentframe().f_back.f_code.co_name # .title().replace("_", "")
        #print(f"{typename=}")
    func_locals = dict(inspect.currentframe().f_back.f_locals)

    field_dict = {}
    # if prepend_name:
    #     field_dict[typename] = ""
    for _name in field_names:
        if _name in func_locals:
            field_dict[_name] = func_locals[_name]
        else:
            raise ValueError('make_return_namedtuple: ' + typename + ' Field missing: ' + _name)

    # if prepend_name:
    #     field_names.insert(0, typename)

    retTuple = namedtuple(typename, field_names)
    return retTuple(**field_dict)




def isinstance_namedtuple(obj, typename=None):
    """
    https://docs.python.org/3/library/collections.html#collections.namedtuple
    """
    if issubclass(type(obj), tuple) and hasattr(obj, "_asdict") and hasattr(obj, "__class__"):
        if typename and typename!=obj.__class__.__name__:
            return False
        return True
    else:
        return False


# a test...
def pipeline_properties(*, lp_props=None, **kwargs):
    if lp_props and isinstance_namedtuple(lp_props, "linepipe_properties"):
        for varname, value in lp_props._asdict():
            exec(f"{varname} = {value}")  # ???



# https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
# https://stackoverflow.com/a/62692640
# def isinstance_namedtuple(obj) -> bool:
#     return (
#             isinstance(obj, tuple) and
#             hasattr(obj, '_asdict') and
#             hasattr(obj, '_fields')
#     )


# test namedtuple ===============================================================================
def test_f():
    a = 1
    b = "2"
    x = 1.2
    _locals = locals()    
    print(f"test_f: {_locals=}")
    print(f"function name: {test_f.__name__}")
    print(f"class name: {test_f.__name__.title().replace("_", "")}")
    return dict(_locals)

def test_make_return_namedtuple():
    a = 1
    b = "2"
    x = 1.2
    #return makeReturnNamedTuple("TestMakeNamedTuple", "a b x", dict(locals()))    
    return make_return_namedtuple("a b x")


if __name__=="__main__":
    retVal = test_f()
    retTuple = test_make_return_namedtuple()
